import json

from app.handlers.embed_handler import handle_embed
from app.utils.pika_helper import pika_handler


def on_message_embed(ch, method, properties, body):
    """Embed listener

    Decodes payload and sends to the embed handler. Response from handler is encoded and sent to response queue.
    """
    data = json.loads(body.decode('utf-8'))

    response = handle_embed(data)
    response_encoded = response.json().encode('utf-8')

    pika_handler.send_response(
        response=response_encoded,
        correlation_id=properties.correlation_id,
        delivery_tag=method.delivery_tag,
        reply_to=properties.reply_to
    )
