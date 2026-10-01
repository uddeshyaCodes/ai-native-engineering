# In-Lecture Quizzes — Module 1, Lecture 1 (Mentimeter)

**Lecture:** Foundation Models, Token Economics & AI Pair Programming  
**Format:** Two quizzes, five questions each, conducted live via Mentimeter by Dr. Somposashi Mukhopadhyay  
**Timing:** Quiz 1 after sub-module M2 (token economics); Quiz 2 after M5 (AI pair programming), before hands-on / M6

---

## In-lecture Quiz 1 (after M2 — token economics & model selection)

### Quiz 1 — Question 1

**Question:** Which are the three pillars of model selection?

| Option | Text (as read in lecture) |
|--------|---------------------------|
| **1** | Cost, capability, risk |
| 2 | Speed, memory, accuracy |
| 3 | Hardware, software, network security |
| 4 | Latency and storage *(grouped with option 3 in poll)* |

**Class result:** ~92% chose option 1.

**Correct answer:** **Option 1 — Cost, capability, risk**

**Explanation:** Opening framework for the entire course session—every model/tool choice should be scored on economics, task fit, and organizational risk (privacy, IP, SLA, lock-in).

---

### Quiz 1 — Question 2

**Question:** Which model is most suitable when **data privacy and on-premise deployment** are mandatory?

| Option | Text (as read in lecture) |
|--------|---------------------------|
| 1 | GPT-4.1 (cloud) |
| 2 | Claude Sonnet |
| 3 | Gemini 1.5 Pro |
| **4** | **Llama 3 (open weight)** |

**Class result:** ~90% chose option 4; ~91% answered correctly.

**Correct answer:** **Option 4 — Llama 3 open weight**

**Explanation:** Open-weight models can be self-hosted on organization-controlled (including air-gapped) infrastructure; frontier APIs require sending data to vendor clouds.

---

### Quiz 1 — Question 3

**Question:** Which statement about **context windows** is true?

| Option | Text |
|--------|------|
| 1 | Larger context always means better accuracy |
| 2 | Context window equals usable context |
| **3** | **Attention can degrade in very long context** |
| 4 | Context window has no effect on latency |

**Class result:** ~77% chose option 3.

**Correct answer:** **Option 3**

**Explanation:** Lecture emphasized “lost in the middle”—nominal window size overstates **usable** context; long inputs suffer attention degradation (and latency/cost still matter).

---

### Quiz 1 — Question 4

**Question:** Approximately how many tokens are contained in **1,000 words**?

| Option | Tokens |
|--------|--------|
| A | 500 |
| B | 800 |
| **C** | **1,333** |
| D | 2,000 |

**Class result:** ~94% chose option C.

**Correct answer:** **Option C — 1,333**

**Explanation:** Rule of thumb from token economics: ~4/3 tokens per English word (~33% expansion vs. word count).

---

### Quiz 1 — Question 5

**Question:** Why should developers **minimize output tokens**?

| Option | Text (as read in lecture) |
|--------|---------------------------|
| A | They reduce model accuracy |
| **B** | **Output tokens are generally more expensive than input tokens** |
| C | They increase GPU memory |
| D | They reduce context size |

*Note: Transcript ASR garbled option B as “more expensive than human input tokens”; slide intent matches standard input vs. output pricing.*

**Class result:** ~93% chose option B.

**Correct answer:** **Option B**

**Explanation:** Providers typically charge a higher **per-million** rate for generated (output) tokens than for prompt (input) tokens—often several× more—so verbose completions dominate spend.

---

## In-lecture Quiz 2 (after M5 — hallucinations, tooling, pair programming)

### Quiz 2 — Question 1

**Question:** What is **hallucination** in an LLM?

| Option | Text |
|--------|------|
| A | Slow response |
| **B** | **Fabricating information presented as fact** |
| C | Context truncation |
| D | GPU memory overflow |

**Class result:** ~95–96% chose option B.

**Correct answer:** **Option B**

**Explanation:** Hallucination is confident but ungrounded or false content—not infrastructure failure or latency.

---

### Quiz 2 — Question 2

**Question:** Which technique helps **reduce hallucinations** by retrieving external documents?

| Option | Text (reconstructed from lecture; poll audio garbled) |
|--------|--------------------------------------------------------|
| A | *(Transcript: “Optional Ora” — option text unclear)* |
| B | Fine-tuning |
| **C** | **RAG (retrieval-augmented generation)** |
| D | Dropout |

**Class result:** ~97% chose option C.

**Correct answer:** **Option C — RAG**

**Explanation:** Grounding generation in retrieved, external documents reduces reliance on parametric memory alone; fine-tuning and dropout do not replace external retrieval.

*Transcript note: TA read options unclearly (“Optional Ora… fine tuning… COAC… drop out”); instructor confirmed **option C** (~97% correct), which matches the lecture’s RAG mitigation content.*

---

### Quiz 2 — Question 3

**Question:** Which AI coding tool is particularly suitable for **large multi-file refactoring**?

| Option | Text |
|--------|------|
| A | GitHub Copilot |
| B | Cursor |
| **C** | **Claude Code** |
| D | VS Code *(“BBS code” in transcript)* |

**Class result:** Majority voted Claude Code; ~74% marked correct.

**Correct answer:** **Option C — Claude Code**

**Explanation:** Lecture positioned Claude Code as strongest for agentic, repository-scale multi-file refactors (terminal/agent workflow).

---

### Quiz 2 — Question 4

**Question:** Which workflow is recommended for **disciplined AI-assisted software development**?

| Option | Text |
|--------|------|
| A | Prompt, copy, deploy |
| **B** | **Spec, verify, and override** *(read as “overwrite” in audio)* |
| C | Prompt, train, and test |
| D | Prompt, code, prompt, and merge *(“March” in transcript)* |

**Class result:** ~79 votes for option B; ~80% correct.

**Correct answer:** **Option B — Spec, Verify, Override**

**Explanation:** Matches Module 5 structured pair programming: specify precisely, verify with tests/review, override/fix before commit—opposite of vibe coding.

---

### Quiz 2 — Question 5

**Question:** In AI pair programming, who is **responsible for final code quality**?

| Option | Text |
|--------|------|
| A | AI model |
| B | IDE |
| **C** | **Human developer** |
| D | Cloud provider |

**Class result:** Option C received the most votes; instructor confirmed all participants answered correctly.

**Correct answer:** **Option C — Human developer**

**Explanation:** Legal and commercial liability stays with engineers/organizations even when code is AI-generated; vendors are not accountable to your customers.

---

## Summary

| Quiz | When | Questions | Topics covered |
|------|------|-----------|----------------|
| **Quiz 1** | End of M2 | 5 | Model selection pillars, on-prem/open weight, context/attention, token/word ratio, output token cost |
| **Quiz 2** | End of M5 | 5 | Hallucination definition, RAG, Claude Code refactors, Spec/Verify/Override, human accountability |

**Total in-lecture quiz questions extracted:** **10**
