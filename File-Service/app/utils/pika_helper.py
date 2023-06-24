import pika

from app.config import settings


class PikaHelper:
    def __init__(self):
        """Connects to RabbitMQ and declares its exchange."""
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=settings.rabbitmq_host,
            port=5672,
            virtual_host='/',
            credentials=pika.PlainCredentials(settings.rabbitmq_username, settings.rabbitmq_password),
            connection_attempts=100,
            retry_delay=10,
        ))
        self.channel = self.connection.channel()
        self.exchange_name = settings.embedding_exchange
        self.channel.exchange_declare(exchange=self.exchange_name, exchange_type='direct')
        self.debug = settings.debug
        print(f"Connected to RabbitMQ as {self.exchange_name}, host: {settings.rabbitmq_host}", flush=True)

    def register_consumer(self, queue_name, routing_key, on_message_callback):
        """Registers a consumer for a queue and routing key.

        :param queue_name: Name of the queue to consume from
        :param routing_key: Routing key to bind to
        :param on_message_callback: Callback function to call when a message is received
        """
        self.channel.queue_declare(queue=queue_name)
        self.channel.queue_bind(exchange=self.exchange_name, queue=queue_name, routing_key=routing_key)
        self.channel.basic_consume(queue=queue_name, on_message_callback=on_message_callback, auto_ack=False)

        if self.debug:
            print(f"+ Registered consumer for queue: {queue_name}, routing key: {routing_key}", flush=True)

    def send_response(self, response, correlation_id, delivery_tag, reply_to):
        """Sends a response to the response_exchange

        :param response: Response to send
        :param correlation_id: Correlation id of the request
        :param delivery_tag: Delivery tag of the request
        :param reply_to: Routing key to send the response to
        """
        self.channel.basic_publish(
            exchange=settings.response_exchange,
            routing_key=reply_to,
            properties=pika.BasicProperties(correlation_id=correlation_id),
            body=response
        )
        self.channel.basic_ack(delivery_tag=delivery_tag)

        if self.debug:
            print(f"|| Sent response to routing key: {reply_to}", flush=True)

    def send_message(self, exchange_name: str, routing_key: str, message: bytes):
        """Sends a message to the specified exchange and routing key.


        :param exchange_name: Name of the exchange to send the message to
        :param routing_key: Routing key to send the message to
        :param message: Contents of message to send
        """
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=message
        )

    def start_consuming(self):
        """Starts consuming messages from the registered consumers."""
        print("Waiting for messages...", flush=True)
        self.channel.start_consuming()


# Create singleton instance of PikaHandler
pika_helper = PikaHelper()
