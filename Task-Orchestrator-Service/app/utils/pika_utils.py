import asyncio
import logging
import uuid

import aio_pika
import yaml

from app.config import settings


class PikaUtilsTaskOrchestrator:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.service_id = None

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
                print(settings.rabbitmq_host, settings.rabbitmq_username, settings.rabbitmq_password, flush=True)
                self.connection = await aio_pika.connect_robust(
                    host=settings.rabbitmq_host,
                    login=settings.rabbitmq_username,
                    password=settings.rabbitmq_password
                )
                self.channel = await self.connection.channel()
                self.service_id = str(uuid.uuid4())

                logging.info(f"[*] Connected to RabbitMQ! Service ID : {self.service_id}")
                break

            except aio_pika.exceptions.AMQPConnectionError as e:
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                else:
                    logging.critical(f"[!!!] Could not connect to RabbitMQ after {max_retries} attempts. Exiting.")
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

            if exchange['name'] == f"task_orchestrator_exchange":
                self.service_exchange = declared_exchange
            else:
                self.external_exchanges[exchange['name']] = declared_exchange

            logging.debug(f"[*] Declared exchange : {exchange['name']}")

    async def register_consumer(self, queue_name: str, routing_key: str, callback):
        """Registers a queue and consumes messages from it

        :param queue_name: The name of the queue
        :param routing_key: The routing key
        :param callback: The callback function to call when a message is received
        """
        declared_queue = await self.channel.declare_queue(
            queue_name,
            durable=True,
            auto_delete=False
        )

        await declared_queue.bind(
            self.service_exchange,
            routing_key=routing_key
        )

        await declared_queue.consume(callback)

        self.service_queues[queue_name] = declared_queue

        logging.debug(f"[*] Registered queue : {queue_name} for callback {callback.__name__}")

    async def publish_job(self, exchange_name: str, routing_key: str, message: bytes):
        """Publish a message to an exchange

        :param exchange_name: The name of the exchange
        :param routing_key: The routing key
        :param message: The message to publish
        """
        await self.external_exchanges[exchange_name].publish(
            aio_pika.Message(
                body=message,
            ),
            routing_key=routing_key
        )

        logging.info(f"[-] Published message to {exchange_name} with routing key {routing_key}")

    async def publish_reply(self, api_gateway_id: str, task_id: str, message: bytes):
        """Publish a message to an API-Gateway's response queue

        :param api_gateway_id: The ID of the API-Gateway
        :param task_id: The ID of the task
        :param message: The message to publish
        """
        await self.external_exchanges['api_gateway_exchange'].publish(
            aio_pika.Message(
                body=message,
                headers={"task-id": task_id}
            ),
            routing_key=api_gateway_id
        )

        logging.info(f"[-] Published reply to {api_gateway_id} for task {task_id}")


pika_helper = PikaUtilsTaskOrchestrator()
