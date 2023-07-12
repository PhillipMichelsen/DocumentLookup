import logging

import pika

from app.config import settings


class PikaHandler:
    def __init__(self):
        """Connects to RabbitMQ and declares its exchange."""
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            port=5672,
            virtual_host='/',
            credentials=pika.PlainCredentials(settings.rabbitmq_username, settings.rabbitmq_password),
            connection_attempts=10,
            retry_delay=10,
        ))
        self.channel = self.connection.channel()
        self.exchange_name = settings.service_exchange
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct')
        logging.info(f"[!] Connected to RabbitMQ as {self.exchange_name}, host: {settings.rabbitmq_host}")

    def register_consumer(self, queue_name, routing_key, on_message_callback):
        """Registers a consumer for a queue and routing key.

        :param queue_name: Name of the queue to consume from
        :param routing_key: Routing key to bind to
        :param on_message_callback: Callback function to call when a message is received
        """
        self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange=self.exchange_name, queue=queue_name, routing_key=routing_key)
        self.channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback, auto_ack=False)

        logging.info(f"[*] Registered consumer for queue: {queue_name}, routing key: {routing_key}")

    def send_response(self, response, delivery_tag, headers):
        """Sends a response to the gateway_exchange

        :param response: Response to send
        :param delivery_tag: Delivery tag of the request
        :param headers: Headers dictionary to include in the message
        """
        properties = pika.BasicProperties(
            headers=headers,  # Include headers in properties
        )
        self.channel.basic_publish(
            exchange=settings.gateway_exchange,
            routing_key='.response',
            properties=properties,
            body=response
        )
        self.channel.basic_ack(delivery_tag=delivery_tag)

        logging.debug(f"[-] Sent response for task: {headers['task_id']}")

    def start_consuming(self):
        """Starts consuming messages from the registered consumers."""
        logging.info("[*] Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()


# Create singleton instance of PikaHandler
pika_handler = PikaHandler()
