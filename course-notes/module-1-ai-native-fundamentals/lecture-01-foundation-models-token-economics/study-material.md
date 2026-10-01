# Study Material — Module 1, Lecture 1: Foundation Models, Token Economics & AI Pair Programming

**Course:** Post Graduate Diploma in AI-Enabled Software Engineering (IIT Kharagpur)  
**Instructor:** Prof. Rajat Shukla Chakraborty (with TA Dr. Somposashi Mukhopadhyay)  
**Session:** First class — foundational sub-modules M1–M6 of Module 1

---

## Learning outcomes (end of session)

By the end of this lecture you should be able to:

- **Evaluate foundation models** on **cost, capability, and risk**
- **Estimate token usage and INR/API costs** for realistic workloads
- **Explain hallucinations**, calibration, and mitigation (prevent / detect / mitigate)
- **Compare AI coding tools** (Copilot, Cursor, Claude Code, Windsurf) and match them to roles
- **Apply disciplined AI pair programming** (Spec → Verify → Override), not “prompt-copy-ship”
- **Apply a build vs. buy / AI vs. traditional logic** decision framework

---



## Session map (six sub-modules)


| Sub-module | Topic                                           |
| ---------- | ----------------------------------------------- |
| **M1**     | Foundation model ecosystem & decision framework |
| **M2**     | Token economics (INR examples, TCO)             |
| **M3**     | AI failure modes: hallucination & calibration   |
| **M4**     | AI-augmented development tooling                |
| **M5**     | Structured AI pair programming                  |
| **M6**     | Build vs. buy decision framework                |


**In-class activities:** Mentimeter Quiz 1 (after M2), Quiz 2 (after M5), hands-on in Google Colab (token counting, cost estimation, hallucination demo).

---



## M1 — Foundation models & model selection



### Definition

A **foundation model** is a large neural network **pre-trained on broad data**, adapted for downstream tasks via **prompting** and sometimes **fine-tuning**.

### Three common deployment tiers


| Tier                         | Weights      | Typical access                        | Strengths                                                                                                 | Trade-offs                                          |
| ---------------------------- | ------------ | ------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| **Frontier (closed)**        | Not released | API (often chat + API)                | Highest capability; good for general tasks & prototyping                                                  | Per-token cost; data sent to vendor; vendor lock-in |
| **Open weight**              | Downloadable | Self-host or cloud-hosted open models | No per-token API fees (amortized hardware); data sovereignty; fine-tuning (incl. LoRA); air-gapped deploy | Up-front compute; you operate infra                 |
| **Specialized / fine-tuned** | Varies       | Provider or self-host                 | Vertical domains (medical, **code** — e.g. Code Llama, StarCoder)                                         | Host-dependent privacy; may need custom data        |


**Examples mentioned:** GPT, Claude (Sonnet), Gemini (frontier); Llama 3, Mistral, Falcon (open weight); Med-PaLM, code-specialized models.

### Model selection: three pillars

1. **Cost** — especially at scale (token burn in engineering orgs; e.g. industry concern over engineers “burning tokens”)
2. **Capability** — benchmarks and **your** task validation
3. **Risk** — data privacy, **IP indemnity**, **vendor lock-in**, **SLA/uptime**, contract exit cost

Risks can be **mitigated**, not fully eliminated.

### Capability benchmarks (programming focus)

- **MMLU** — broad knowledge (57 subjects)
- **HumanEval** — Python code generation from docstring + signature; **164 problems**; e.g. “90%” ≈ ~149/164 correct
- Domain-specific sets (e.g. Verilog/VLSI benchmarks) matter when general coding benchmarks don’t reflect your stack

**Rule:** Benchmarks are **guides** — always validate on **your** tasks.

### Context window vs. usable context

- **Context window** ≠ **usable context** — **attention degrades** on very long inputs (“**lost in the middle**”: beginning/end often reliable; middle weaker)
- Example intuition: 500K window might yield ~100K **effective** usable tokens (top + bottom chunks)


| Model (as discussed) | Context (approx.)      | Latency     | Notes                                                                  |
| -------------------- | ---------------------- | ----------- | ---------------------------------------------------------------------- |
| GPT-4.1              | ~1M tokens             | Medium      | Cost rises with large codebases                                        |
| Claude Sonnet        | ~200K                  | Low–medium  |                                                                        |
| Gemini 1.5 Pro       | Very large (~2M cited) | Medium–high | Long documents / legal corpora                                         |
| Llama (e.g. 70B)     | Depends on deploy      | Self-hosted | 70B ≈ “large”; smaller quantised variants (e.g. 8B) cheaper but weaker |




### When to choose which tier (heuristics from lecture)

- **Complex reasoning / agents:** GPT-4 class or Claude Opus  
- **High volume, cost-sensitive APIs:** GPT mini, Claude Haiku  
- **Very long documents / huge repos:** Gemini 1.5 Pro  
- **Strict on-prem / air-gap / defence-style rules:** **Open weight** (e.g. Llama) on owned infra  
- **Domain fine-tuning at scale:** Open-weight base + custom fine-tune  
- **Rapid exploration:** GPT-4.1 **mini** (cheap, fast)

**Open weight advantages:** no per-token API fees, amortized hardware, sovereignty, unrestricted fine-tune on proprietary data, LoRA ecosystem, GGUF/quantization, offline/air-gap.

**Cost at scale (lecture figure):** open weight can be **~5–25× cheaper** than frontier API at scale (transcript ASR: “weeks”; meaning in slide context is **multiplicative savings**).

---



## M2 — Token economics



### What is a token?

- LLMs consume text as **tokens** (subword pieces, often ~3–4 characters)
- **Autoregressive:** one token at a time; next token depends on all prior tokens (errors can **compound** → hallucination paths)



### Rules of thumb


| Quantity            | Approximate tokens                                |
| ------------------- | ------------------------------------------------- |
| 1,000 English words | **~1,333 tokens** (~4/3 expansion vs. word count) |
| 1 page of text      | **~700–800 tokens**                               |
| Typical API call    | **~500–2,000 tokens**                             |
| “Hello world”       | ~4 tokens (model-dependent)                       |




### Pricing structure

- Quoted in **USD per million tokens** (input vs. **output**)
- **Output usually costs more than input** — often **~4–5×** (model-dependent; e.g. Gemini ~4–5×, Claude Haiku ratio similar)
- **INR conversion:** lecture uses **₹84/USD** (adjust for current FX — costs scale with dollar)

**Example (lecture):** 1M **output** tokens on Claude Sonnet-class pricing (~$4.6/M output) ≈ **₹1,260** at ₹84/USD — sounds small until daily volume grows.

**Scale example:** **1M tokens/day** on Sonnet-class pricing ≈ **₹7,560/month** — framed as roughly **one junior developer-day of salary** (exchange rate drift can make AI relatively **more** expensive vs. flat INR salaries).

### Hidden cost: TCO

- **Raw API fees are misleading**
- **True TCO ≈ 2× raw API fees** when including infra, DevOps, prompt engineering, eval, RAG/vector DB (~10%), monitoring/guardrails, fine-tuning (5–15%), etc.
- **API/token line item ≈ 30–50%** of total deployment cost (rest is engineering + platform)



### Cost reduction strategies


| Strategy                   | Idea                                                                                                                                                           |
| -------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Minimize output tokens** | Ask for concise answers; refactor **sections** not whole files                                                                                                 |
| **Prompt caching**         | Static **system** prompt cached → **50–90%** discount on cached portion                                                                                        |
| **Batch APIs**             | Async bulk jobs → e.g. **~50%** OpenAI batch discount                                                                                                          |
| **Model routing**          | Small/cheap models for easy queries; frontier for hard tasks → **~60–80%** savings possible                                                                    |
| **Short prompts**          | Long prompts waste money; “effective” prompt may be ~**20%** of nominal size under lost-in-the-middle                                                          |
| **Batch vs. realtime**     | 1M output tokens/month GPT-4.1 **batch** ≈ **₹20,000/month** vs. **100 × 2K-token realtime calls** (200K tokens) costing **much more** for immediate responses |


**Hands-on reference:** GPT-4.1 pricing used in Colab — **$2/M input**, **$8/M output** (USD).

---



## M3 — Hallucinations & calibration



### Definition

**Hallucination:** model generates text that is **factually wrong, fabricated, or ungrounded** in context/input, often **stated confidently**.

### Why it happens (not a patchable “bug”)

- Autoregressive **probability** picking — greedy/high-probability tokens can be **semantically wrong**
- Wrong tokens enter context → **divergence** (hard to recover)
- **Lossy compression** of training data into weights → fabrication when recall fails
- **Noisy, contradictory, outdated** training data
- Switching to **local Llama** does **not** remove hallucinations — inherent to how LLMs work



### Severity tiers (examples)


| Tier            | Example                                                                                                |
| --------------- | ------------------------------------------------------------------------------------------------------ |
| **Harmless**    | Wrong year for Eiffel Tower (partially close)                                                          |
| **Problematic** | Fake paper/author; reputation damage                                                                   |
| **Dangerous**   | Wrong drug dose; legal fabricated cases (e.g. **Argentina lawyer / Mata v. Avianca** citation scandal) |




### Types (lecture)

- **Factual** — false fact with confidence → mitigate with **RAG**, sources  
- **Temporal** — outdated software/API answers  
- **Retrieval** — wrong grounding from search/RAG pipeline



### Calibration

- **Overconfidence** + wrong answer → highest risk (legal/medical/finance)
- **Underconfidence** (“I’m not sure…”) → often **more trustworthy** when answer is actually correct
- Use **confidence / faithfulness signals**, not vibe alone



### Mitigation playbook: **Prevent → Detect → Mitigate**

**Prevent**

- **RAG** / verified sources  
- **Structured outputs** (JSON schema)  
- **Domain limits** (“only answer about X”)  
- **Citation forcing** — every factual claim needs a source; “source unknown” = red flag

**Detect**

- **NLI faithfulness scoring** — e.g. P(entail) − P(contradiction); want **higher** score  
- Log confidence; monitor drift  
- **Self-consistency** — multiple samples; unstable answers → red flag

**Mitigate**

- **Human-in-the-loop** for commits, medical, legal, finance  
- **Graceful degradation** — prefer “I don’t know”  
- **Model versioning & rollback** if new model regresses on your queries

---



## M4 — AI coding tools (four compared)


| Tool                   | Form factor                        | Highlights                                                                                     |
| ---------------------- | ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| **GitHub Copilot**     | IDE extension, CLI, GitHub Actions | Enterprise adoption; deep GitHub integration; **IP indemnity** for generated production code   |
| **Cursor**             | AI-native IDE (VS Code fork)       | Tab completion <300ms; Composer multi-file edits; ~$20/mo (Pro tiers cited)                    |
| **Claude Code**        | Terminal agent                     | Strong **multi-file refactor**; agentic tasks; Sonnet/Opus; GitHub Actions, MCP                |
| **Windsurf (Codeium)** | Flow-state IDE                     | Cascade session memory; competitive pricing; generous free tier; good for cost-sensitive teams |


**Selection heuristics**

- **Enterprise + compliance + IP indemnity:** Copilot Business  
- **Individual/startup speed:** Cursor  
- **Staff engineer / large refactors:** Claude Code  
- **Student / emerging markets / tight budget:** Windsurf  
- **Mixed teams:** Copilot Business or Cursor Business

**Evaluate on your real codebase** before standardizing — no single universal winner.

---



## M5 — AI pair programming & Spec / Verify / Override



### AI pair programming vs. human pair programming

- Human pair: driver/navigator, **synchronous**, scheduling overhead  
- **AI pair:** **asynchronous**, on-demand, always available; **amplifies** developer — does **not** replace judgment

Research cited: ~**55% faster** task completion with AI pair programming (with discipline).

### Anti-pattern: “vibe coding” (transcript: *wide/white coding*)

- Accept AI output unread, skip tests, **prompt → copy → ship**  
- Dangerous in **production** — you (not the vendor) own quality and liability



### Disciplined workflow: **Spec → Verify → Override**

1. **Spec** — precise requirements (types, errors, edge cases, performance)
2. **Verify** — linters, types, **unit/integration/security** tests; review diffs (**≤ ~200 lines** per change)
3. **Override** — reject/fix; add constraints (e.g. concurrency fix on AI-generated banking snippet)

**Practices**

- Write **tests before** or alongside generation  
- Read **every line** of AI output  
- **Human developer** responsible for final quality (also Quiz 2)  
- Avoid auto-merge on security-sensitive code  
- Benchmark performance-critical changes

---



## M6 — Build vs. buy & hybrid architectures



### Core question

Before adding AI: **Does this task need AI at all?** Options: **build in-house**, **buy tool/API**, or **traditional logic only**.

### Prefer traditional / deterministic logic when

- Problem has **clear rules**  
- **Compliance, auditability, determinism** required  
- **Latency** ≪ LLM (e.g. **<10 ms** APIs vs. **200–2000 ms** LLM inference even with caching)  
- **Same input → same output** (pricing engines, discounts)  
- Known-schema **ETL** — simple deterministic code suffices



### Prefer AI when

- **NLP, images, unstructured data**  
- Creative generation, semantic search, chat/voice interfaces  
- No clean algorithm; many acceptable solutions



### Hybrid patterns (production norm)

- AI **extracts** → rules **validate**  
- AI **UI/NLP** → traditional **business logic**  
- AI **anomaly detection** → **human** decision  
- **Shadow mode:** run AI parallel to legacy **~4 weeks**, compare, then integrate — **don’t** push AI straight to prod



### Decision checklist (lecture summary)

1. Problem rule-defined enough? → **Rules first**
2. Input NLP/images? → **Consider AI**
3. Need extreme throughput/low latency? → **Avoid large LLMs**
4. Compliance/auditability? → **Deterministic or hybrid**
5. Cost at **₹1M+/day** scale? → **Open weight or traditional**
6. Novel task, no labels? → **Few-shot prompting**

**Closing theme:** AI does not accelerate everything; traditional logic doesn’t either — **horses for courses**, often **hybrid**.

---



## Hands-on takeaways (Colab)

Libraries: **transformers**, **tiktoken**, **sentencepiece**, **pandas**, **matplotlib**  
Tokenizer: `cl100k_base` (GPT-4 / GPT-3.5-style counting)  
Activities: token counting, API cost estimation, prompt cost comparison, token-saving strategies, hallucination demo  

Install pattern: `%pip install -q transformers tiktoken sentencepiece pandas matplotlib`

---



## Quick exam crib sheet

- **Model selection pillars:** cost, capability, risk  
- **On-prem mandatory:** open weight (e.g. Llama 3)  
- **Context:** larger ≠ always better; **attention degrades**  
- **1000 words ≈ 1333 tokens**  
- **Minimize output tokens** (output pricier)  
- **Hallucination:** fabricating facts confidently; **not fixable by “better model” alone**  
- **RAG** reduces hallucination via external retrieval  
- **Claude Code** — large multi-file refactor  
- **Workflow:** Spec, Verify, Override  
- **Final code quality:** **human developer**  
- **TCO ≈ 2× API fees**; routing/caching/batch save heavily

