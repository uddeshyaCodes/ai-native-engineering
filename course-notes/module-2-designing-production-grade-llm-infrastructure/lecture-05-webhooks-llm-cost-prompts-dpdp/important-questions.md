# Lecture 05: Important Exam Q&A

Practice questions aligned with lecture emphasis and in-class quizzes. Answers are concise for revision.

---

## Webhooks and callbacks

### Q1. What is the difference between polling and a callback?

**A.** **Polling:** the client repeatedly asks the server for status. **Callback:** the client gives the server a URL and the server **pushes** the result when it is ready. Callbacks avoid wasted requests and waiting.

### Q2. Why must the callback URL be publicly reachable?

**A.** The server (or payment provider) sends the HTTP POST from outside. A localhost-only address cannot receive it.

### Q3. In the division demo, what does the main thread do and what does the child thread do?

**A.** The **main thread** stores the task as `processing` and returns the status at once. The **child thread** does the slow computation, then updates the task store to `success` or `failed` and POSTs to the callback URL if one was given.

### Q4. In the callback version, what changes on the client?

**A.** The client sends `callback_url` with the two numbers and runs a public endpoint (for example `/callback`) that receives the result. It refreshes once, instead of polling.

### Q5. Who creates the webhook/callback URL in the payment example?

**A.** The **client application** (the marketplace). It sends the URL to the payment provider, which later POSTs to it.

---

## Celery recap

### Q6. What does `.delay()` do, and what does `result.ready()` tell you?

**A.** `.delay()` enqueues the task on the broker and returns immediately. `ready()` returns `True` once the result is in the result backend.

---

## Cost instrumentation

### Q7. Which tokens are priced differently, and which fields in LiteLLM hold them?

**A.** **Input** (prompt) tokens and **output** (completion) tokens are priced separately. In LiteLLM: `response.usage.prompt_tokens` and `response.usage.completion_tokens`.

### Q8. Which LiteLLM function computes the cost of a response?

**A.** `completion_cost(completion_response=response)`.

### Q9. How do you make LiteLLM track cost on every call without asking each time?

**A.** Register a **success callback**, for example `litellm.success_callback = [track_cost]`. Each successful `completion()` triggers it.

### Q10. What does tiktoken do, and what does it not do?

**A.** It encodes text into tokens with a chosen encoding and counts them. It does **not** know model prices, so the developer computes cost.

### Q11. What are the three main Langfuse concepts used in the lecture?

**A.** **Trace** (a whole application run), **generation** (one LLM call), and the **`@observe`** decorator, which records a function's inputs, outputs and timing.

### Q12. Why should keys be stored in environment variables?

**A.** Hard-coded keys leak through source control. Libraries such as LiteLLM and Langfuse read them from the environment.

---

## Prompt versioning

### Q13. Why create a new version instead of editing the live prompt?

**A.** Editing in place changes behaviour for every live caller without a record. A new version keeps history, allows comparison, and lets you roll back by moving the production label.

### Q14. What is the production label for?

**A.** It marks the version that `get_prompt(name)` returns by default, so live apps use a tested version without a code change.

### Q15. How do you fetch a specific prompt version in Python?

**A.** `get_prompt(name, version=N)`; use `label="latest"` for the newest version, or no label for the production version.

### Q16. What do variables like `{{topic}}` do?

**A.** They are placeholders. `prompt.compile(topic="back propagation")` replaces them to build the final text.

---

## Evaluation

### Q17. What three inputs does an LLM-as-judge evaluator need?

**A.** The **input** (question or topic), the **expected output** (ground truth from the dataset) and the **actual output** (the model's answer under test).

### Q18. What does the dataset contain, and why is it needed?

**A.** Test inputs with expected outputs. Without ground truth, a judge has nothing to compare against.

### Q19. What is an experiment in Langfuse?

**A.** Running a chosen prompt version, on a chosen model, over a dataset, scored by an evaluator. You get a score per item and an average per version.

### Q20. Name one risk of trusting a single LLM judge.

**A.** It can be biased or inconsistent. Re-run, use a clear rubric, and spot-check a sample of scores.

---

## DPDP Act and PII

### Q21. Who are the Data Principal and the Data Fiduciary?

**A.** The **Data Principal** is the person whose data is collected. The **Data Fiduciary** is the entity that decides how and why the data is processed.

### Q22. What does data minimisation mean under the DPDP framing in the lecture?

**A.** Collect only data that is strictly necessary for the stated purpose, not data that “might be useful later”.

### Q23. What must happen when a Principal withdraws consent?

**A.** The Fiduciary must stop processing their data for that purpose and let them opt out of the collection.

### Q24. What are the obligations for children's data?

**A.** Verifiable parental consent first; no tracking, behavioural monitoring, profiling or targeted advertising aimed at children.

### Q25. What must a Fiduciary do after a breach?

**A.** Inform the Data Protection Board without delay and affected Principals; file a detailed report within 72 hours; isolate the affected system immediately.

### Q26. What is the difference between Presidio's analyzer and anonymizer?

**A.** The **analyzer** detects PII and returns entity type, position and confidence. The **anonymizer** replaces the detected text with a placeholder, random value, mask or encrypted value.

### Q27. Why anonymise text before sending it to an LLM?

**A.** So the external provider never sees the raw personal data. The model still gets enough context to do the task.

### Q28. How do you detect an entity Presidio does not recognise?

**A.** Write a regex, wrap it in a `Pattern` with a score, build a `PatternRecognizer`, and add it to the analyzer's registry.
