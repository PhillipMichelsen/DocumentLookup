import uuid

import pika
import yaml

from app.config import settings


class PikaUtils:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.service_id = None

        self.service_exchange = None

    def init_connection(self, host: str, username: str, password: str) -> None:
        """Initialize connection to RabbitMQ

        :param host: The host of the RabbitMQ server
        :param username: The username of the RabbitMQ server
        :param password: The password of the RabbitMQ server
        :return: None

        :raises aio_pika.exceptions.AMQPConnectionError: If the connection cannot be established after 10 attempts
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=host,
            port=5672,
            virtual_host='/',
            credentials=pika.PlainCredentials(username, password),
            connection_attempts=10,
            retry_delay=10,
        ))
        self.channel = self.connection.channel()
        self.service_id = str(uuid.uuid4())

    def declare_exchanges(self, exchanges_file: str) -> None:
        """Declares exchanges from a YAML file

        :param exchanges_file: The path to the YAML file
        :return: None
        """
        with open(exchanges_file) as f:
            data = yaml.safe_load(f)
            exchanges = data['exchanges'].values()

        for exchange in exchanges:
            self.channel.exchange_declare(
                exchange['name'],
                exchange['type'],
                durable=exchange.get('durable', False),
                auto_delete=exchange.get('auto_delete', False)
            )

            if exchange['name'] == settings.service_exchange:
                self.service_exchange = exchange['name']

    def register_consumer(self, queue_name: str, exchange: str, routing_key: str, on_message_callback,
                          auto_delete: bool) -> None:
        """Registers a queue and consumes messages from it

        :param on_message_callback:
        :param queue_name: The name of the queue
        :param exchange: The name of the exchange
        :param routing_key: The routing key
        :param on_message_callback: The callback function to be called when a message is received
        :param auto_delete: Whether the queue should be deleted when the consumer disconnects
        :return: None
        """
        self.channel.queue_declare(
            queue=queue_name,
            durable=False,
            auto_delete=auto_delete
        )

        self.channel.queue_bind(
            exchange=exchange,
            queue=queue_name,
            routing_key=routing_key
        )

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message_callback
        )

    def publish_message(self, exchange_name: str, routing_key: str, message: bytes) -> None:
        """Publish a message to an exchange

        :param exchange_name: The name of the exchange
        :param routing_key: The routing key
        :param message: The message to publish
        :return: None
        """
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message
        )
        print(f"Message published to exchange {exchange_name} with routing key {routing_key}",
              flush=True)

    def start_consuming(self) -> None:
        """Starts consuming messages from the registered consumers.

        :return: None
        """
        print(f"Service {self.service_id} is listening for messages...", flush=True)
        self.channel.start_consuming()


pika_utils = PikaUtils()
