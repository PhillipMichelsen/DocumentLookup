import json

from app.handlers.job_request_handler import handle_job_request


def on_message_job_request(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_job_request(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
