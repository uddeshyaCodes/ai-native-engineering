# Lecture 03 — Likely Exam Q&A

Based on Dr. Mainak Mandal’s lecture *Accessible Component System Design with AI* (transcript `transcripts/module-1/lecture-03-accessible-components-with-ai.txt`). Answers reflect lecture content, not external trivia.

---

### 1. What problem did Tailwind CSS (utility-first CSS) solve?

**A:** Teams kept accumulating bespoke CSS class names for the same concepts (e.g. multiple `card-header` variants) because nobody removes production styles. Tailwind avoids inventing new semantic class names by **composing utility classes** at build time.

---

### 2. What does Radix UI provide that Tailwind alone does not?

**A:** Radix supplies **unstyled, accessible component behavior**: WAI-ARIA patterns, roles, focus management, and keyboard navigation. Tailwind handles **styling/composition**, not accessible interaction semantics.

---

### 3. How does shadcn/ui combine Radix and Tailwind?

**A:** shadcn/ui **copies** component source (e.g. `button.tsx`) into your repo, built on **Radix primitives** and styled with **Tailwind/CVA**. You own and edit the files; it is not a typical opaque npm UI package.

---

### 4. Why are AI coding agents especially effective with shadcn/ui?

**A:** Components live as **plain source files** in the repository. Agents can read and patch real code directly. Deep npm dependency trees hide the files that need changing and waste context guessing package internals.

---

### 5. What is CVA (Class Variance Authority) used for in this stack?

**A:** It maps component **props** (e.g. `variant`, `size`) to **Tailwind class strings** with no extra runtime CSS cost—one component definition, many visual states (`default`, `outline`, `ghost`, `destructive`, etc.).

---

### 6. Why use compound components (Card + CardHeader + CardTitle…) instead of one mega-card with many props?

**A:** Compound components avoid **prop explosion**, naming collisions across variants, and rigid markup. Parent context lets children compose flexibly and mirror on-screen structure in code.

---

### 7. What are design tokens, and why do they matter for AI-generated UI?

**A:** Named values for color, spacing, radius, etc., used instead of raw numbers everywhere. They keep **theming consistent** and give clearer constraints when prompting agents (vs. ad hoc “dark background” choices that may fail contrast or user needs).

---

### 8. What is WCAG, and which conformance level does the course target?

**A:** **Web Content Accessibility Guidelines** (W3C)—a **testable** rule set (pass/fail). The course targets **Level AA** of **WCAG 2.1**, widely referenced in law and industry.

---

### 9. Name the four WCAG principles (POUR) and one requirement under each from the lecture.

**A:**  
- **Perceivable** — e.g. alt text, **4.5:1** contrast for normal text.  
- **Operable** — full keyboard access, no keyboard traps, Escape closes dialogs.  
- **Understandable** — predictable navigation, clear errors.  
- **Robust** — compatible with assistive technologies.

---

### 10. What keyboard test did the instructor recommend for AA operability?

**A:** **Unplug the mouse** and complete tasks. If anything breaks, the interface fails operability expectations.

---

### 11. Why is keyboard support alone insufficient for screen reader users?

**A:** Elements also need **accessible names** and correct **roles/values** in the accessibility tree. A focusable control with no name/label can still be **unannounced** or meaningless to screen readers.

---

### 12. How does WAI-ARIA relate to the DOM and screen readers?

**A:** The browser exposes an **accessibility tree** (fed by ARIA attributes and semantics) via OS APIs. Screen readers consume that tree—not the visual DOM alone. ARIA changes **announcements**, not layout.

---

### 13. State the “first rule of ARIA” from the lecture.

**A:** **Do not use ARIA** when native HTML already conveys semantics (`button`, `nav`, `main`, labeled inputs, `ul`/`li` lists).

---

### 14. How can LLM-generated UI fail accessibility regarding ARIA?

**A:** **Under-use:** custom widgets/dropdowns without roles/labels; missing `aria-live` for dynamic content. **Over-use:** redundant roles on native elements; duplicate `aria-label` when visible text exists—causing **double announcements**.

---

### 15. What is axe-core’s core design trade-off, and what coverage figure was cited?

**A:** **Zero false positives**—only report provable violations (may miss subjective/grey issues). Lecture cited ~**57%** of WCAG-mandated issues caught automatically; ~**43%** needs human testing (screen reader, tasks, reading order, meaningful alt text).

---

### 16. What axe impact levels should block CI merges?

**A:** Focus on **critical** and **serious** (e.g. insufficient contrast, inputs without accessible names). Gate merges on **impact**, not total violation count alone.

---

### 17. What must you still do after automated axe tests pass?

**A:** Manual **screen reader** pass, **keyboard-only** task flows, and **200% zoom** checks for clipping—axe does not validate reading order, task success, or alt-text quality.

---

### 18. Why did the instructor say engineers remain necessary when AI generates UI?

**A:** AI output must be **verified**—contrast, populations (vision impairment, color blindness), prompts, and accessibility semantics. Example: a “dark compact tooltip” may ignore light mode or user needs; humans adjust prompts and code.

---

### 19. How does shadcn/ui differ from MUI/Chakra in deployment model?

**A:** Traditional libraries ship as large **npm dependencies** with hidden implementation. shadcn/ui adds **files to your project** (CLI/copy-paste)—you modify `components/ui/*.tsx` directly.

---

### 20. What legal/regulatory motivators for accessibility were mentioned?

**A:** US **ADA** (websites included; Target settlement); **EU Accessibility Act** (2025); **India RPWD Act 2016** aligning to WCAG 2.1 via **IS 17802**—plus lawsuits and users “locked out” of paying customers.
