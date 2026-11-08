import pika

# Create a connection with localhost
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Create a queue name "hello"
channel.queue_declare(queue='hello', durable=True)
# Send a message to a default exchange
# routing_key = queue name. 
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()