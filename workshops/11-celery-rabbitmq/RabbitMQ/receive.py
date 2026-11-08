import pika, sys, os

def main():
    # Establish a connection with the RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Redeclare the queue because we are unsure whether or not the queue exists. 
    channel.queue_declare(queue='hello', durable=True)

    # RabbitMQ will trigger this function once we receive a message.
    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")

    # Subscribe to the "hello" queue. 
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)