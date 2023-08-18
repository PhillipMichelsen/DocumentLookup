import json

from app.handlers.chat_completion_handler import handle_chat_completion


def on_message_chat_completion(ch, method, properties, body):
    decoded_message_body = json.loads(body.decode('utf-8'))
    handle_chat_completion(decoded_message_body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
