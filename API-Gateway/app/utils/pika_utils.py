import asyncio
import uuid

import aio_pika


class PikaUtilsAsync:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.service_id = None

        self.service_exchange = None
        self.response_queue = None

        self.task_orchestrator_exchange = None
        self.task_request_queue = None
        self.task_request_routing_key = None

    async def init_connection(self, host: str, username: str, password: str):
        """Initialize connection to RabbitMQ

        :param host: The host of the RabbitMQ server
        :param username: The username of the RabbitMQ server
        :param password: The password of the RabbitMQ server

        :raises aio_pika.exceptions.AMQPConnectionError: If the connection cannot be established after max_retries
        """
        for attempt in range(1, 7):
            try:
                self.connection = await aio_pika.connect_robust(
                    host=host,
                    login=username,
                    password=password,
                )
                self.channel = await self.connection.channel()
                self.service_id = str(uuid.uuid4())

                break

            except aio_pika.exceptions.AMQPConnectionError as error:
                if attempt < 6:
                    await asyncio.sleep(10)
                else:
                    raise error

    async def declare_exchanges(self, service_exchange: str, task_orchestration_exchange: str):
        """Declares exchanges essential for the service

        :param service_exchange: The name of the exchange for this service
        :param task_orchestration_exchange: The name of the task_orchestration exchange
        """
        self.service_exchange = await self.channel.declare_exchange(
            name=service_exchange,
            type='direct',
            durable=False,
            auto_delete=False
        )

        self.task_orchestrator_exchange = await self.channel.declare_exchange(
            name=task_orchestration_exchange,
            type='direct',
            durable=False,
            auto_delete=False
        )

    async def declare_queues(self, task_request_queue: str, task_request_routing_key: str):
        """Declares queues essential for the service.

        :param task_request_queue: Name of the task_request_queue
        :param task_request_routing_key: Routing key for the task_request_queue
        """
        self.response_queue = await self.channel.declare_queue(
            name=self.service_id,
            durable=False,
            auto_delete=True
        )
        await self.response_queue.bind(self.service_exchange, routing_key=self.service_id)

        self.task_request_queue = await self.channel.declare_queue(
            name=task_request_queue,
            durable=False,
            auto_delete=False
        )
        await self.task_request_queue.bind(self.task_orchestrator_exchange, routing_key=task_request_routing_key)

        self.task_request_routing_key = task_request_routing_key

    async def publish_task(self, message: bytes) -> None:
        """Publish a message to an exchange

        :param message: The message to publish
        """
        await self.task_orchestrator_exchange.publish(
            aio_pika.Message(
                body=message
            ),
            routing_key=self.task_request_routing_key
        )


pika_helper = PikaUtilsAsync()
