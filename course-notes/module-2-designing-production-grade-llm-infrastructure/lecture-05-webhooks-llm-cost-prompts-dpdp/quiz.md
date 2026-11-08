# Lecture 05: In-Lecture Quizzes

Live polls were run after the callback demo, after the cost tools, after the prompt and evaluation demos, and after the Presidio section. Stems follow the instructor's readout; the transcript is partly garbled, so the wording is best-effort.

---

## Quiz 1 - After webhooks and callbacks

### Q1. Who creates the webhook (callback) URL in the payment example?

| | |
|---|---|
| **Correct ✓** | **The client application** (it sends the URL to the provider) |

**Explanation:** The provider does not invent the URL; it posts to the URL the application supplied.

---

## Quiz 2 - After Celery recap and cost tools

### Q2. Which LiteLLM function computes the cost of a completion?

| | |
|---|---|
| **Correct ✓** | **`completion_cost`** |

**Live note:** Most respondents picked the completion-cost function.

---

## Quiz 3 - After prompt versioning

### Q3. What is the primary entity in Langfuse that holds and versions prompts?

| | |
|---|---|
| **Correct ✓** | **A prompt repository** (named prompts, each with versions) |

---

### Q4. Which SDK method retrieves a prompt in Python?

| | |
|---|---|
| **Correct ✓** | **`get_prompt`** on the Langfuse client |

---

## Quiz 4 - After Presidio

### Q5. What is the primary purpose of sensitivity analysis when evaluating an AI/ML model?

| | |
|---|---|
| **Correct concept ✓** | To examine **how changes in the input affect the output** and performance, so you know which inputs the model is sensitive to |

**Note:** The lecture's question wording was ambiguous; the answer above is the lecturer's accepted reading.

---

### Q6. Which Presidio component detects PII and returns entity type, position and confidence?

| | |
|---|---|
| **Correct ✓** | **The analyzer** (not the anonymizer) |

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
