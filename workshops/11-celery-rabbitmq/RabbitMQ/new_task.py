import pika
import sys

# Create a connection with RabbitMQ server. 
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

# Create a durable queue
#channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"

channel.basic_publish(
    exchange='',
    routing_key='hello',
    body=message,
)

#Make the message persistent
# channel.basic_publish(
#     exchange='',
#     routing_key='task_queue',
#     body=message,
#     properties=pika.BasicProperties(
#         delivery_mode=pika.DeliveryMode.Persistent
#     ))
print(f" [x] Sent {message}")
connection.close()