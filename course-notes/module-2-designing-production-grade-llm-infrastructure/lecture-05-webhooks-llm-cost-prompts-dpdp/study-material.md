# Lecture 05: Webhooks and Callbacks, LLM Cost Instrumentation, Prompt Versioning, DPDP Act, and PII Anonymisation

**Course:** AI-Enabled Software Engineering · **Module 2:** Designing Production-Grade LLM Infrastructure  
**Instructor:** Professor, CSE, IIT Kharagpur (name garbled in the transcript)  
**TA / demos:** Salma (Celery, webhooks), Dipanita (LiteLLM, Langfuse tracing), Taranum (Langfuse prompts and evals)  
**Running example:** Generic demos - a two-number division service, a marketplace payment flow, `x² + y²` Celery task, an admission assistant and an order-support chatbot. No KaryaSetu code this session.  
**Workshop path:** none for this lecture (related Celery/RabbitMQ material is in `workshops/11-celery-rabbitmq/`)

> **Transcript note:** Source is an auto-captioned WebVTT file (`lecture-05-webhooks-llm-cost-prompts-dpdp.txt`) with many mis-hearings. Read “wave book / web book” as **webhook**, “call back” as **callback**, “salary” as **Celery**, “Light LLM / Lite LLM” as **LiteLLM**, “Lang Fuse / line fuse / land fuse” as **Langfuse**, “tick token” as **tiktoken**, “Presidio” as **Microsoft Presidio**, “DPTP / DPDP” as **DPDP Act 2023**, “Anumerizer / ionimize” as **anonymizer**, “Polish phone number” as the **Polish phone number** example. Where the lecturer gives a number that is clearly garbled (for example the DPDP penalty), the notes use the figure from the Act itself and say so.

---

## Learning outcomes (exam-ready)

By the end of this session you should be able to:

- Explain **polling vs callback (webhook)** and why callbacks reduce wasted requests.
- Build a minimal **Flask** server that accepts a job with an optional callback URL, runs it in a **thread**, and posts the result back.
- Recall the **Celery** flow from the previous lecture: `.delay()`, broker, worker, result backend, `AsyncResult`.
- Count tokens with **tiktoken**, estimate cost from input and output prices per million tokens, and state the difference between input and output tokens.
- Use **LiteLLM** `completion()`, read `usage.prompt_tokens` and `usage.completion_tokens`, call `completion_cost()`, and register a **success callback** to track cost automatically.
- Explain **Langfuse** concepts: trace, generation, `@observe` decorator, and why it complements LiteLLM.
- Manage **prompts as versioned assets** in Langfuse: create a prompt, add versions, set a production label, fetch by name with `latest`, a version number, or the default production version, and compile variables.
- Build an **evaluation loop**: dataset (inputs and expected outputs), LLM-as-a-judge evaluator with a judge prompt, field mapping, and experiment scores per version.
- Summarise the **DPDP Act 2023** roles (Data Principal, Data Fiduciary), consent, data minimisation, children's data, and breach obligations.
- Use **Microsoft Presidio** to detect and anonymise PII before sending text to an LLM, and add a **custom regex recogniser** for an unknown entity.

---

## Session map

| Block | Topic | Demo |
|-------|-------|------|
| **1 - Webhooks and callbacks** | Payment-gateway analogy; polling vs callback | Salma: Celery + Redis recap, then Flask division service, polling client vs callback client |
| **2 - Cost instrumentation** | tiktoken, LiteLLM, Langfuse tracing | Dipanita: tiktoken budget check, LiteLLM usage and cost, Langfuse traces |
| **3 - Prompt versioning and evals** | Langfuse prompt management, playground, datasets, LLM-as-judge | Taranum: prompt v1 and v2, dataset, judge, experiment |
| **4 - DPDP Act and PII** | Consent, minimisation, breach rules; Presidio anonymiser and custom recogniser | Presidio examples in class (not a live demo) |

---

## Part 1: Polling vs callbacks (webhooks)

### The motivating example: a marketplace payment

1. Customer chooses a product. The marketplace (application) asks a **payment provider** for a payment ID or URL.
2. The customer pays on the provider's hosted form. The application is not involved in the payment itself.
3. The application must learn the outcome (success or failure) before it fulfils the order.

### Polling (the naive way)

- The application repeatedly asks the provider “is it paid yet?”
- **Costs:** wasted requests, load on both sides, unknown wait time, and the application stays busy checking.

### Callback / webhook (the better way)

- When creating the payment, the application sends a **callback URL**: a public endpoint it controls.
- The provider **pushes** the result to that URL as soon as the event happens.
- The application does other work in the meantime and only reacts when the push arrives.

| | Polling | Callback (webhook) |
|---|---------|--------------------|
| Who initiates | Client asks repeatedly | Server pushes once, on the event |
| Waste | Many empty requests | None |
| Latency | Up to one polling interval | Near-immediate |
| Requirement | Nothing extra | The callback URL must be **publicly reachable** |

> **Webhook vs callback:** the lecturer treats them as the same concept; “webhook” is the name when the callback is over HTTP.

### Demo: division service (Flask)

Architecture: client form (two numbers + optional callback URL) → server stores a task ID with status `processing` → a **child thread** does the slow work → server updates the task store to `success` or `failed` → if a callback URL was supplied, server **POSTs** the status to it.

| Piece | Polling version | Callback version |
|-------|-----------------|------------------|
| Client sends | `n1`, `n2` | `n1`, `n2`, `callback_url` |
| Server response | Current status (`processing`) | Current status (`processing`) |
| Result delivery | Client refreshes and calls the status endpoint | Server POSTs to client's callback endpoint; client refreshes once |
| Client needs | Nothing extra | A public endpoint at `/callback` |

Key points from the demo:

- The **main thread** returns the status immediately. The child thread does the computation.
- A **task repository** (a dict keyed by task ID) holds `status` and `result`.
- With no callback, the server only updates the repository; the client must poll.
- With a callback, the client must be reachable from the server, so the callback endpoint has to be public (or tunnelled).

### Celery recap (from lecture 4)

- `task.delay(x, y)` enqueues to the **broker** (Redis here) and returns at once.
- A **worker** (`celery -A task worker`) dequeues and runs the function.
- With a **result backend** set, `result = task.delay(...)`, then `result.ready()` returns `True` or `False` and `result.get()` returns the value.
- The demo used Redis at `localhost` as broker and backend.

---

## Part 2: LLM cost instrumentation

### Terminology

| Term | Meaning |
|------|---------|
| **Prompt** | Text sent to the model |
| **Token** | Small piece of text (roughly ¾ of an English word) |
| **Input tokens** | Tokens in the prompt |
| **Output tokens** | Tokens the model generates; usually priced higher |
| **Pricing** | Often quoted per **million** tokens, separately for input and output |

Cost formula used in class:

```
cost = (input_tokens / 1_000_000) × input_price_per_M
     + (output_tokens / 1_000_000) × output_price_per_M
```

### Tool 1: tiktoken (basic, manual)

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")   # vocabulary / encoding scheme
tokens = enc.encode(prompt)                  # list of token IDs
n = len(tokens)
```

- Counts tokens only; **you** supply prices and compute cost.
- Dipanita's demo added a **budget check**: `if total_cost <= budget: "affordable"`.
- Note that the encoding must match the model family, or counts will be off.

### Tool 2: LiteLLM (one interface, automatic usage and cost)

LiteLLM provides a single `completion()` call for many providers (OpenAI, Anthropic, and others). Keys are read from **environment variables**, not hard-coded.

```python
from litellm import completion, completion_cost
response = completion(
    model="claude-sonnet-5-5",          # provider/model name as configured
    messages=[{"role": "user", "content": "Explain binary search trees"}],
    max_tokens=200,                     # cap spend
)
response.choices[0].message.content
response.usage.prompt_tokens           # input tokens
response.usage.completion_tokens       # output tokens
response.usage.total_tokens
completion_cost(completion_response=response)   # cost computed for you
```

- **`prompt_tokens` = input, `completion_tokens` = output.** The lecturer stressed this distinction.
- `completion_cost()` looks up the model's prices, so you do not supply them.

#### Automatic tracking with a success callback

```python
import litellm

def track_cost(kwargs, completion_response, start_time, end_time):
    cost = litellm.completion_cost(completion_response=completion_response)
    print("cost:", cost)

litellm.success_callback = [track_cost]    # registered once
```

Every successful `completion()` now triggers `track_cost` automatically. This is the callback pattern from Part 1, applied to LLM calls: you do not poll for the cost.

### Tool 3: Langfuse (observability platform)

Langfuse is an open-source platform (cloud or self-hosted) to observe LLM applications. It gives a dashboard for traces, generations, token counts, cost and latency.

| Term | Meaning |
|------|---------|
| **Trace** | One end-to-end run of an application (for example one chatbot session) |
| **Generation** | One LLM call inside a trace (one query) |
| **Span** | Any timed step within a trace |

**Setup:** create an account and project, then create an API key set: **public key**, **secret key** and **host URL**. Store them as environment variables (`LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST`). Check the connection with `get_client().auth_check()`.

#### Option A: LiteLLM sends to Langfuse

```python
import litellm
litellm.success_callback = ["langfuse"]
# then call completion() as usual; each call appears as a trace/generation
```

#### Option B: `@observe` decorator

```python
from langfuse import observe
from litellm import completion

@observe()
def admission_assistant(question: str):
    r = completion(model="...", messages=[{"role": "user", "content": question}], max_tokens=300)
    return r.choices[0].message.content
```

The decorator records the function's start and end time, its arguments and its output as a trace, with the LLM cost attached by the nested completion call.

#### Option C: Direct Anthropic call with manual Langfuse updates

For a non-LiteLLM client, you create the Langfuse record yourself, call the model, then update the record with the output and `usage` (input and output tokens). This gives full control at the cost of more code. The order-support demo used this to log eight queries in a loop, each as its own entry.

### Cost-tool comparison (as summarised in class)

| Tool | Count tokens | Cost | Dashboard | Effort |
|------|:------------:|:----:|:---------:|--------|
| tiktoken | Yes | You compute | No | Lowest |
| LiteLLM | Yes | Automatic | No (unless wired to Langfuse) | Medium |
| Langfuse | Yes (via integration) | Yes | **Yes** | Highest, most features |

---

## Part 3: Prompt versioning and evaluation (Langfuse)

### Prompts as managed assets

A prompt has **fixed text** (for example "You are a deep learning tutor") and **variables** (for example `{{topic}}`). Compiling the prompt replaces the variables with values.

Langfuse prompt management workflow:

1. **Create** a prompt with a name, text and commit message. This becomes **version 1**.
2. **Add a version** by editing the text. Editing never changes an existing version; each save creates a new version. Example: v2 adds “explain in 120 words”, v3 adds more constraints.
3. **Set a label** such as **production** on the version that live apps should use. The default fetch returns the production version.
4. **Test** a version in the **playground**: fill variables, pick a model, submit.

### Fetching prompts in code

```python
from langfuse import get_client
langfuse = get_client()

prompt = langfuse.get_prompt("movie-critic", label="latest")   # or version=2, or default (production)
text = prompt.compile(critic_level="expert", movie="Inception")
# send text to the model as the system or user message
```

| Way to fetch | Returns |
|--------------|---------|
| `label="latest"` | Newest version |
| `version=2` | That exact version |
| no label | The **production** version (safe default for live apps) |

### Evaluation: dataset + judge + experiment

| Part | What it is | Example in class |
|------|-----------|------------------|
| **Dataset** | Test inputs and **expected** (ground-truth) outputs, usually a CSV | 10 topics (back-propagation, overfitting, loss functions, CNN) with textbook answers |
| **Prompt version** | The version under test | Deep learning tutor v2 vs v3 |
| **Evaluator (LLM-as-judge)** | A separate model that scores each answer against the expected answer | Judge prompt: “You are an expert QA judge… score 0 to 1 and justify” |
| **Variable mapping** | Tells Langfuse which dataset column is the input, expected output and actual output | `input = topic`, `expected_output = answer`, `output = model response` |
| **Experiment** | Runs a prompt version on the dataset with a judge | Scores per item and an average per version |

Steps (from the lecture):

1. Create the dataset (name it; upload CSV with `input` and `expected_output`).
2. Create an **LLM-as-a-judge** evaluator: pick the judge model, write the judge prompt, set the score range, map the three fields. Keep the judge prompt strict and the score range explicit.
3. Run an **experiment**: choose the prompt version, model, dataset and evaluator. Compare average scores across versions.

Conclusion from the demo: version 3 (word-limited) scored better than version 2, judged by the LLM judge against ground truth. Caveat: a single judge model can be biased or inconsistent, so re-run and spot-check scores, as the earlier lecture advised for non-deterministic models.

---

## Part 4: DPDP Act 2023 (privacy basics)

Indian **Digital Personal Data Protection Act, 2023** (DPDP). High-level points from the lecture, with the Act's own terms:

| Concept | Meaning |
|---------|---------|
| **Data Principal** | The person whose data is collected (the “owner” in the lecture) |
| **Data Fiduciary** | The entity that decides how and why data is processed (the “custodian”) |
| **Notice** | Before collecting data, give a clear, itemised notice: what data, why, and where it is used. It can be in several languages |
| **Consent** | Free, specific, informed and unambiguous; not forced; can be **withdrawn** at any time |
| **Data minimisation** | Collect only what is strictly necessary; do not collect “just in case” |
| **Storage limitation** | Delete or anonymise once the purpose is done |
| **Sensitive data** | Name and email are lower risk. Identity documents, financial data, health, biometric data need stronger safeguards: strong encryption and tight access control |
| **Children (under 18)** | Verifiable parental consent; no tracking, behavioural monitoring or targeted advertising aimed at children |
| **Processors** | A Data Fiduciary stays responsible for any third-party processor it uses |
| **Breach** | Inform the Data Protection Board **without delay** and affected Principals; a detailed report follows within **72 hours** (lecturer said "within 72 hours"). The lecturer said isolate the system immediately |
| **Penalty** | Up to ₹250 crore for failing to take reasonable security safeguards (the lecturer's figure was garbled; this is the Act's maximum for that offence) |

> The lecture says the Act came in 2023 and the “2023 Indian government enforced it”. Treat the timeline as the lecturer's framing and check the official text before relying on any figure.

---

## Part 5: PII anonymisation with Microsoft Presidio

### Why

Text sent to an external LLM can contain names, phone numbers and account numbers. Anonymise it first, so the provider never sees the raw values.

### Analyzer and anonymizer

| Component | Role |
|-----------|------|
| **AnalyzerEngine** | Detects PII: returns entity type, position and confidence score |
| **AnonymizerEngine** | Replaces the detected spans (placeholder, random value, mask, encrypt) |

```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
results = analyzer.analyze(text=text, language="en")
out = anonymizer.anonymize(text=text, analyzer_results=results)
out.text
```

- Anonymiser replacements can be **placeholders** (`<PERSON>`), **random values**, **masks** or **encryption**.
- You can limit which entities to anonymise (the lecture showed names and phone numbers only).

### Using it with an LLM (LangChain chain)

The demo built a chain that runs in this order:

1. Anonymise the input text.
2. Fill a prompt template (“rewrite this text into an official short email”) with the anonymised text.
3. Send the prompt to the chat model.

```text
chain = anonymize  |  prompt_template  |  llm
chain.invoke({"text": raw_text})
```

Nothing runs until `invoke()` is called. The model sees only the anonymised text.

### Custom recogniser for unknown PII

Presidio does not know every format. For a **Polish phone number**, write a regex, wrap it in a `Pattern` with a name and score, make a `PatternRecognizer`, then add it:

```python
from presidio_analyzer import Pattern, PatternRecognizer
polish = PatternRecognizer(supported_entity="POLISH_PHONE",
                           patterns=[Pattern("polish_phone", r"\+48\s?\d{3}[\s-]?\d{3}[\s-]?\d{3}", 0.5)])
analyzer.registry.add_recognizer(polish)
```

Matches become `<POLISH_PHONE>`; non-matching numbers are handled as usual. The **score** tells Presidio how confident to be in a match.

Note: `AnonymizerEngine` can also be made **reversible** (the lecturer skipped this for time) so that replaced values can be restored later.

---

## Key takeaways

1. **Callbacks push, polling pulls.** Use a callback when the event is slow and you cannot predict when it ends; the receiver must expose a public endpoint.
2. **Cost = tokens × price**, and **input and output are priced separately**. `prompt_tokens` vs `completion_tokens` in LiteLLM is the main thing to remember.
3. **LiteLLM callbacks and Langfuse `@observe`** turn cost and tracing into automatic side effects, not manual logging.
4. **Prompts are versioned assets.** Never edit a live version in place; create a new version and move the production label deliberately.
5. **Evaluate before you promote.** A dataset with expected outputs, an LLM judge, and experiment scores let you compare versions with numbers.
6. **Minimise and protect personal data** (DPDP): consent, minimisation, storage limits, child safeguards, breach reporting.
7. **Anonymise PII before the model call** with Presidio, and add custom recognisers for local formats.
