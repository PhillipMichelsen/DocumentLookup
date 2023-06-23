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

    async def init_connection(self, delay=5, max_retries=10):
        """Initialize connection to RabbitMQ

        :param delay: The delay in seconds between retries
        :type delay: int
        :param max_retries: The maximum number of retries
        :type max_retries: int

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
                self.response_exchange = await self.channel.declare_exchange(exchanges_routing.response_exchange,
                                                                             aio_pika.ExchangeType.DIRECT)

                asyncio.create_task(self._listen_for_responses())
                # If the connection was successful, break out of the loop
                break
            except aio_pika.exceptions.AMQPConnectionError as e:
                print(f"Attempt {attempt} - Error connecting to RabbitMQ: {str(e)}")
                if attempt < max_retries:
                    await asyncio.sleep(delay)
                else:
                    raise

    async def send_message(self, exchange_name: str, routing_key: str, message: bytes) -> str:
        """Sends a message to the specified exchange and routing key and returns the correlation id

        :param exchange_name: The name of the exchange to send the message to
        :type exchange_name: str
        :param routing_key: The routing key to use
        :type routing_key: str
        :param message: The message to send, in utf-8 bytes
        :type message: bytes
        :return: The correlation id of the message
        :rtype: str
        """
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

    async def get_response(self, corr_id: str, timeout: int = 10) -> bytes:
        """Gets the response for the specified correlation id

        :param corr_id: The correlation id to get the response for
        :type corr_id: str
        :param timeout: The timeout in seconds
        :type timeout: int
        :return: The response, in utf-8 bytes
        :rtype: bytes

        :raises Exception: If the timeout is reached
        """
        event, response = self.pending_responses[corr_id]

        try:
            await asyncio.wait_for(event.wait(), timeout=timeout)
            _, response = self.pending_responses[corr_id]
        except asyncio.TimeoutError:
            raise Exception("Timed out")
        finally:
            del self.pending_responses[corr_id]

        return response

    async def _listen_for_responses(self):
        """Listens for responses from the response queue and adds them to `pending_responses` as they appear.

        This private method is called when the connection is established, it runs in the background.
        """

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
