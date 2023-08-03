import json

from app.handlers.job_request_handler import handle_job_request


def job_request_callback(ch, method, properties, body):
    print(" [x] Received %r" % body, flush=True)
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_job_request(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
