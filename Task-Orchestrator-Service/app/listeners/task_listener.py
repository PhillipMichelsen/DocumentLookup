import json
import logging

import aio_pika

from app.handlers.task_handler import handle_task


async def job_callback(message: aio_pika.IncomingMessage):
    decoded_message = json.loads(message.body.decode('utf-8'))
    logging.info(f"[*] Received task request: {decoded_message}")
    await handle_task(decoded_message)
    await message.ack()
