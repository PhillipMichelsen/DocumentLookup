import json

from app.handlers.embed_handler import handle_embed
from app.utils.pika_helper import pika_handler


def on_message_embed(ch, method, properties, body):
    """Embed listener

    Decodes payload and sends to the embed handler. Response from handler is encoded and sent to response queue.
    """
    data = json.loads(body.decode('utf-8'))
    print(f"Received embed request!", flush=True)

    response = handle_embed(data)
    response = response.json()

    pika_handler.send_response(
        response=response.encode('utf-8'),
        delivery_tag=method.delivery_tag,
        headers=properties.headers
    )
