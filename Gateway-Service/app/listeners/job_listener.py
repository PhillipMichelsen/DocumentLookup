import json
import logging

import aio_pika

from app.handlers.job_handler import handle_job


async def job_callback(message: aio_pika.IncomingMessage):
    decoded_message = json.loads(message.body.decode('utf-8'))
    logging.info(f"[*] Received job: {decoded_message}")
    await handle_job(decoded_message, message.headers)
