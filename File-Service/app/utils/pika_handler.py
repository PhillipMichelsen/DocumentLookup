import pika

from app.config import settings


class PikaHandler:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            port=5672,
            virtual_host='/',
            credentials=pika.PlainCredentials(settings.rabbitmq_username, settings.rabbitmq_password),
            connection_attempts=10,
            retry_delay=10,
        ))
        self.channel = self.connection.channel()
        self.exchange_name = settings.self_exchange
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct')

    def register_consumer(self, queue_name, routing_key, on_message_callback):
        self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange=self.exchange_name, queue=queue_name, routing_key=routing_key)
        self.channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback, auto_ack=False)

    def send_response(self, message, correlation_id, reply_to):
        self.channel.basic_publish(
            exchange=settings.response_exchange,
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=message
        )

    def send_message_internal(self, exchange_name, routing_key, message):
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message
        )

    def start_consuming(self):
        print("STARTING MESSAGE CONSUME!!", flush=True)
        self.channel.start_consuming()


pika_handler = PikaHandler()
