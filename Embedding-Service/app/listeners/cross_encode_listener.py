import json
import logging

from app.handlers.cross_encode_handler import handle_cross_encode
from app.utils.pika_utils import pika_utils


def on_message_rerank(ch, method, properties, body):
    data = json.loads(body.decode('utf-8'))
    logging.debug(f"[+] Received cross-encode job for task: {properties.headers['task_id']}")

    response = handle_cross_encode(data)
    response = response.json()

    pika_utils.send_response(
        response=response.encode('utf-8'),
        delivery_tag=method.delivery_tag,
        headers=properties.headers
    )
