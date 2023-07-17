import uuid

import pika

from app.config import settings


class PikaUtils:
    def __init__(self):
        """Connects to RabbitMQ and declares its exchange."""
        self.connection = None
        self.channel = None
        self.service_id = None

        self.service_exchange = None

    def init_connection(self, host: str, username: str, password: str):
        """Initialize connection to RabbitMQ

        :param host: The host of the RabbitMQ server
        :param username: The username of the RabbitMQ server
        :param password: The password of the RabbitMQ server

        :raises pika.exceptions.AMQPConnectionError: If the connection cannot be established after 10 attempts
        """
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=host,
                port=5672,
                virtual_host='/',
                credentials=pika.PlainCredentials(
                    username=username,
                    password=password
                ),
                connection_attempts=10,
                retry_delay=10,
            ))
            self.channel = self.connection.channel()
            self.service_id = str(uuid.uuid4())
        except pika.exceptions.AMQPConnectionError as error:
            raise error

    def declare_service_exchange(self, exchange_name: str) -> None:
        """Declares an exchange on the RabbitMQ server.

        :param exchange_name: The name of the exchange to declare
        """
        self.channel.exchange_declare(
            exchange=exchange_name,
            exchange_type='direct',
            durable=False,
            auto_delete=False
        )
        self.service_exchange = exchange_name

    def register_consumer(self, queue_name: str, routing_key: str, on_message_callback) -> None:
        """Registers a queue and consumes messages from it

        :param on_message_callback:
        :param queue_name: The name of the queue
        :param routing_key: The routing key
        """
        self.channel.queue_declare(
            queue=queue_name,
            durable=False,
            auto_delete=False
        )

        self.channel.queue_bind(
            exchange=self.service_exchange,
            queue=queue_name,
            routing_key=routing_key
        )

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message_callback
        )

    def publish_response(self, message: bytes) -> None:
        """Publish a response message to the task orchestrator.

        :param message: The message to publish
        """
        self.channel.basic_publish(
            exchange=settings.task_orchestrator_exchange,
            routing_key=settings.task_orchestrator_response_routing_key,
            body=message
        )

    def start_consuming(self):
        """Starts consuming messages from the registered consumers."""
        print(f"Service {self.service_id} is listening for messages...", flush=True)
        self.channel.start_consuming()


# Create singleton instance of PikaHandler
pika_utils = PikaUtils()
