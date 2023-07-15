import json
import logging

from app.handlers.embed_handler import handle_embed


def on_message_embed(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    logging.debug(f"[+] Received embed job for job!")
    handle_embed(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)

