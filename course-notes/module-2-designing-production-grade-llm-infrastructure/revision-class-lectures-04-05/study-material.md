# Revision Class: Celery, RabbitMQ, Webhooks, and an Integrated Project (Lectures 04 and 05)

**Course:** AI-Enabled Software Engineering · **Module 2:** Designing Production-Grade LLM Infrastructure  
**Instructor:** Professor, CSE, IIT Kharagpur (name garbled in the transcript)  
**Demos:** Salma  
**Running example:** A FastAPI service that accepts a document (PDF, scanned image or PAN/Aadhaar card), extracts and OCRs it in a background worker, optionally anonymises sensitive fields, and notifies the client through a callback.  
**Workshop path:** `workshops/11-celery-rabbitmq/` (`Celery_Redis/`, `RabbitMQ/`, `Webhook_Callback/`)

> **Transcript note:** Source is an auto-captioned transcript (`revision-class-lectures-04-05.txt`) with many mis-hearings. Read “salary” as **Celery**, “wave hook / web hoops” as **webhook**, “rabid MQ / Ravi NQ / gravity in queue” as **RabbitMQ**, “Pica” as **pika**, “Reddis / radius” as **Redis**, “Fiat dispatch” as **fair dispatch**, “Azar / other card” as **Aadhaar card**. The lecturer also describes the Celery result store as living "inside the task queue"; in Celery it is a separate **result backend** that you configure (the demo happened to use the same Redis server for both).

---

## Learning outcomes (exam-ready)

By the end of this session you should be able to:

- Explain why a synchronous upload-and-process endpoint does not scale, and how a producer, broker and worker split the load.
- Recall the three Celery components and the difference between a call with and without `.delay()`.
- Explain why a result backend is needed for `result.get()` and `result.ready()`.
- Describe the RabbitMQ model: producer, exchange, queue, consumer (and where the default exchange fits).
- Compare **round-robin** dispatch (default) with **fair dispatch** (`basic_qos(prefetch_count=1)`).
- Explain **acknowledgements**: auto-ack versus manual `basic_ack`, and what happens when a consumer dies mid-task.
- Explain **durability**: a durable queue survives a broker restart; persistent messages (`delivery_mode=2`) survive too.
- Describe the integrated project pipeline and where webhook callbacks, Celery workers, OCR and anonymisation sit.

---

## Session map

| Block | Topic | Demo |
|-------|-------|------|
| **1 - Motivation** | Synchronous processing bottleneck; why offload to a second server | Slides only |
| **2 - Celery recap** | Producer / broker / worker; `.delay()`; result retrieval | Salma: Celery with Redis, with and without `.delay()`, with `backend` set |
| **3 - RabbitMQ** | Hello World, round robin, fair dispatch, acks, durability | Salma: `send` / `worker` / `new_task` with dot-based sleep |
| **4 - Webhooks recap** | Payment analogy, polling vs callback | Polling vs callback division service |
| **5 - Integrated project** | FastAPI upload → Celery → OCR/extraction → optional anonymisation → callback | Salma: end-to-end ID card processing |

---

## Part 1: Why offload work

- A FastAPI endpoint that runs OCR and an LLM call inline blocks its request. At 1 user, 50 seconds may be tolerable. At thousands of concurrent users, the API server runs out of resources.
- **Fix:** split the system into two roles:
  - **API server (producer):** accepts the request, enqueues a job, returns a **task ID** immediately.
  - **Worker server (consumer):** dequeues jobs and does the heavy work.
  - **Broker / task queue** in between.
- Threads inside the API server are not enough: they share the same CPU and memory, so they do not scale across machines.

---

## Part 2: Celery recap

| Component | Role |
|-----------|------|
| **Producer** | The FastAPI app calling `task.delay(...)` |
| **Broker** | Holds queued messages (Redis or RabbitMQ) |
| **Worker** | `celery -A <module> worker`; runs tasks, one at a time per process |
| **Result backend** | Where return values are stored so the producer can read them |

Key calls:

```python
app = Celery("task", broker="redis://localhost:6379", backend="redis://localhost:6379")

@app.task
def process(x, y):
    ...
    return x**2 + y**2

process(2, 3)            # runs inline in the calling process - blocks
r = process.delay(2, 3)  # enqueues and returns an AsyncResult at once
r.ready()                # True once the result is in the backend
r.get(timeout=30)        # waits for and returns the value
r.status                 # e.g. PENDING, SUCCESS, FAILURE
```

- Without `backend=`, `r.get()` cannot work; the demo showed this with the backend line commented out in `Celery_Redis/task.py`.
- The demo's `process` task sleeps to simulate heavy work, so `delay()` returns while the worker is still running.

---

## Part 3: RabbitMQ

### Model

```
producer -> exchange -> queue -> consumer (worker)
```

- **Default exchange:** an empty-name exchange. Its routing key is the **queue name**, so `basic_publish(exchange='', routing_key='hello', ...)` delivers to queue `hello`.
- **Queue:** holds messages until a consumer acknowledges them.
- Multiple consumers can subscribe to one queue; messages are shared between them.

### Minimal code (pika)

```python
# producer
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='hello')
channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
connection.close()

# consumer
def callback(ch, method, properties, body):
    print(body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)   # manual ack

channel.basic_consume(queue='hello', on_message_callback=callback)  # auto_ack defaults to False
channel.start_consuming()
```

The demo's consumer sleeps for one second per dot in the message (`time.sleep(body.count(b'.'))`), so you can make "heavy" and "light" tasks by typing `Hello..` or `Hi.`.

### Round robin (default)

- With no extra settings, RabbitMQ hands messages to consumers in turn, without checking how busy they are.
- Example with two workers and four tasks (heavy, light, heavy, light): worker 1 gets tasks 1 and 3, worker 2 gets tasks 2 and 4. If task 1 and 3 are heavy, worker 2 sits idle while worker 1 is overloaded.
- Auto-acknowledgement (`auto_ack=True`) is the usual pairing with round robin in the demo. Note the lecturer's point: the message is acknowledged as soon as it is delivered, so a crash during processing loses it.

### Fair dispatch

```python
channel.basic_qos(prefetch_count=1)                          # one unacked message per worker
channel.basic_consume(queue='hello', on_message_callback=callback)  # no auto_ack
```

- `prefetch_count=1` means a worker is given a new message only after it acknowledges the previous one.
- Result in the demo: the free worker takes the next task, so load goes to whoever is idle.
- Two changes from round robin: add `basic_qos(prefetch_count=1)` and use **manual** `basic_ack`.

### Acknowledgements and reliability

| Situation | What RabbitMQ does |
|-----------|-------------------|
| Consumer acks the message | Message removed from the queue |
| Consumer dies before acking | Message is requeued and given to another consumer |
| Consumer uses auto-ack and dies mid-task | Message is already gone; the task is lost |

### Durability (survives a broker restart)

Two separate settings:

| Setting | Survives |
|---------|----------|
| `queue_declare(queue=..., durable=True)` | The **queue** itself after a broker restart |
| `basic_publish(..., properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent))` | The **messages** in that queue |

Both are needed. The demo showed a queue with pending messages surviving a `rabbitmq-server` stop and restart, and a worker receiving them afterwards.

> **Gotcha:** a queue must be declared with the same `durable` flag by every script that uses it. In this workshop, `send.py` and `receive.py` use `durable=True`, while `worker.py` and `new_task.py` do not. Mixing them makes RabbitMQ refuse the declaration (`PRECONDITION_FAILED`). Delete the queue in the management UI (http://localhost:15672) and use one style throughout.

### Workshop vs lecture: what the files actually do

| File | Dispatch | Ack | Durable |
|------|----------|-----|---------|
| `RabbitMQ/send.py` | — | — | `hello` durable |
| `RabbitMQ/receive.py` | Round robin | `auto_ack=True` | `hello` durable |
| `RabbitMQ/worker.py` | Round robin (QoS line commented out) | Manual `basic_ack` | `hello` not durable |
| `RabbitMQ/new_task.py` | — | — | `hello` not durable; dots from the command line |

To reproduce fair dispatch from the lecture, uncomment `channel.basic_qos(prefetch_count=1)` in `worker.py`. Then make the queue durable everywhere if you want to test durability.

> These examples use **pika** directly, not Celery. The lecturer said "we'll see RabbitMQ" as a broker; the RabbitMQ demos in this session are raw message-queue code, not `celery -A ... --broker=amqp://...`.

---

## Part 4: Webhooks and callbacks (recap)

Covered in full in lecture 05 study material. Recap points from this session:

- **Polling:** client calls `GET /task/<id>` repeatedly. Wasteful, and the client doesn't know when the result will arrive.
- **Callback:** client sends a public `callback_url` with the request. Server `POST`s the result when ready. Client refreshes once.
- The division demo in this session uses a server that sleeps 5 to 15 seconds at random, then either updates a task dict (polling) or POSTs to `callback_url` (callback).
- The workshop's `Webhook_Callback/` folder has `server.py` (Flask on port 5000), `client.py` (polling, port 5001), and `client2.py` (callback, adds `/callback`).

---

## Part 5: Integrated project

Pipeline the lecturer described:

1. **Upload:** client uploads an image or PDF and a public `callback_url` to a FastAPI endpoint.
2. **Enqueue:** the endpoint calls a Celery task with `.delay()` and returns a **job ID** immediately.
3. **Worker:** the Celery worker extracts text and tables (pdfplumber / PyMuPDF), runs OCR where needed (Tesseract or a vision model), and optionally anonymises sensitive fields with Presidio.
4. **Result:** the worker stores the output in the result backend and POSTs it to `callback_url`.
5. **Retrieve:** the client calls the job endpoint with the job ID to fetch the full or anonymised result. The demo showed two modes: "show all fields" and "anonymised fields" (for example, the document number replaced by a placeholder).

Where each earlier topic fits:

| Stage | Topic from earlier notes |
|-------|--------------------------|
| Extract text, tables | Lecture 04 Part 1 (pypdf / pdfplumber / PyMuPDF) |
| OCR | Lecture 04 Part 2 and 3 |
| Queue and worker | Lecture 04 Part 4; this session Part 2 and 3 |
| Callback | Lecture 05 Part 1; this session Part 4 |
| Anonymise | Lecture 05 Part 5 (Presidio) |

The lecturer's wrap-up: the design lets one API server accept many uploads while workers scale out, and the client never waits for the heavy job.

---

## Key takeaways

1. **Producer returns quickly; workers do the heavy work.** That is the whole point of Celery and of the RabbitMQ setup.
2. **Celery needs a result backend** before `get()` or `ready()` can return anything.
3. **Round robin is the default** in RabbitMQ and ignores worker load. **Fair dispatch** (`prefetch_count=1`, manual ack) sends work to whichever worker is free.
4. **Manual acks protect against lost work.** An unacked message goes to another consumer when one dies.
5. **Durability needs both a durable queue and persistent messages.**
6. **Design the flow once:** enqueue, return a job ID, process in the background, notify by callback, fetch the result by job ID.
