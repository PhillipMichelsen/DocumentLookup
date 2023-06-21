import json
from app.handlers.embed import handle_embed
from app.utils.pika_handler import pika_handler


def on_message_embed(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))

    response = handle_embed(data)
    response_encoded_json = response.json().encode('utf-8')

    pika_handler.send_response(
        response=response_encoded_json,
        correlation_id=properties.correlation_id,
        delivery_tag=method.delivery_tag,
        reply_to=properties.reply_to
    )
