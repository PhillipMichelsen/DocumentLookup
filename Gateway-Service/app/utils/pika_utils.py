import asyncio
import logging
import uuid

import aio_pika
import yaml

from app.config import settings


class PikaUtilsAsync:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.service_id = None

        self.service_exchange = None
        self.response_queue = None

        self.task_orchestrator_exchange = None
        self.task_request_queue = None

    async def init_connection(self, host: str, username: str, password: str, delay: int = 5, max_retries: int = 10):
        """Initialize connection to RabbitMQ

        :param host: The host of the RabbitMQ server
        :param username: The username of the RabbitMQ server
        :param password: The password of the RabbitMQ server
        :param delay: The delay in seconds between retries
        :param max_retries: The maximum number of retries

        :raises aio_pika.exceptions.AMQPConnectionError: If the connection cannot be established after max_retries
        """
        for attempt in range(1, max_retries + 1):
            try:
                self.connection = await aio_pika.connect_robust(
                    host=host,
                    login=username,
                    password=password,
                )
                self.channel = await self.connection.channel()
                self.service_id = str(uuid.uuid4())

                logging.info(f"Connected to RabbitMQ. Service ID : {self.service_id}")
                break

            except aio_pika.exceptions.AMQPConnectionError as e:
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                else:
                    logging.error(f"Could not connect to RabbitMQ after {max_retries} attempts. Exiting.")
                    raise e

    async def declare_exchanges(self, service_exchange: str, task_orchestrator_exchange: str):

        self.service_exchange = await self.channel.declare_exchange(
            name=service_exchange,
            type='direct',
            durable=False,
            auto_delete=False
        )

        self.task_orchestrator_exchange = await self.channel.declare_exchange(
            name=task_orchestrator_exchange,
            type='direct',
            durable=False,
            auto_delete=False
        )

        logging.debug(f"Declared exchanges: {service_exchange}, {task_orchestrator_exchange}")

    async def declare_queues(self, task_request_queue: str, task_request_routing_key: str):

        self.response_queue = await self.channel.declare_queue(
            name=self.service_id,
            durable=False,
            auto_delete=True
        )
        await self.response_queue.bind(self.service_exchange, routing_key=self.service_id)
        logging.info(f"Declared response queue: {self.service_id}, bound with routing key: {self.service_id}")

        self.task_request_queue = await self.channel.declare_queue(
            name=task_request_queue,
            durable=False,
            auto_delete=False
        )
        await self.task_request_queue.bind(self.task_orchestrator_exchange, routing_key=task_request_routing_key)

        logging.info(f"Declared task request queue: {task_request_queue}, bound with routing key: {task_request_routing_key}")

    async def publish_task(self, message: bytes, task_request_routing_key: str) -> None:
        """Publish a message to an exchange

        :param message: The message to publish
        :param task_request_routing_key: The routing key to use
        """

        await self.task_orchestrator_exchange.publish(
            aio_pika.Message(
                body=message
            ),
            routing_key=task_request_routing_key
        )

        logging.info(f"[+] Published message to task orchestrator")
        logging.debug(f"   Message : {message}")


pika_helper = PikaUtilsAsync()
