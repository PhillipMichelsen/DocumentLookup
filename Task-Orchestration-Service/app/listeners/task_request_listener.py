import json

from app.handlers.task_request_handler import handle_task


def task_request_callback(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_task(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
