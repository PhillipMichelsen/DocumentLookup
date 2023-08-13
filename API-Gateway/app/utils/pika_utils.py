import uuid

import aio_pika
import yaml

from app.config import settings


class PikaUtilsAsync:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.service_id = str(uuid.uuid4())
        self.service_exchange = settings.service_exchange

    async def init_connection(self, host: str, username: str, password: str):
        self.connection = await aio_pika.connect_robust(
            host=host,
            login=username,
            password=password,
            timeout=10
        )
        self.channel = await self.connection.channel()

    async def declare_exchanges(self, exchanges_file: str) -> None:
        """Declares exchanges from a YAML file

        :param exchanges_file: The path to the YAML file
        :return: None
        """
        with open(exchanges_file) as f:
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
        queue = await self.channel.declare_queue(
            name=queue_name,
            durable=False,
            auto_delete=auto_delete
        )
        await queue.bind(exchange, routing_key=routing_key)
        await queue.consume(on_message_callback)

    async def publish_message(self, exchange_name: str, routing_key: str, message: bytes):
        exchange = await self.channel.declare_exchange(exchange_name)
        await exchange.publish(
            aio_pika.Message(
                body=message
            ),
            routing_key=routing_key
        )
        print(f"Message published to exchange {exchange_name} with routing key {routing_key}, content: {message}",
              flush=True)


pika_utils = PikaUtilsAsync()
