# Revision Class: Important Exam Q&A

Practice questions for the revision session on Celery, RabbitMQ, webhooks and the integrated project. Answers are concise.

---

## Motivation and architecture

### Q1. Why does a synchronous endpoint that runs OCR inline fail at scale?

**A.** Each request holds the API server while the heavy work runs. At thousands of concurrent users, the server runs out of resources, requests queue up, and the server can crash.

### Q2. Why are threads inside the API server not enough?

**A.** Threads share the same CPU, memory and hardware, so they cannot scale across machines the way separate workers can.

### Q3. Name the three roles in an asynchronous task system.

**A.** **Producer** (API server that enqueues), **broker / task queue** (holds messages), **consumer / worker** (executes tasks).

---

## Celery

### Q4. What does `task.delay(x, y)` do compared with `task(x, y)`?

**A.** `delay()` enqueues the task on the broker and returns an `AsyncResult` immediately. Calling `task(x, y)` runs it inline in the calling process.

### Q5. Why does `result.get()` need a result backend?

**A.** The worker's return value must be stored somewhere the producer can read it. Without `backend=` configured, there is nowhere to store it.

### Q6. What does `result.ready()` tell you?

**A.** Whether the task has finished and its result is available in the backend.

### Q7. Is the Celery result store the same thing as the broker?

**A.** No. The broker carries messages; the result backend stores return values. The demo used one Redis server for both, which can make them look like one thing.

---

## RabbitMQ

### Q8. What is the default exchange, and what is its routing key?

**A.** The default exchange has the empty name `''`. Its routing key is the queue name, so `basic_publish(exchange='', routing_key='hello')` delivers to the queue `hello`.

### Q9. What is round-robin dispatch, and when is it the default?

**A.** RabbitMQ hands messages to consumers in turn without checking their load. It is the default when no QoS setting is used.

### Q10. With two workers and tasks 1 to 4 (heavy, light, heavy, light), which worker gets which task under round robin?

**A.** Worker 1 gets tasks 1 and 3 (both heavy); worker 2 gets tasks 2 and 4. Worker 2 can sit idle while worker 1 is overloaded.

### Q11. What does `channel.basic_qos(prefetch_count=1)` do?

**A.** It limits each consumer to one unacknowledged message at a time, so a busy worker is not given more work. This is the setting that turns on fair dispatch.

### Q12. Which two changes turn round robin into fair dispatch?

**A.** Add `basic_qos(prefetch_count=1)` and use manual acknowledgement (`auto_ack=False` with `basic_ack`).

### Q13. What is the difference between auto-ack and manual ack?

**A.** Auto-ack marks the message done as soon as it is delivered. Manual ack marks it done only after the consumer calls `basic_ack`, so an unacked message can be redelivered if the consumer dies.

### Q14. What happens if a consumer dies while processing a message with manual ack?

**A.** RabbitMQ requeues the message and delivers it to another consumer.

### Q15. What is the risk of auto-ack for heavy tasks?

**A.** If the worker crashes during processing, the message is already acknowledged and is lost.

### Q16. What two settings make messages survive a RabbitMQ restart?

**A.** `queue_declare(..., durable=True)` makes the queue survive; `delivery_mode=pika.DeliveryMode.Persistent` makes the messages survive. Both are needed.

### Q17. Why must every script declare a queue with the same `durable` flag?

**A.** RabbitMQ refuses a redeclaration with different settings (`PRECONDITION_FAILED`). The workshop's `send.py` and `receive.py` are durable while `worker.py` and `new_task.py` are not, so mixing them causes this error.

---

## Webhooks and the project

### Q18. What is the main difference between polling and a callback?

**A.** Polling makes the client ask repeatedly. A callback makes the server push the result to a URL the client gave it, once the work is done.

### Q19. Why must a callback URL be public?

**A.** The server sends the POST from outside the client's machine, so the URL must be reachable from the server.

### Q20. In the integrated project, what does the client get back immediately after upload?

**A.** A job (task) ID. The processing runs in a Celery worker in the background.

### Q21. Where does anonymisation sit in the project pipeline?

**A.** Inside the worker, after extraction and OCR and before the result is returned or sent to the callback, so that anonymised fields are what leave the system.

### Q22. Which two output modes did the project demo show?

**A.** Full extracted fields, and anonymised fields where sensitive values such as the document number are replaced.
