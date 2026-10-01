# Lecture 03: Accessible Component System Design with AI

**Course:** AI-Native Software Engineering (Module 1)  
**Instructor:** Dr. Mainak Mandal, IIT Kharagpur  
**Transcript note:** The available transcript covers Chapters 1–3 in full and ends during Q&A after the Chapter 3 polls. Chapter 4 (end-to-end AI-generated UI verification) is announced in the intro but not present in this transcript.

---

## Learning goal

By the end of this lecture (as stated by the instructor), you should be able to build an **accessible component system** that can pass an **accessibility audit** (government, company, or third party)—written by you, possibly with AI assistance, but **verified by you**.

---

## Chapter 1: Component architecture — Tailwind CSS & shadcn/ui

> Transcript renders **“Chat CN” / “Shatsen UI”** as **shadcn/ui**.

### Historical arc (why these tools exist)

| Era | Idea |
|-----|------|
| **1996 — CSS1** | Separate stylesheets from HTML; control color, spacing, layout site-wide. |
| **2011+ — CSS3** | Flexbox, animations; modern layouts. |
| **Problem** | Teams invent endless custom class names (`card-header`, `card-header-v2`, `card-header-new`, …); nobody deletes production CSS. |
| **2017 — Tailwind CSS** (Adam Wathan) | **Utility-first CSS**: compose styling from utilities instead of naming every variant. |
| **2020 — Radix UI** | Unstyled, **accessible primitives** (behavior, focus, keyboard). |
| **2022 — shadcn/ui** | **Radix accessibility + Tailwind styling**; copy components into your repo (industry default for Next.js + Tailwind). |

### Tailwind CSS (utility-first)

- Utilities (e.g. `P4`, `font-semibold`) are composed in TSX—no new `.card-header-v3` in a global CSS file.
- Styles are **predetermined at build time** from a **config file** → **no runtime CSS cost** for those utilities.
- Override at use site: e.g. pass `className="P2 font-semibold"` to change padding without forking the component file.

### shadcn/ui vs traditional libraries (MUI, Chakra)

| Traditional npm UI library | shadcn/ui |
|----------------------------|-----------|
| Huge `node_modules`; button lives in minified vendor code | `components/ui/button.tsx` **in your repo** |
| Hard for humans/AI to safely edit internals | Plain source files—AI edits **real code**, not a black box |
| Install via npm only | **Copy-paste / CLI** adds files to the project (not an opaque dependency) |

**Why AI agents prefer shadcn/ui:** Agents can only fix code they can see. NPM packages hide implementation layers deep; shadcn components sit as **plain files** in the repository.

### Three pillars of the stack

1. **Tailwind** — utility-first engine; build-time generation from config.  
2. **shadcn/ui** — copy-paste components on **Radix primitives**; you **own** the code.  
3. **Design tokens** — named values for color, spacing, radius (theming consistency). Use open-source token sets where appropriate.

**Caveat:** “Accessible by default” is **partially** true via Radix; **you** must still verify prompts, tokens, and contrast (e.g. AI adding “dark background” tooltips without light-mode or population-specific needs).

### Radix UI (behavior layer)

- Follows **WAI-ARIA authoring patterns**.
- Handles **ARIA roles/attributes**, **focus**, and **keyboard navigation** internally.
- **Unstyled** by design—pair with Tailwind (shadcn) or any styling solution.
- **Composable**: granular parts; copy one primitive or the whole system.
- shadcn/ui **did not invent** accessible behavior—it **packages** Radix + editable Tailwind styling.

### CVA (Class Variance Authority)

- Maps **props → class strings** (e.g. `buttonVariants` with `default`, `outline`, `ghost`, `destructive`, sizes).
- Same markup/handlers; only the **class string** changes per variant.
- Typos in Tailwind classes (e.g. `focus-visible:outline-none` misspelled) → **compile-time** failure—catch with tests.

### Compound components

- **Problem:** Monolithic components with dozens of props → naming collisions (`default` on button vs text), rigid markup.
- **Fix:** Parent provides **context**; children compose (`Card`, `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, `CardFooter`).
- Encodes **visual structure in code**; teams can work on subparts without prop explosion.
- Same idea as escaping the old CSS class-naming mess—**composition over property sprawl**.

### When to use what

- **shadcn/ui + Tailwind:** Pixel-level control, AI-friendly owned components, accessibility primitives via Radix.  
- **MUI/Chakra:** Large template suites fast; can become hard to customize; AI + shadcn/templates can narrow the speed gap.

### Chapter 1 takeaways

- Tailwind = **composition**, not endless class naming.  
- shadcn/ui = **own the code**; copy-paste beats opaque npm for AI and audits.  
- **Compound components** replace prop explosion.  
- **Design tokens** keep theming consistent.  
- **AI generates fast; humans verify** (contrast, populations, prompts).

---

## Chapter 2: WCAG, keyboard access, WAI-ARIA

### Why accessibility is not optional

- ~**1.3 billion** people worldwide live with significant disability (WHO, cited in lecture).  
- **4000+** digital accessibility lawsuits in the US in 2024 (lecture figure).  
- **Regulations:** US **ADA** (websites, not just devices—Target settlement ~$6M, 2008); **EU Accessibility Act** (June 2025); **India RPWD Act 2016** → **WCAG 2.1** via **IS 17802**.

**Course target level:** **WCAG 2.1 Level AA** — legally referenced, rigorous, testable, shippable (with AI-native workflows).

### WCAG basics

- **WCAG** = Web Content Accessibility Guidelines (W3C); **testable pass/fail** rules.  
- **Levels:** **A** (minimum, e.g. alt text) → **AA** (legal/industry bar: **4.5:1** contrast for normal text, full keyboard support, focus visible) → **AAA** (often impractical globally; e.g. **7:1** contrast—selective use for dedicated accessible products).

### POUR (four principles)

| Principle | Meaning (lecture emphasis) |
|-----------|----------------------------|
| **Perceivable** | Alt text; **sufficient color contrast**; content adapts without losing meaning. |
| **Operable** | Full **keyboard** use; no seizure-inducing flashing; enough time to read moving content; no keyboard traps. |
| **Understandable** | Predictable navigation; clear errors. |
| **Robust** | Works with assistive tech (screen readers, etc.). |

### Example: inaccessible vs compliant UI

- **Bad:** Built in dark mode only → light mode yields **low-contrast** “Add to cart / terms apply”; **~22px** tap target; missing/poor **focus ring**.  
- **Good:** **4.5:1** contrast, **~44px** target, visible focus—usable for low vision and motor impairment.

### Keyboard support (AA)

**Simple test:** Unplug the mouse; if any task breaks, the interface is broken.

**Must work:** Logical **tab order**; **visible focus**; **Enter/Space** activate; **Escape** closes dialogs; **Tab / Shift+Tab**; arrow keys in custom widgets where expected.

**Must not happen:** **Keyboard traps**; **positive `tabindex`** to hijack order; missing focus outlines; mouse-only controls.

**Keyboard alone is insufficient:** Buttons need **accessible names** for screen readers—not just alt text on images.

### Focus trap (modals)

- Dialog open → focus may cycle **inside** the modal (focus trap).  
- Users must **Escape** (or equivalent) to exit; Radix/shadcn **Dialog** implements focus trap patterns.  
- Trap without escape = broken UX; ARIA exists partly because **dynamic AJAX** updates weren’t announced to screen readers.

### WAI-ARIA

- **Accessible Rich Internet Applications** — translation layer for assistive tech when native HTML isn’t enough.  
- Browser builds an **accessibility tree** (parallel to DOM); OS APIs (**UIA** on Windows, **AX** on macOS) expose it; **screen readers read the API**, not raw DOM.  
- ARIA **does not change layout/CSS**; it changes **what is announced**.

**Semantics:**

- **Roles** (e.g. `dialog`, `tab`)  
- **States** (`aria-expanded`, `aria-checked`) — must stay in sync  
- **Properties** (`aria-label`, `aria-labelledby`, `aria-describedby`)

**Modal example (lecture):** `role="dialog"`, `aria-modal="true"`, `aria-labelledby` / `aria-describedby` → inert background; screen reader announces title and description.

**First rule of ARIA:** Don’t use ARIA if **native HTML** works (`<button>`, `<nav>`, `<main>`, `<label>` on inputs, `<ul>`/`<li>`).

**Decorative icons:** `aria-hidden="true"` so screen readers skip them.

### Population → solution (thumb rules for prompts)

- Low vision / dyslexia → contrast, not color-only meaning.  
- Color blindness → never red=bad / green=good **by color alone**.  
- Motor → keyboard + large targets.  
- Cognitive → plain language, consistent nav, no time pressure.  
- Deaf/hard of hearing → captions/transcripts.

### AI + ARIA limitations

LLMs **under-use** ARIA (custom dropdowns with no semantics; missing **`aria-live`** for async updates) and **over-use** it (`role="button"` on a real `<button>`; duplicate `aria-label` when visible text exists → double announcement).

Root cause: pattern matching **without** modeling the accessibility tree.

### Chapter 2 takeaways

- Accessibility is an **architecture constraint**, not a post-hoc checklist.  
- **AA** = contrast, keyboard, focus, name/role/value.  
- **Radix/shadcn** give a head start; **you** verify tokens, modes, and AI output.

---

## Chapter 3: Automated accessibility testing (axe-core)

### Why automation

- Manual-only audits **don’t scale** (Target case); inconsistent across auditors; stale after each release.  
- **axe-core** (~2017, Deque, open source): industry-standard **automated** a11y engine.

### Design rule: zero false positives

- axe reports only violations it can prove → fewer subjective “grey zone” catches.  
- ~**57%** of WCAG-mandated issues (lecture figure); **~43%** still needs **human** review (screen reader walkthrough, meaningful alt text, task completion, reading order).

### What axe checks (examples)

- Color contrast (e.g. **4.5:1**).  
- ARIA validity.  
- Form labels.  
- Heading structure (real headings vs giant `<div>`).

Framework-agnostic (shadcn, MUI, etc.).

### Impact levels

| Level | Examples (lecture) | Response |
|-------|-------------------|----------|
| **Minor** | Missing `lang` | Dev warning |
| **Moderate** | Redundant ARIA role | Dev warning |
| **Serious** | Insufficient contrast; input with no accessible name | Unit tests / block merge |
| **Critical** | — | **CI gate** — block merge/deploy |

Gate on **impact** (critical/serious), not raw violation count alone.

### Testing patterns

**Component unit test (Jest + Testing Library + jest-axe):**

- Render component → `axe(container)` → `expect(results).toHaveNoViolations()`.

**Full page (Playwright + `@axe-core/playwright`):**

- Navigate → `AxeBuilder` with tags (e.g. WCAG 2.x **A and AA**) → assert no **critical/serious** violations.

**AI can scaffold tests** but often only **happy path**—review container, variants, and corner cases; re-prompt in a loop.

### What automation cannot catch

- Logical **reading/tab order**  
- Whether **alt text is meaningful**  
- Whether users can **complete real tasks**  
- Subjective design choices (axe avoids false positives here)

### After axe passes

- **Screen reader** walkthrough  
- **Keyboard-only** task flows  
- **200% zoom** — check clipping/reflow  

**axe is a floor, not a ceiling.**

### Chapter 3 takeaways

- Automate the **floor**; spend human time on the **ceiling**.  
- Layer: dev warnings → unit tests → CI scans by severity.  
- Playwright for **functionality**; axe for **accessibility rules**.

---

## Chapter 4 (planned — not in transcript)

Intro promised: **end-to-end AI-generated UI** and **how to verify** it; current techniques “not enough” without human verification, screen readers, and targeted prompts. Details were not recorded in `transcripts/module-1/lecture-03-accessible-components-with-ai.txt`.

---

## Glossary (transcript spellings → intent)

| Heard in transcript | Intended term |
|---------------------|---------------|
| Chat CN / Shatsen UI | shadcn/ui |
| Y area / area | WAI-ARIA / ARIA |
| W cat / West CAC | WCAG |
| X score / Export | axe-core |
| Adder | ADA |
| CVA | Class Variance Authority |
| A11Y | Accessibility (a + 11 letters + y) |
