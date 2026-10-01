# Lecture 03 — In-Lecture Polls & Quizzes

Polls were run via QR code after **Chapters 1, 2, and 3** (hydration breaks). Question stems below are taken **verbatim or paraphrased only from** `transcripts/module-1/lecture-03-accessible-components-with-ai.txt`. Where the transcript gives **correct-answer commentary** but not MCQ options, answers are tied to that commentary and matching lecture content—**not invented distractors**.

**Transcript gap:** Chapter 3 poll **questions were not read aloud** in the transcript (only “most got it correct”). Those polls are listed with a note, not fabricated stems. One WCAG poll (“tricky question”) has **no stem** in the transcript. **Chapter 4** had no polls in the available transcript.

---

## Poll set 1 — After Chapter 1 (Tailwind / shadcn/ui)

### Q1

**Question (from transcript):** What is the main way **shadcn/ui** differs from a traditional component library like **MUI**?

**Instructor:** Most answered correctly.

**Answer (from lecture + debrief):** shadcn/ui delivers **copy-paste component source in your repo** that you **own and edit**; it is **not** a typical opaque **npm install** where button implementation lives deep in `node_modules`. MUI/Chakra-style libs ship vendor code you rarely modify.

---

### Q2

**Question (from transcript):** What problem did **Radix** solve that **Tailwind CSS** did not?

**Instructor:** Almost everyone correct; topic covered in the last half hour of Chapter 1.

**Answer:** **Accessible component behavior**—WAI-ARIA patterns, roles, focus, keyboard navigation—while Tailwind solves **styling via utility composition**, not semantic/assistive behavior.

---

### Q3

**Question (from transcript):** Based on what we just saw about **card components** (compound structure).

**Instructor:** “The one that maximum people have understood correctly.”

**Answer (from lecture):** Use **compound components** (`Card`, `CardHeader`, `CardTitle`, …) so structure composes without a monolithic card with dozens of props—parent provides context, children consume it.

---

### Q4

**Question (from transcript):** Why do **coding agents** work particularly well with **shadcn/ui**?

**Instructor:** Because components sit as **plain files in a repo** without agents needing deep knowledge of folder/package internals.

**Answer:** shadcn/ui places editable **source files** (e.g. under `components/ui/`) in the repository, so agents patch **visible source**, not hidden npm layers.

---

## Poll set 2 — After Chapter 2 (WCAG / ARIA)

### Q1

**Question (from transcript):** Normal sized text — WCAG contrast requirement. (Transcript ASR: “WCGAG … **4.1**”.)

**Instructor:** Most responded correctly.

**Answer (from lecture content, not the garbled “4.1”):** **4.5:1** minimum contrast ratio for normal text at Level **AA**. (Large text: lecture mentioned **3:1** for large text.)

---

### Q2

**Question (from transcript):** Which of these is a **WCAG keyboard violation** (not a valid technique)?

**Options read in session:**

- A visible focus indicator on every interactive element  
- Escape closing an open dialogue  
- **Using positive `tabindex` values to control tab order**  
- Arrow key navigation inside a custom menu  

**Instructor:** Most chose correctly; noted that “visible focus indicator” was a common **wrong** pick—focus indicators are **required**, not violations.

**Answer:** **Using positive `tabindex` to control order** — lecture explicitly forbids positive `tabindex` values.

---

### Q3

**Question:** *Not captured in transcript.* Instructor: “Good question … **tricky question**, but that shows that we understood it.”

**Answer:** *Stem and choices unavailable in `transcripts/module-1/lecture-03-accessible-components-with-ai.txt` — refer to live poll slides or recording.*

---

### Q4

**Question (from transcript):** Which statement about **ARIA** is correct? (“Which straight node area is correct?”)

**Instructor debrief (correct vs incorrect statements):**

- **Correct:** ARIA changes **what is announced**, **not** what is shown visually.  
- **Incorrect:** “ARIA attributes are read **directly from the DOM** by screen readers.” Screen readers use the **accessibility tree** exposed via OS APIs (UIA/AX), not raw DOM alone.

**Answer:** Select the option equivalent to: **ARIA affects assistive technology announcements, not visual layout** — and **reject** the option that screen readers read ARIA straight from the DOM without the separate accessibility tree.

---

## Poll set 3 — After Chapter 3 (axe-core)

The facilitator ran **four poll questions** (“first question … next one … last question … wraps up the polling”). The transcript **does not include question text or options**—only that most participants answered correctly.

| Poll # | Transcript record |
|--------|-------------------|
| 1 | “Clear favorite”; most correct |
| 2 | Most correct |
| 3 | “Relatively easier” |
| 4 | Last question; poll wrap-up |

**Answer:** *Stems not in transcript — use course slides/Mentimeter export or video for exact MCQs. Lecture content to revise: axe **zero false positives**, ~**57%** WCAG issue coverage, **critical/serious** CI gates, jest-axe + Playwright `AxeBuilder`, manual screen reader pass for the remainder.*

---

## Q&A snippet (not a poll)

**Question:** Can a **WCAG-compliant website** be used as **grounding** for an AI agent to build another compliant site?

**Answer (instructor):** Partly—you need **much better prompting**; you cannot say “this site is compliant, make mine compliant too” because your buttons, roles, custom widgets, and features differ. Grounding requires explicit constraints, not a single generic compliance claim.
