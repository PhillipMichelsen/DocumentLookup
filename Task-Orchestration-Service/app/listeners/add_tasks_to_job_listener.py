import json

from app.handlers.add_tasks_to_job_handler import handle_add_tasks_to_job


def on_message_add_tasks_to_job(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_add_tasks_to_job(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
