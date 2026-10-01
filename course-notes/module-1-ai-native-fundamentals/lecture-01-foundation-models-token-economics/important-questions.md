# Important Questions — Module 1, Lecture 1 (Foundation Models, Token Economics & AI Pair Programming)

Practice for graded MCQs and short answers. Each item includes an **answer** and a **brief explanation**.

---

## Model selection (cost / capability / risk)

**1. What three factors should primarily drive foundation model selection in professional software engineering?**  
**Answer:** Cost, capability, and risk.  
**Explanation:** The lecture frames all adoption decisions around economic scale, task-fit (benchmarks + your validation), and non-functional risks (privacy, IP, lock-in, SLA).

**2. Which model category is most appropriate when data privacy and on-premise deployment are mandatory?**  
**Answer:** Open-weight models (e.g., Llama 3) self-hosted on organization-controlled infrastructure.  
**Explanation:** Frontier APIs send data to vendors; open weights can run air-gapped/on-prem with full operational control (subject to how you host them).

**3. Why can a model with a larger advertised context window still perform poorly on a single long prompt?**  
**Answer:** Usable context is smaller than the nominal window; attention degrades in the middle (“lost in the middle”).  
**Explanation:** Effective retrieval of facts often concentrates at the start/end of long contexts; middle sections may be ignored or weakly used.

**4. What is the main limitation of using HumanEval scores alone to pick a coding model?**  
**Answer:** It measures Python function synthesis from docstrings—not your full stack, repo scale, or domain.  
**Explanation:** Benchmarks are guides; the instructor stresses validation on your actual tasks (multi-language, Verilog/VLSI examples, etc.).

**5. Name two “risk” issues beyond data privacy when buying frontier API access.**  
**Answer:** IP indemnity exposure and vendor lock-in / SLA constraints (any two of: indemnity, lock-in, uptime SLA, contract exit cost).  
**Explanation:** Production code may infringe third-party IP; long contracts make switching costly even if quality or uptime disappoints.

**6. When is Gemini 1.5 Pro especially suited according to the lecture?**  
**Answer:** Very long documents or huge code/text corpora (e.g., legal analysis).  
**Explanation:** Extremely large context window trades off with medium–high latency but fits whole-corpus workflows.

**7. Open-weight models at scale can be how much cheaper than frontier APIs (order-of-magnitude stated in class)?**  
**Answer:** Roughly 5–25× cheaper at scale (per lecture slide; transcript ASR says “weeks”).  
**Explanation:** Amortized hardware vs. per-token API fees dominates at high volume.

---

## Tokens & economics

**8. Approximately how many tokens are in 1,000 English words?**  
**Answer:** ~1,333 tokens.  
**Explanation:** Rule of thumb: ~4/3 expansion from word count to token count.

**9. Why should developers minimize output tokens in production LLM use?**  
**Answer:** Output tokens are typically more expensive than input tokens (often ~4–5×).  
**Explanation:** Providers charge higher rates for generation; verbose completions multiply cost at scale.

**10. If USD ≈ ₹84, what INR cost did the lecture cite for ~1M output tokens on Claude Sonnet-class output pricing (~$4.6/M)?**  
**Answer:** About ₹1,260.  
**Explanation:** Illustrates that “per million” sounds small but compounds with daily volume (e.g., ₹7,560/month for 1M tokens/day).

**11. What is a reasonable TCO multiplier versus raw API fees, once engineering and platform costs are included?**  
**Answer:** About **2×** raw API fees; tokens alone may be only **30–50%** of total deployment cost.  
**Explanation:** Prompt engineering, eval, RAG, monitoring/guardrails, fine-tuning, and DevOps add substantial overhead.

**12. Name three strategies to reduce token spend mentioned in the lecture.**  
**Answer:** Any three: prompt caching, batch APIs, model routing to smaller models, concise output instructions, shorter prompts, section-scoped refactors instead of full-file regen.  
**Explanation:** Caching/batching give large discounts; routing avoids using frontier models for trivial queries (60–80% savings cited).

**13. Why is batch mode much cheaper than synchronous API calls for the same total tokens?**  
**Answer:** Providers discount asynchronous bulk processing; you trade latency for cost.  
**Explanation:** Example: 1M monthly output tokens in batch vs. many 2K-token realtime calls—the realtime pattern costs far more for less total work.

---

## Hallucinations & calibration

**14. Define hallucination in an LLM.**  
**Answer:** Generating content that is false, fabricated, or ungrounded in context/input while presenting it as factual.  
**Explanation:** Core quiz definition: not slow response, OOM, or mere truncation.

**15. Is hallucination a bug that disappears if you self-host an open-weight model?**  
**Answer:** No.  
**Explanation:** It arises from autoregressive probabilistic generation and lossy training—not from “closed vs. open” alone.

**16. Which technique reduces hallucinations by retrieving external documents?**  
**Answer:** RAG (retrieval-augmented generation).  
**Explanation:** Grounds answers in verified corpora instead of parametric memory only.

**17. What are the three hallucination severity levels illustrated in class?**  
**Answer:** Harmless, problematic (reputation/professional harm), dangerous (e.g., medical/legal harm).  
**Explanation:** Mitigation strictness should match downstream impact.

**18. What is the mitigation playbook order taught in the lecture?**  
**Answer:** Prevent → detect → mitigate.  
**Explanation:** Accept inevitability; combine RAG, structured outputs, NLI faithfulness, self-consistency, human review.

**19. Why is overconfident wrong output worse than underconfident output?**  
**Answer:** Users trust and act on confident answers without verification.  
**Explanation:** Underconfidence signals need to cross-check; overconfidence drives blind adoption (especially in legal/medical/finance).

**20. What NLI-style score did the lecture emphasize increasing?**  
**Answer:** P(entailment) − P(contradiction) (faithfulness / NLI score).  
**Explanation:** Higher score means generated hypothesis is more supported by premise/source text.

---

## AI tooling & pair programming

**21. Which tool did the instructor highlight for large multi-file refactoring?**  
**Answer:** Claude Code.  
**Explanation:** Described as strongest for agentic multi-file refactors at industry scale.

**22. Which commercial coding assistant prominently offers IP indemnity for generated production code?**  
**Answer:** GitHub Copilot.  
**Explanation:** Vendor may defend/legal-cost coverage if generated code faces infringement claims—important for Fortune 500 buyers.

**23. What workflow is recommended for disciplined AI-assisted development?**  
**Answer:** Spec → Verify → Override (quiz wording: “Spec verify and override/overwrite”).  
**Explanation:** Contrasts with “prompt, copy, deploy” or untested ship paths.

**24. In AI pair programming, who is responsible for final code quality?**  
**Answer:** The human developer.  
**Explanation:** Customers blame engineers/companies—not Microsoft/Anthropic—if untested AI code ships.

**25. What maximum diff size per review did the lecture recommend, and why?**  
**Answer:** About **200 lines**; larger diffs exceed effective human review capacity.  
**Explanation:** Prevents “prompt-copy-ship” fatigue and missed regressions across many files.

**26. What is “vibe coding” (wide/white coding) and why is it risky in production?**  
**Answer:** Accepting AI output without understanding, tests, or review.  
**Explanation:** Non-programmers may ship unsafe commands/code; professionals must not adopt the same trust model.

---

## Build vs. buy / hybrid

**27. When should traditional deterministic logic beat an LLM?**  
**Answer:** Clear rules, strict auditability/compliance, need for identical outputs, ultra-low latency, deterministic ETL.  
**Explanation:** LLMs are probabilistic (same prompt may differ) and slower than rule engines.

**28. What deployment pattern runs AI alongside legacy systems before cutover?**  
**Answer:** Shadow mode (parallel run, compare outputs for weeks, then gradual integration).  
**Explanation:** Avoid pushing AI directly to production without measured accuracy.

**29. Give one hybrid architecture pattern from the lecture.**  
**Answer:** AI extracts fields from unstructured input → deterministic rules validate types/ranges.  
**Explanation:** Combines NLP strength with auditable business logic.

**30. According to the checklist, when cost reaches roughly ₹1 million per day, what directions are favored?**  
**Answer:** Open-weight or traditional approaches (vs. unchecked frontier API burn).  
**Explanation:** Scale forces economic architecture, not hype-driven model choice.

---

## Short scenario (exam-style)

**31. A defence client forbids external network access and requires models on internal servers. Which tier and hosting model do you recommend?**  
**Answer:** Open-weight (or specially licensed on-prem frontier) on internal air-gapped servers.  
**Explanation:** Matches lecture examples of defence/agency constraints and data sovereignty.

**32. An engineer asks GPT-4.1 to rewrite an entire 5,000-line file but only 100 lines need optimization. What token-economic fix does the lecture suggest?**  
**Answer:** Scope the prompt to the relevant section or lines instead of regenerating the whole file.  
**Explanation:** Reduces **output** tokens—the dominant cost driver.
