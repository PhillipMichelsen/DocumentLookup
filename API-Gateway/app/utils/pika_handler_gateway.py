import asyncio
import uuid

import aio_pika

from app.config import settings, exchanges_routing


class PikaHandler:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue_name = str(uuid.uuid4())
        self.response_exchange = None
        self.pending_responses = {}

    async def init_connection(self):
        self.connection = await aio_pika.connect_robust(
            host=settings.rabbitmq_host,
            login=settings.rabbitmq_username,
            password=settings.rabbitmq_password
        )
        self.channel = await self.connection.channel()
        self.response_exchange = await self.channel.declare_exchange(exchanges_routing.response_exchange, aio_pika.ExchangeType.DIRECT)

        asyncio.create_task(self.listen_for_responses())

    async def send_message(self, exchange_name, routing_key, message):
        corr_id = str(uuid.uuid4())

        exchange = await self.channel.declare_exchange(exchange_name, aio_pika.ExchangeType.DIRECT)

        await exchange.publish(
            aio_pika.Message(
                body=message,
                correlation_id=corr_id,
                content_type='application/json',
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                reply_to=self.queue_name
            ),
            routing_key=routing_key,
        )

        event = asyncio.Event()
        self.pending_responses[corr_id] = (event, None)

        return corr_id

    async def get_response(self, corr_id, timeout=10):
        event, response = self.pending_responses[corr_id]

        try:
            await asyncio.wait_for(event.wait(), timeout=timeout)
            _, response = self.pending_responses[corr_id]
        except asyncio.TimeoutError:
            raise Exception("Timed out")
        finally:
            del self.pending_responses[corr_id]

        return response

    async def listen_for_responses(self):
        response_queue = await self.channel.declare_queue(self.queue_name, auto_delete=True)
        await response_queue.bind(self.response_exchange, routing_key=self.queue_name)

        async def callback(message: aio_pika.IncomingMessage):
            corr_id = message.correlation_id

            if corr_id in self.pending_responses:
                event, _ = self.pending_responses[corr_id]
                self.pending_responses[corr_id] = (event, message.body)
                event.set()

            await message.ack()

        await response_queue.consume(callback)


pika_handler = PikaHandler()
