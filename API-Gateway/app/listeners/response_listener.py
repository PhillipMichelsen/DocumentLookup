import aio_pika
import json

from app.handlers.response_handler import handle_response


async def response_callback(message: aio_pika.IncomingMessage):
    decoded_message = json.loads(message.body.decode('utf-8'))
    await handle_response(decoded_message, message.headers)
