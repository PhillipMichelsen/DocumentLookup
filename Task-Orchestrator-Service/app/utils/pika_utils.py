import logging
import uuid
import time

import pika
import yaml

from app.config import settings


class PikaUtilsTaskOrchestrator:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.service_id = None

        self.service_exchange = None
        self.service_queues = {}

    def init_connection(self, delay: int = 5, max_retries: int = 10):
        """Initialize connection to RabbitMQ

        :param delay: The delay in seconds between retries
        :param max_retries: The maximum number of retries

        :raises aio_pika.exceptions.AMQPConnectionError: If the connection cannot be established after max_retries
        """
        for attempt in range(1, max_retries + 1):
            try:
                print(settings.rabbitmq_host, settings.rabbitmq_username, settings.rabbitmq_password, flush=True)
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host=settings.rabbitmq_host,
                    port=5672,
                    virtual_host='/',
                    credentials=pika.PlainCredentials(settings.rabbitmq_username, settings.rabbitmq_password),
                    connection_attempts=10,
                    retry_delay=10,
                ))
                self.channel = self.connection.channel()
                self.service_id = str(uuid.uuid4())

                logging.info(f"[*] Connected to RabbitMQ! Service ID : {self.service_id}")
                break

            except pika.exceptions.AMQPConnectionError as e:
                if attempt < max_retries:
                    time.sleep(delay)
                else:
                    logging.critical(f"[!!!] Could not connect to RabbitMQ after {max_retries} attempts. Exiting.")
                    raise e

    def declare_exchanges(self):
        with open('app/exchanges.yaml') as f:
            data = yaml.safe_load(f)
            exchanges = data['exchanges'].values()

        for exchange in exchanges:
            declared_exchange = self.channel.exchange_declare(
                exchange['name'],
                exchange['type'],
                durable=exchange.get('durable', False),
                auto_delete=exchange.get('auto_delete', False)
            )

            if exchange['name'] == settings.service_exchange:
                self.service_exchange = exchange['name']

            logging.debug(f"[*] Declared exchange : {exchange['name']}")

    def register_consumer(self, queue_name: str, routing_key: str, on_message_callback):
        """Registers a queue and consumes messages from it

        :param queue_name: The name of the queue
        :param routing_key: The routing key
        """
        self.channel.queue_declare(
            queue=queue_name,
            durable=True,
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

        logging.debug(f"[*] Registered queue : {queue_name}")

    def publish_message(self, exchange_name: str, routing_key: str, message: bytes):
        """Publish a message to an exchange

        :param exchange_name: The name of the exchange
        :param routing_key: The routing key
        :param message: The message to publish
        """
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message
        )

        logging.info(f"[-] Published message to {exchange_name} with routing key {routing_key}")

    def start_consuming(self):
        """Starts consuming messages from the registered consumers."""
        logging.info("[*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()


pika_helper = PikaUtilsTaskOrchestrator()
