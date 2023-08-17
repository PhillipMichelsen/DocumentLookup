import json

import aio_pika

from app.handlers.job_response_handler import handle_job_response


async def on_message_job_response(message: aio_pika.IncomingMessage):
    decoded_message_body = json.loads(message.body.decode('utf-8'))
    await handle_job_response(decoded_message_body)
    await message.ack()
