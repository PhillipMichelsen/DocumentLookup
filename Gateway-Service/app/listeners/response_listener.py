import logging
import json

import aio_pika

from app.handlers.response_handler import handle_response


async def response_callback(message: aio_pika.IncomingMessage):
    decoded_message_body = json.loads(message.body.decode('utf-8'))
    logging.info(f"[*] Received response")
    await handle_response(decoded_message_body)
    await message.ack()
