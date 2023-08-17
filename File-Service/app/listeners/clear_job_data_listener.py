import json

from app.handlers.clear_job_data_handler import handle_clear_job_data


def on_message_clear_job_data(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_clear_job_data(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
