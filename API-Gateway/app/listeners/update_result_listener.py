import json

import aio_pika

from app.handlers.update_result_handler import handle_update_result


async def on_message_update_result(message: aio_pika.IncomingMessage):
    decoded_message_body = json.loads(message.body.decode('utf-8'))
    await handle_update_result(decoded_message_body)
    await message.ack()
