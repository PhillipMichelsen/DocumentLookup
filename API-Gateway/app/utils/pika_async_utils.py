import asyncio
import uuid
import logging

import aio_pika
import yaml

from app.config import settings


class PikaHelperAsync:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.service_id = None
        self.service_type = settings.service_type

        self.external_exchanges = {}

        self.service_exchange = None
        self.service_queues = {}

    async def init_connection(self, delay: int = 5, max_retries: int = 10):
        """Initialize connection to RabbitMQ

        :param delay: The delay in seconds between retries
        :param max_retries: The maximum number of retries

        :raises aio_pika.exceptions.AMQPConnectionError: If the connection cannot be established after max_retries
        """
        for attempt in range(1, max_retries + 1):
            try:
                self.connection = await aio_pika.connect_robust(
                    host=settings.rabbitmq_host,
                    login=settings.rabbitmq_username,
                    password=settings.rabbitmq_password
                )
                self.channel = await self.connection.channel()
                self.service_id = str(uuid.uuid4())

                logging.info(f"Connected to RabbitMQ as {self.service_type}. Service ID : {self.service_id}")
                break

            except aio_pika.exceptions.AMQPConnectionError as e:
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                else:
                    logging.error(f"Could not connect to RabbitMQ after {max_retries} attempts. Exiting.")
                    raise e

    async def declare_exchanges(self):
        with open('app/exchanges.yml') as f:
            data = yaml.safe_load(f)
            exchanges = data['exchanges'].values()

        for exchange in exchanges:
            declared_exchange = await self.channel.declare_exchange(
                exchange['name'],
                exchange['type'],
                durable=exchange.get('durable', False),
                auto_delete=exchange.get('auto_delete', False)
            )

            if exchange['name'] == f"{self.service_type}_exchange":
                self.service_exchange = declared_exchange

            self.external_exchanges[exchange['name']] = declared_exchange

            logging.debug(f"Declared exchange : {exchange['name']}")

    async def declare_queues(self):
        with open('app/service_queues.yml') as f:
            data = yaml.safe_load(f)
            queues = data['queues'].values()

        for queue in queues:
            declared_queue = await self.channel.declare_queue(
                queue['name'],
                durable=queue.get('durable', False),
                auto_delete=queue.get('auto_delete', False)
            )

            await declared_queue.bind(self.service_exchange, routing_key=f"#{queue['routing_key']}")
            await declared_queue.bind(self.service_exchange, routing_key=f"{self.service_id}{queue['routing_key']}")

            self.service_queues[queue['name']] = declared_queue

            logging.debug(f"Declared queue : {queue['name']}")

    async def publish_message(self, exchange_name: str, routing_key: str, headers: dict, message: bytes):
        """Publish a message to an exchange

        :param exchange_name: The name of the exchange
        :param routing_key: The routing key
        :param headers: The headers to add to the message
        :param message: The message to publish
        """
        await self.external_exchanges[exchange_name].publish(
            aio_pika.Message(
                body=message,
                headers=headers
            ),
            routing_key=routing_key
        )

        logging.info(f"[+] Published message to {exchange_name} with routing key {routing_key}")
        logging.debug(f"   Message : {message} \n"
                      f"   Headers : {headers}")


pika_helper = PikaHelperAsync()
