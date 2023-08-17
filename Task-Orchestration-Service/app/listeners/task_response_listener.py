import json

from app.handlers.task_response_handler import handle_task_response


def on_message_task_response(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_task_response(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
