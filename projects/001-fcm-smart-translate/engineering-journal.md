# Project 001 – FCM Smart Translate

> *From a Manual Translation Workflow to an AI-Assisted Localisation Pipeline*

---

# Project Information

| Field | Value |
|--------|-------|
| Project | FCM Smart Translate |
| Type | Internal Hackathon Project |
| Duration | 5 Days |
| Status | Prototype |
| My Roles | Front-end Engineer, Translation Coordinator, Solution Architect |
| Team | 2 Front-end Engineers, 1 QA Engineer |
| Technologies | Node.js, TypeScript, React, Azure OpenAI, WebTranslateIt API, Cursor |
| Primary Model | GPT-4o |
| Objective | Reduce localisation cost and turnaround time by automating the translation workflow whilst keeping humans in the review loop |

---

# Executive Summary

Software products evolve continuously, and every release introduces new user interface (UI) strings that must be translated before reaching customers across the world. Whilst translation itself is an essential part of delivering a global product, the process surrounding it is often far more expensive and time-consuming than the translation work itself.

After taking over the role of Translation Coordinator for our product, I became responsible for coordinating translations with our external localisation agency alongside my existing front-end development responsibilities. It quickly became apparent that the workflow had changed very little over the years. Every release required exporting untranslated strings from WebTranslateIt (WTI), requesting a quotation from the agency, waiting for internal approval, waiting for the completed translations, and finally importing the translated files back into WTI.

This process typically took between three and four weeks regardless of how many new strings required translation. Because the agency charged a minimum fee per language, even very small releases incurred a significant cost. In one instance, the team paid €182.70 to translate only a handful of strings. For the following two releases, translations were postponed altogether because the number of new strings did not justify the agency's minimum charges.

Rather than accepting this as an unavoidable part of the release process, I began exploring whether recent advances in Large Language Models (LLMs) could automate the workflow whilst maintaining translation quality and preserving the existing human review process.

That question became the foundation of our internal hackathon project.

Over five days, our team designed and implemented **FCM Smart Translate**, an AI-assisted localisation pipeline that automatically retrieves untranslated strings from WebTranslateIt, translates them into six target languages using Azure OpenAI, and uploads the translated files back into WTI as **Unproofread**, allowing them to follow the existing review workflow.

Although the project relies on LLMs for translation, the primary engineering challenge was not the model itself. Producing reliable translations required carefully engineering the surrounding system. Throughout the project we introduced project-specific glossaries, translation memory, language-specific rules, contextual prompting, glossary optimisation and cross-file translation caching to improve translation consistency whilst controlling token consumption.

The resulting prototype demonstrated that AI-generated translations could closely match professionally translated output whilst reducing translation time from several weeks to a matter of minutes and lowering operational costs by more than 99%. Equally importantly, the project demonstrated that AI can augment an existing software delivery workflow without removing humans from the process. Instead of replacing professional translators, the system enables them to review and approve AI-generated translations rather than translating every string from scratch.

This engineering journal documents the evolution of the project from an operational pain point to a working prototype. Rather than focusing solely on the use of AI, it explores the architectural decisions, engineering trade-offs, technical challenges and lessons learned whilst designing a practical AI-assisted localisation workflow.

# 2. Background

For most of my time on the project, localisation was something that happened in the background. As a Front-end Engineer, my involvement was limited to adding new UI strings whenever I introduced new features. Once development was complete, the translation process was handled by the designated Translation Coordinator, who worked with our external localisation agency to ensure every release was translated into the supported languages.

That changed when I took over the role of Translation Coordinator.

Alongside my front-end development responsibilities, I became responsible for preparing translation files, coordinating with the agency, tracking quotations, managing the translation cycle and uploading the completed translations back into WebTranslateIt.

Experiencing the workflow from the other side quickly changed my perspective.

What initially appeared to be a straightforward operational task was, in reality, a lengthy process involving multiple manual steps and significant waiting time. Every release followed the same sequence: export untranslated strings, request a quotation, wait for approval, wait for the translated files to be delivered, and finally upload them back into WebTranslateIt.

What surprised me most was that the process was almost entirely independent of the amount of work involved.

Whether the release introduced hundreds of new strings or only a handful, the workflow remained largely the same. The agency charged a minimum fee for each language, meaning even the smallest releases incurred a relatively high cost.

Curious to understand the impact, I reviewed the translation costs from our previous releases.

The numbers were difficult to ignore.

One release had cost €182.70 despite containing only a very small number of new strings. The cost was driven almost entirely by the agency's minimum pricing policy rather than the amount of translation work itself.

The consequences extended beyond cost alone.

For the following two releases, translations were postponed because there were too few new strings to justify another agency request. The process had effectively become a bottleneck: small releases either incurred disproportionate costs or shipped without updated translations.

At that point, I stopped asking how the existing process worked and started asking a different question:

**Why does this process exist in its current form?**

By this time, Large Language Models had demonstrated impressive capabilities across a variety of language tasks. Rather than viewing AI as a replacement for professional translators, I began wondering whether it could eliminate the repetitive operational work surrounding translations whilst allowing human reviewers to remain responsible for quality assurance.

When the company announced the quarterly hackathon, it provided the perfect opportunity to explore that idea.

# 3. The Problem

The challenge was never translation itself.

The challenge was the workflow surrounding translations.

Our product supports multiple languages, with English serving as the source language and six additional locales maintained through WebTranslateIt (WTI). Every new feature, enhancement or bug fix introduced new UI strings that required translation before a release could be considered complete.

At the time, the localisation workflow relied entirely on a professional translation agency.

Whenever new English strings were added, the Translation Coordinator was responsible for exporting the untranslated files from WTI, requesting a quotation from the agency, waiting for internal approval, sending the files for translation, waiting for the completed translations and finally importing the translated files back into WTI.

Although each individual step was relatively straightforward, the overall process was slow and almost entirely manual.

More importantly, the cost and turnaround time were largely independent of the amount of work required.

The agency charged a minimum fee for every target language. As a result, even a release containing only a handful of new strings incurred a significant translation cost. For larger releases this pricing model was reasonable, but for smaller maintenance releases it became increasingly difficult to justify.

This created an undesirable trade-off.

Small releases either incurred disproportionate translation costs or shipped without updated translations altogether.

Neither outcome was ideal.

From an engineering perspective, another issue became apparent.

The workflow had no technical bottleneck.

There were no complex algorithms, computational limitations or integration challenges preventing faster translations. The bottleneck existed because the process had been designed around human coordination rather than software automation.

Every release followed the same sequence of manual actions regardless of whether five strings or five hundred strings required translation.

As the Translation Coordinator, I found myself questioning whether AI could automate these repetitive operational tasks whilst preserving the existing review process.

The objective was never to remove professional translators from the workflow.

Instead, the goal was to automate everything surrounding translation so that human expertise could be focused where it added the most value: reviewing and validating translations rather than producing every translation manually.

# 4. Existing Workflow

Before designing a replacement, it is important to understand the existing localisation process.

At the time of the hackathon, every release followed the same workflow regardless of the number of new UI strings requiring translation. The process involved multiple stakeholders, manual hand-offs and significant waiting time, making it both expensive and difficult to scale for smaller releases.

The workflow is illustrated below.

```text
                 New UI Strings
                        │
                        ▼
        Export untranslated strings from WTI
                (Translation Coordinator)
                        │
                        ▼
       Request quotation from translation agency
                (Translation Coordinator)
                        │
                        ▼
            Internal approval of quotation
                        │
                        ▼
        Translation agency performs translation
                  (Typically 1–2 weeks)
                        │
                        ▼
        Receive translated language files
                        │
                        ▼
     Upload translated files back into WTI
                (Translation Coordinator)
                        │
                        ▼
          Translations available for release
```

## Workflow Analysis

Although the workflow appears relatively simple, several characteristics made it inefficient.

### Manual Coordination

Almost every step required manual intervention.

The Translation Coordinator was responsible for exporting files, communicating with the agency, monitoring progress, receiving completed translations and importing the translated files back into WebTranslateIt. None of these tasks added value to the translations themselves, yet they consumed time during every release.

### Long Turnaround Time

The translation process typically took between three and four weeks from start to finish.

Only a small portion of this time was spent performing the translations. Most of the delay resulted from quotation requests, internal approvals, scheduling and agency turnaround time.

As a result, translations frequently became one of the final blockers before a release.

### Cost Structure

The localisation agency charged a minimum fee for each target language regardless of the number of strings requiring translation.

This pricing model worked reasonably well for large feature releases but became increasingly inefficient for maintenance releases containing only a handful of new strings.

In one release, the cost of translating a very small number of strings reached €182.70 purely because of the minimum per-language charge.

### Lack of Scalability

The workflow treated every release identically.

Whether ten strings or one thousand strings required translation, the same sequence of manual activities was followed.

This meant that operational effort remained almost constant whilst the amount of translation work varied significantly.

### Human Effort in Low-Value Activities

The Translation Coordinator spent considerably more time managing the process than performing any technical work.

Tasks such as exporting files, requesting quotations and uploading translated content were repetitive administrative activities that could potentially be automated without affecting translation quality.

## Key Observations

Reviewing the workflow highlighted several opportunities for improvement.

- The majority of the release timeline was consumed by coordination rather than translation.
- Manual file handling introduced unnecessary operational overhead.
- Translation costs were largely independent of the amount of work required.
- Small releases were disproportionately affected by the agency's pricing model.
- Human expertise was being used to manage process rather than validate translation quality.

These observations shaped the objectives for the hackathon project. Rather than attempting to replace professional translators entirely, the goal became much more focused:

**Automate the operational workflow whilst preserving human review as the final quality gate.**

# 5. Project Objectives

Having analysed the existing localisation workflow, it became clear that the challenge extended beyond translation itself. The project needed to address cost, turnaround time and operational efficiency without compromising translation quality or disrupting the existing release process.

Rather than building a proof of concept for AI translation, the objective was to demonstrate that AI could become a practical component of the software localisation workflow.

The project was therefore guided by the following objectives.

## Reduce Translation Turnaround Time

The existing translation process typically required three to four weeks from the moment new strings were exported until translated files were available for import.

The primary objective was to reduce this process to a matter of minutes, allowing translations to be generated on demand rather than becoming a release bottleneck.

## Reduce Operational Cost

The existing workflow relied on a professional translation agency whose pricing model included a minimum charge for each target language.

The solution should significantly reduce the cost of translating small and medium-sized batches of strings whilst maintaining an acceptable level of translation quality.

## Eliminate Manual Operational Work

Several stages of the existing workflow consisted entirely of repetitive manual tasks.

The project aimed to automate activities such as:

- Retrieving untranslated strings from WebTranslateIt.
- Identifying missing translations.
- Generating translated language files.
- Uploading translated files back into WebTranslateIt.

Removing these manual steps would simplify the responsibilities of the Translation Coordinator and reduce the likelihood of human error.

## Maintain Translation Quality

Reducing cost and turnaround time should not come at the expense of translation quality.

The generated translations should:

- Use consistent terminology.
- Preserve existing product language.
- Respect domain-specific vocabulary.
- Produce translations suitable for human review.

Professional-quality output remained the ultimate goal.

## Preserve the Existing Review Process

One of the project's guiding principles was that AI should assist translators rather than replace them.

For this reason, generated translations would be uploaded as **Unproofread** entries in WebTranslateIt.

This ensured that the existing review workflow remained unchanged, allowing human reviewers to validate translations before they became part of the product.

## Minimise Integration Effort

The solution should integrate with existing tooling wherever possible.

Rather than replacing WebTranslateIt or introducing a new localisation platform, the pipeline should operate alongside the current workflow, treating WebTranslateIt as the single source of truth.

This would reduce adoption effort and make future integration into the release process considerably simpler.

## Demonstrate Production Potential

Although the project was developed during a five-day hackathon, it was designed with production use in mind.

The objective was not merely to demonstrate that AI could translate text, but to show that an AI-assisted localisation pipeline could realistically replace large parts of the existing workflow for routine software releases.

---

## Success Criteria

The project would be considered successful if it could demonstrate the following:

- End-to-end automation of the localisation workflow.
- Significant reduction in translation turnaround time.
- Significant reduction in translation cost.
- Translation quality comparable to professionally translated content.
- Seamless integration with the existing WebTranslateIt workflow.
- Human reviewers remaining the final quality gate.

These objectives served as the foundation for every architectural and engineering decision described in the following chapters.

# 6. Solution Overview

The primary objective of FCM Smart Translate was not simply to translate text using AI. It was to redesign the localisation workflow so that translations could be generated automatically whilst remaining compatible with the existing release process.

Rather than replacing WebTranslateIt (WTI), introducing a new localisation platform or changing how translations were reviewed, the solution was designed to integrate seamlessly with the existing workflow. WTI continued to serve as the single source of truth for all localisation files, whilst AI became an additional service responsible for generating translation suggestions.

The resulting pipeline consists of five high-level stages.

```text
                 WebTranslateIt (WTI)
                         │
                         ▼
            Fetch untranslated language files
                         │
                         ▼
          Identify untranslated strings
                         │
                         ▼
     Generate AI translations for each language
                         │
                         ▼
       Create WTI-compatible language files
                         │
                         ▼
        Upload translations back to WTI
                 (Marked as Unproofread)
```

The entire workflow is executed using a single command. Once started, the pipeline performs every stage automatically, requiring no manual intervention until the translated strings are available in WebTranslateIt for review.

## Stage 1 – Retrieving Translation Files

The pipeline begins by communicating with the WebTranslateIt API.

For each localisation folder, it downloads the English source file together with all target language files. At this stage, no translation takes place. The objective is simply to obtain the latest localisation data directly from the source of truth.

Keeping WebTranslateIt as the authoritative source ensures that the pipeline always operates on the most recent version of every translation file.

## Stage 2 – Identifying Missing Translations

Once the language files have been retrieved, the pipeline compares the English source strings with each target language.

Any string that contains an empty or null value is considered untranslated and becomes a candidate for AI translation.

This approach ensures that the pipeline only processes new or missing translations, avoiding unnecessary work and reducing both execution time and token consumption.

## Stage 3 – AI Translation

The untranslated strings are then translated using Azure OpenAI.

Rather than translating individual strings in isolation, the pipeline processes one localisation folder at a time and translates the complete language file for each target language.

This approach allows the model to maintain greater consistency across related strings whilst reducing the number of API requests.

At this stage, additional contextual information is supplied to improve translation quality. This includes project-specific terminology, professionally translated examples, language-specific rules and other contextual information that will be discussed in later chapters.

## Stage 4 – Generating Translation Files

Once the translations have been generated, the results are converted into the format expected by WebTranslateIt.

This allows the translated files to be uploaded without requiring any changes to the existing localisation platform or release process.

By preserving the existing file structure, the solution remains compatible with current tooling and minimises integration effort.

## Stage 5 – Uploading to WebTranslateIt

Finally, the translated language files are uploaded back into WebTranslateIt using its API.

Rather than marking the translations as complete, every newly generated translation is uploaded with the status **Unproofread**.

This decision was intentional.

Human reviewers remain responsible for validating translations before they become part of the product, ensuring that AI augments the existing workflow rather than replacing it.

---

## Design Principles

Several design principles guided the implementation of the pipeline.

### Preserve Existing Tooling

The project was designed to complement the existing localisation process rather than replace it.

WebTranslateIt remained the single source of truth, allowing the solution to be introduced without disrupting existing workflows.

### Automate Repetitive Work

Every repetitive operational task performed by the Translation Coordinator was considered a candidate for automation.

This included exporting files, identifying untranslated strings, generating translations and uploading completed files.

Human involvement was intentionally reserved for reviewing translation quality rather than managing file transfers.

### Keep Humans in the Loop

Translation quality directly affects the user experience.

For this reason, the project deliberately retained the existing review process. AI-generated translations are suggestions rather than final output, allowing reviewers to approve, modify or reject translations before release.

### Optimise for Practicality

The project was developed during a five-day hackathon.

Rather than attempting to solve every localisation challenge, the focus was on building a practical end-to-end workflow capable of demonstrating immediate business value.

The architecture therefore prioritised simplicity, maintainability and seamless integration over unnecessary complexity.

---

> **Engineering Decision**
>
> One of the earliest architectural decisions was to keep WebTranslateIt at the centre of the workflow rather than replacing it.
>
> This significantly reduced implementation effort, avoided changes to the existing release process and made the prototype feel like an enhancement to the current system rather than an entirely new platform.

## Looking Ahead

Although the high-level workflow appears straightforward, producing reliable translations required considerably more engineering than simply calling an LLM API.

The following chapters explore the key architectural decisions that transformed a basic translation script into a practical AI-assisted localisation pipeline, including context engineering, prompt design, glossary management, translation memory, caching and token optimisation.