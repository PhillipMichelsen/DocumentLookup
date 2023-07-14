import json
import logging

from app.handlers.task_request_handler import handle_task


def task_request_callback(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    logging.info(f"[*] Received task request")
    handle_task(decoded_message_body, properties.headers)
    ch.basic_ack(delivery_tag=method.delivery_tag)
