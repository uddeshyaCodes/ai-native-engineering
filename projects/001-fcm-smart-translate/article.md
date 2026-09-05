# Solving the Workflow, Not Just the AI

## Lessons from building an AI-assisted localisation pipeline during a five-day hackathon

> *The hardest part of building an AI application isn't always the AI. Sometimes, it's understanding the problem well enough to know where AI actually belongs.*

---

## Introduction

Like many developers experimenting with Large Language Models (LLMs), I walked into our internal hackathon with a fairly simple assumption.

The hardest part of building an AI application would be getting the model to do its job well.

In our case, that meant translation.

If we could produce accurate, consistent translations, I assumed we'd have solved the problem.

Five days later, I realised I'd been solving the wrong problem.

By the end of the hackathon, I'd learnt that the challenge wasn't translation, prompt engineering or even choosing the right model. The real challenge was understanding an existing business workflow well enough to redesign it around AI without disrupting the people who depended on it.

Although this project focused on localisation, the lessons extended far beyond translation. They fundamentally changed the way I think about designing AI-assisted systems.

---

## Understanding the Problem

Earlier this year, alongside my front-end development responsibilities, I also became the Translation Coordinator for my project. That gave me a completely different perspective on how our software moved from development to production.

Every release followed a familiar localisation process. New UI strings were exported from our localisation platform, sent to an external translation agency, quoted, approved, translated, imported back into the platform and finally reviewed before they were published.

> **📌 Diagram Placeholder – Existing Localisation Workflow**

Nothing about the workflow was fundamentally broken. It had evolved over time, and everyone involved understood their role.

What stood out to me, however, was the amount of operational work surrounding translation itself. Exporting files, coordinating with translators, tracking progress, importing results and preparing everything for review consumed far more effort than I had expected.

When our team began discussing hackathon ideas, my instinct was to focus on the most obvious part of the process.

*Can we build a better translator?*

Looking back, I think that was the wrong question.

---

## Reframing the Problem

One of the most valuable lessons from the project came surprisingly early.

We realised we were trying to optimise the wrong part of the workflow.

Our initial question was centred around technology:

> **How can AI translate our strings?**

As we analysed the localisation process in more detail, it became obvious that translation itself wasn't the bottleneck. Professional translators already existed, and they were exceptionally good at what they did.

The larger challenge was everything surrounding the translation.

Preparing files.

Managing requests.

Waiting for approvals.

Importing completed translations.

Coordinating the entire workflow.

That shifted our thinking completely.

Instead of asking how AI could translate our content, we started asking:

> **How can AI reduce the operational overhead while preserving quality?**

It sounds like a small change in perspective.

In reality, it changed the entire solution.

> **📌 Diagram Placeholder – From "AI Translation" to "AI-Assisted Workflow"**

---

## Designing Around the Workflow

Once we reframed the problem, our design decisions became much clearer.

Our objective was never to replace professional translators or eliminate human review. Those parts of the process already worked well and existed for good reasons.

Instead, we wanted to remove the repetitive tasks that surrounded them.

Could we automatically identify new strings that required translation?

Could we provide the model with enough context to generate useful draft translations?

Could we preserve consistent terminology?

Could we reuse previous translations instead of generating them again?

Could we return everything back into the existing localisation platform so reviewers could continue working exactly as they always had?

Those questions gradually transformed our project from "an AI translator" into "an AI-assisted localisation pipeline".

The distinction mattered because it shifted our attention away from the model and towards the overall system.

---

## The Model Was Only One Component

Before the hackathon, I expected prompt engineering to occupy most of our time.

It didn't.

Instead, most of our effort went into solving engineering problems around the model.

We built mechanisms to provide better context, maintain consistent terminology, reuse previous translations, reduce unnecessary token usage and integrate the generated translations back into the existing workflow.

> **📌 Diagram Placeholder – High-Level Architecture**

Looking back, it's interesting how small the LLM became within the overall architecture.

The model generated translations, but the surrounding system determined whether those translations were useful.

That was one of the biggest surprises of the entire project.

---

## What Changed for Me

Before this project, I associated AI engineering primarily with prompts, models and APIs.

Today, I think those are only one part of the picture.

The more interesting engineering questions looked like this:

- What information does the model actually need?
- How much context is enough?
- How do we maintain consistency across multiple releases?
- How do we reduce unnecessary token consumption?
- How do we integrate AI into an existing workflow without forcing people to change how they work?

Very few of those questions are about the model itself.

They're systems design questions.

That shift in perspective has stayed with me long after the hackathon ended.

---

## Looking Ahead

This project introduced us to several engineering challenges that deserve much deeper discussion than one article can provide.

In future articles, I'll be exploring topics such as:

- Why context engineering mattered more than prompt engineering.
- Designing an effective translation memory.
- Dynamic glossary retrieval for domain-specific terminology.
- Reducing token consumption without sacrificing quality.
- Building AI systems around existing human workflows.

Each of those decisions solved a different engineering problem, and together they shaped the final system far more than the prompt ever did.

---

## Final Thoughts

When I look back at this project, I don't think we built an AI translator.

We built a localisation system that happened to use an LLM.

That distinction fundamentally changed how I think about AI engineering.

It's easy to focus on models, prompts and benchmarks because they're the most visible parts of an AI application. But in practice, the success of a system often depends on everything around the model: understanding the business process, respecting existing workflows, providing the right context and designing for the people who will ultimately use it.

The technology will continue to evolve.

Understanding the problem you're trying to solve will always matter more.