import aio_pika
import json

from app.handlers.job_handler import handle_job


async def job_callback(message: aio_pika.IncomingMessage):
    decoded_message = json.loads(message.body.decode('utf-8'))
    print(f"Received job {decoded_message}", flush=True)
    await handle_job(decoded_message, message.headers)
