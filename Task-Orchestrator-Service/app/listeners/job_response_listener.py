import json
import logging

from app.handlers.job_response_handler import handle_job


def job_response_callback(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    logging.info(f"[*] Received job")
    handle_job(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
