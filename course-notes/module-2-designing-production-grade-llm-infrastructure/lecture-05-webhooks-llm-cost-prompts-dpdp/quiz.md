# Lecture 05: In-Lecture Quizzes

Live polls were run after the callback demo, after the cost tools, after the prompt and evaluation demos, and after the Presidio section. Questions and options below are taken verbatim from the Mentimeter deck "Session-2" (8 questions). **The deck has no answer-key slides**, so correct answers are deduced from the lecture notes; live-result notes come from the transcript where recorded.

---

## Quiz 1 - After webhooks and callbacks

### Q1. Who creates and registers the webhook URL?

**Stem:** Who creates and registers the Webhook URL in an integration?

| Option | |
|---|---|
| A | Created by the service provider and sent to the client |
| **B ✓** | **Created by the client and registered with the service provider** |
| C | Created jointly by both the client and service provider |
| D | None of the above |

**Explanation:** The provider does not invent the URL; it posts to the URL the application supplied.

---

### Q2. Polling vs webhooks

**Stem:** What is the fundamental operational difference between a standard REST API polling mechanism and a Webhook?

| Option | |
|---|---|
| A | Webhooks require the client to continuously ping the server for updates. |
| **B ✓** | **Webhooks push data from the source server to a target URL automatically when an event occurs.** |
| C | Standard REST APIs can only send data, while Webhooks can only receive data. |
| D | Webhooks rely private IP address |

**Explanation:** Polling = the client keeps asking; a webhook = the provider pushes when the event happens. A is backwards, and a webhook URL must be publicly reachable (not a private IP).

---

## Quiz 2 - After Celery recap and cost tools

### Q3. LiteLLM cost function

**Stem:** Which of the following functions does LiteLLM provide to help calculate the cost of a model call using its response object or token counts?

| Option | |
|---|---|
| **A ✓** | **litellm.completion_cost()** |
| B | litellm.compute_price() |
| C | litellm.calculate_bill() |
| D | litellm.get_token_fare() |

**Live note:** Most respondents picked the completion-cost function.

---

### Q4. DPDP Act maximum penalty

**Stem:** Under the DPDP Act 2023, what is the maximum monetary penalty that can be imposed on a Data Fiduciary for failing to implement reasonable security saf… *(stem truncated in the Menti deck; it continues "safeguards")*

| Option | |
|---|---|
| A | ₹50 Crore |
| B | ₹150 Crore |
| C | ₹200 Crore |
| **D ✓** | **₹250 Crore** |

**Explanation:** ₹250 crore is the Act's maximum for failing to take reasonable security safeguards. The lecturer's spoken figure was garbled in the transcript; this is the figure from the Act.

---

## Quiz 3 - After prompt versioning and evaluation

### Q5. Langfuse entity for versioning prompts

**Stem:** What primary entity in Langfuse allows developers to track, compare, and manage different iterations of system prompts over time?

| Option | |
|---|---|
| **A ✓** | **Prompt Repository / Version Management** |
| B | Vector Store Index |
| C | Secret Key Manager |
| D | Model Fine-Tuning Pipeline |

**Explanation:** Named prompts, each with numbered versions and labels (e.g. `production`, `latest`).

---

### Q6. Fetching a specific prompt version

**Stem:** When retrieving a prompt programmatically in your code using the Langfuse SDK, how do you fetch a specific non-production prompt version (e.g., versio… *(stem truncated in the Menti deck; presumably "version 3")*

| Option | |
|---|---|
| **A ✓** | **langfuse.get_prompt("my-prompt", version=3)** |
| B | langfuse.get_prompt("my-prompt", label="latest_v3") |
| C | langfuse.fetch_version("my-prompt", 3) |
| D | langfuse.checkout("my-prompt-v3") |

**Explanation:** `get_prompt(name, version=N)` fetches that exact version; `label="latest"` gives the newest version; no label returns the production version. `fetch_version` and `checkout` don't exist, and `latest_v3` is not a label Langfuse defines.

---

### Q7. Purpose of sensitivity analysis

**Stem:** What is the primary purpose of sensitivity analysis when evaluating the performance of an AI/ML model?

| Option | |
|---|---|
| A | To measure the total computational cost of training the model. |
| **B ✓** | **To examine how changes in input parameters affect the model's output or performance.** |
| C | To determine the number of layers required in a neural network. |
| D | To calculate the total number of training samples. |

**Note:** The lecture's question wording was ambiguous; this is the lecturer's accepted reading.

---

## Quiz 4 - After Presidio

### Q8. Presidio method that detects PII

**Stem:** Which Microsoft Presidio method detects PII and returns its entity type, position, and confidence score?

| Option | |
|---|---|
| A | AnonymizerEngine.anonymize() |
| **B ✓** | **AnalyzerEngine.analyze()** |
| C | RecognizerRegistry.add_recognizer() |
| D | PresidioReversibleAnonymizer.deanonymize() |

**Explanation:** The anonymizer replaces text; the analyzer finds it. The lecturer skipped the reversible anonymiser for time.

---

## Quick self-check

| Claim | True / False |
|-------|----------------|
| Polling is more efficient than a callback for a slow, unpredictable event | **False** |
| A callback URL can be `localhost` and still receive a provider's POST | **False** |
| `prompt_tokens` in LiteLLM counts the model's generated output | **False** - that is `completion_tokens` |
| Editing a live prompt version in place is the recommended way to change it | **False** - create a new version |
| `get_prompt` with no label returns the production version | **True** |
| An LLM judge needs the expected answer to score against ground truth | **True** |
| Presidio's anonymiser detects PII on its own | **False** - the analyzer detects; the anonymiser replaces |
| Under DPDP, a Fiduciary can keep data indefinitely "in case we need it later" | **False** - minimisation and storage limits apply |

---

## Summary

| Quiz | When | Questions | Main topics |
|------|------|-----------|-------------|
| **1** | After webhooks / callbacks | **2** | Who creates the webhook URL, polling vs webhook |
| **2** | After Celery recap / cost tools | **2** | `litellm.completion_cost()`, DPDP penalty |
| **3** | After prompt versioning / evals | **3** | Langfuse prompt repository, `get_prompt(version=)`, sensitivity analysis |
| **4** | After Presidio | **1** | `AnalyzerEngine.analyze()` |

**Total Menti questions:** **8** (2 + 2 + 3 + 1)

**Grouping note:** The deck is one flat list of 8 questions. The split into Quizzes 1-4 follows the order of the previous notes and the lecture flow, so the boundaries are approximate.
