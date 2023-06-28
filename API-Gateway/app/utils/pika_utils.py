import asyncio
import uuid
import json
from pydantic import BaseModel

import aio_pika

from app.config import settings
from app.utils.task_utils import job_executor


class PikaHelperGateway:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.service_id = None
        self.service_type = "gateway"

        self.exchanges = {}
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
                break

            except aio_pika.exceptions.AMQPConnectionError as e:
                print(f"Attempt {attempt} - Error connecting to RabbitMQ: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                else:
                    raise

    async def publish_message(self, exchange_name: str, routing_key: str, task_id:str, message: bytes):
        """Publish a message to an exchange

        :param exchange_name: The name of the exchange
        :param routing_key: The routing key
        :param task_id: The task ID
        :param message: The message to publish
        """
        await self.exchanges[exchange_name].publish(
            aio_pika.Message(
                body=message,
                headers={'task_id': task_id}
            ),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            routing_key=routing_key
        )

    async def _job_callback(self, message: aio_pika.IncomingMessage):
        task_id = message.headers['task_id']

        job_executor.execute_job(task_id)

    async def _response_callback(self, message: aio_pika.IncomingMessage):
        task_id = message.headers['task_id']
        # TODO: Handle response, create function in TaskHandler
        raise NotImplementedError


pika_helper = PikaHelperGateway()
