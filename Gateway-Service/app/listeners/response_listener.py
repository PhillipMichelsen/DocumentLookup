import aio_pika
import json
import logging

from app.handlers.response_handler import handle_response


async def response_callback(message: aio_pika.IncomingMessage):
    decoded_message = message.body.decode('utf-8')
    logging.info(f"[*] Received response for task ID: {message.headers['task_id']}")

    await handle_response(decoded_message, message.headers)
