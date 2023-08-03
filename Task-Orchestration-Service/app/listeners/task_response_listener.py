import json

from app.handlers.task_response_handler import handle_task_response


def task_response_callback(ch, method, properties, body):
    print(" [x] Received %r" % body, flush=True)
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_task_response(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
