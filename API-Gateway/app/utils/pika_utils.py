import uuid

import aio_pika
import yaml

from app.config import settings


class PikaUtilsAsync:
    """A class to handle RabbitMQ connections and exchanges

    This class is a singleton, so it can be imported and used anywhere in the app.
    """

    def __init__(self):
        self.connection = None
        self.channel = None
        self.service_id = str(uuid.uuid4())
        self.service_exchange = settings.service_exchange

    async def init_connection(self, host: str, username: str, password: str):
        """Initializes a connection to RabbitMQ"""
        self.connection = await aio_pika.connect_robust(
            host=host,
            login=username,
            password=password,
            timeout=30
        )
        self.channel = await self.connection.channel()

    async def declare_exchanges(self) -> None:
        """Declares exchanges from a YAML file

        :return: None
        """
        with open('app/exchanges.yaml') as f:
            data = yaml.safe_load(f)
            exchanges = data['exchanges'].values()

        for exchange in exchanges:
            await self.channel.declare_exchange(
                name=exchange['name'],
                type=exchange['type'],
                durable=exchange.get('durable', False),
                auto_delete=exchange.get('auto_delete', False)
            )

    async def register_consumer(self, queue_name: str, exchange: str, routing_key: str, on_message_callback,
                                auto_delete: bool) -> None:
        """Registers a consumer for a queue (will create a queue if it doesn't exist)"""
        queue = await self.channel.declare_queue(
            name=queue_name,
            durable=False,
            auto_delete=auto_delete
        )
        await queue.bind(exchange, routing_key=routing_key)
        await queue.consume(on_message_callback)

    async def publish_message(self, exchange_name: str, routing_key: str, message: bytes):
        """Publishes a message to an exchange"""
        exchange = await self.channel.declare_exchange(exchange_name)
        await exchange.publish(
            aio_pika.Message(
                body=message
            ),
            routing_key=routing_key
        )
        print(f"Message published to exchange {exchange_name} with routing key {routing_key}",
              flush=True)


pika_utils = PikaUtilsAsync()
