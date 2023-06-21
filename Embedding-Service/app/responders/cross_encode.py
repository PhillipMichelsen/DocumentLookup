import json
from app.handlers.cross_encode import handle_cross_encode
from app.utils.pika_handler import pika_handler


def on_message_rerank(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))

    response = handle_cross_encode(data)
    response_encoded_json = response.json().encode('utf-8')

    pika_handler.send_response(
        response=response_encoded_json,
        correlation_id=properties.correlation_id,
        delivery_tag=method.delivery_tag,
        reply_to=properties.reply_to
    )
