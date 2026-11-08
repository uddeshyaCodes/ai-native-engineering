# Revision Class: Self-Check Questions

The transcript does not contain in-session poll questions, so these are self-check questions drawn from the topics covered. Answers are in the study material and important questions.

---

## Quick check

| Claim | True / False |
|-------|----------------|
| `process(2, 3)` returns immediately because Celery runs it in the background | **False** - without `.delay()` it runs inline |
| A Celery `result.get()` works with a broker but no result backend | **False** |
| Round robin is the default RabbitMQ dispatch | **True** |
| `basic_qos(prefetch_count=1)` alone is enough to get fair dispatch | **False** - manual ack is also needed |
| With auto-ack, a worker crash mid-task keeps the message for another worker | **False** - the message is already acknowledged |
| A durable queue alone keeps pending messages after a broker restart | **False** - messages also need `delivery_mode=Persistent` |
| The default exchange routes by queue name | **True** |
| `auto_ack=True` in `receive.py` in the workshop means fair dispatch | **False** - that pairing is for round robin |

---

## Scenario questions

1. Two workers, tasks A (heavy), B (light), C (light), D (light) arrive in order. Under round robin, which worker gets C? Under fair dispatch with prefetch 1, which worker is likely to get C?
   - **Answer:** Round robin: worker 1 gets A and C. Fair dispatch: whichever worker finishes B first gets C, usually the worker that did not get A.

2. A worker runs with `auto_ack=True`, takes a message, and is killed halfway through. What happens to the message?
   - **Answer:** It is lost, because it was acknowledged on delivery.

3. You restart RabbitMQ. Your queue is durable, but the messages disappear. What did you miss?
   - **Answer:** The messages were not published with `delivery_mode=Persistent`.

4. A client never gets a callback and the job shows PENDING. List two things to check.
   - **Answer:** The worker is running and consuming from the right queue or broker; the `callback_url` is public and reachable from the worker; the task used the same broker and backend as the producer.
