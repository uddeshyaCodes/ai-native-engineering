# Project Report

# Project 001 — FCM Smart Translate

> Internal Hackathon Project (5 Days)

---

# Project Information

| Field | Value |
|--------|-------|
| Project Name | FCM Smart Translate |
| Type | Internal Hackathon Project |
| Duration | 5 Days |
| Status | Working Prototype |
| My Roles | Front-end Engineer, Translation Coordinator, Solution Designer |
| Team | 2 Front-end Engineers, 1 QA Engineer |
| Technologies | Node.js, TypeScript, React, Azure OpenAI, WebTranslateIt API, Cursor |
| AI Model | GPT-4o (Azure OpenAI) |
| Purpose | Automate the localisation workflow whilst keeping human review in place |

---

# Executive Summary

FCM Smart Translate is an AI-assisted localisation pipeline built during an internal five-day hackathon.

The project automatically:

- Fetches localisation files from WebTranslateIt
- Identifies untranslated strings
- Translates them using Azure OpenAI
- Generates WebTranslateIt-compatible language files
- Uploads them back into WebTranslateIt
- Marks translations as **Unproofread**, allowing the existing review process to continue

The objective was never to replace professional translators.

Instead, the goal was to automate the repetitive operational work surrounding translations, reduce translation costs and turnaround time, and allow human reviewers to focus on validation rather than translation.

The prototype demonstrated that an AI-assisted workflow could produce translations comparable to professionally translated content whilst significantly reducing both cost and processing time.

---

# Background

I recently became the Translation Coordinator for my project.

Alongside my existing Front-end development responsibilities, I became responsible for managing software localisation. This involved coordinating with an external professional translation agency, preparing translation files, requesting quotations, receiving translated files and uploading them back into WebTranslateIt (WTI).

After taking over the responsibility, I started reviewing the translation process used in previous releases.

Although the workflow was functional, it was highly manual, expensive and slow.

Every release required multiple manual steps and depended on an external translation agency regardless of how many new strings actually required translation.

Looking through the previous three releases revealed something interesting.

One release cost approximately **€182.70** despite containing only a relatively small number of new strings. The majority of the cost came from the agency's minimum pricing policy rather than the amount of work involved.

Because of this pricing model, the following two releases were not translated at all. There were simply not enough new strings to justify the minimum agency charges.

This became the motivation behind the hackathon project.

Rather than accepting the workflow as a fixed process, I started asking whether recent advances in Large Language Models could automate the translation workflow whilst maintaining acceptable translation quality.

---

# Problem Statement

The existing localisation process suffered from several issues.

## Manual workflow

Every release required:

- Exporting untranslated files
- Requesting quotations
- Waiting for approvals
- Waiting for agency turnaround
- Receiving translated files
- Uploading translations back into WTI

Most of these activities were administrative rather than technical.

---

## Long turnaround

The complete translation process usually took around three to four weeks.

Most of this time was spent waiting rather than translating.

Translations regularly became one of the last blockers before a release.

---

## High operational cost

The translation agency charged a minimum amount for each supported language.

Small releases therefore became disproportionately expensive.

In some cases, the cost of coordinating translations exceeded the value of the translations themselves.

---

## Poor scalability

The same workflow was followed whether translating:

- 10 strings
- 100 strings
- 1000 strings

Operational effort remained almost constant regardless of workload.

---

## Human effort spent on low-value tasks

The Translation Coordinator spent significantly more time:

- exporting files
- uploading files
- communicating with the agency

than performing activities directly related to translation quality.

---

# Why This Problem Was Worth Solving

The problem was already recognised within the team.

Previous Translation Coordinators had experienced similar frustrations and expressed similar concerns regarding both cost and operational overhead.

As the current Translation Coordinator, I experienced these issues first-hand.

The hackathon provided an opportunity to explore whether AI could remove the repetitive administrative work whilst preserving human review.

---

# Why We Chose This Idea

The team brainstormed multiple ideas.

Ultimately, we chose this one because:

- it solved a real business problem
- the impact was measurable
- the current process was expensive
- improvements could immediately benefit future releases
- it aligned well with recent advances in LLM capabilities

Unlike many hackathon projects, this idea originated from an operational pain point rather than curiosity about AI itself.

---

# Team

The project was completed by a team of three.

## Me

Roles:

- Translation Coordinator
- Front-end Engineer
- Solution Designer

Responsibilities:

- originated the project idea
- designed the overall architecture
- implemented the translation pipeline
- integrated WebTranslateIt APIs
- designed prompt strategy
- created project glossary
- implemented glossary optimisation
- designed translation memory
- implemented translation cache
- added language rules
- optimised token usage
- prepared presentation slides
- delivered final hackathon presentation

---

## Front-end Engineer

Responsibilities:

- prompt engineering support
- language rule improvements
- benchmark UI
- comparison tooling

---

## QA Engineer

Responsibilities:

- glossary preparation
- testing
- validation
- translation verification

---

# Technologies Used

Programming

- Node.js
- TypeScript

AI

- Azure OpenAI
- GPT-4o

Frontend

- React

External Services

- WebTranslateIt API

Development Tools

- Cursor
- ChatGPT

---

# High-Level Solution

The solution automates the localisation workflow whilst preserving the existing review process.

Pipeline:

Developer adds new UI strings

↓

Pipeline fetches localisation files from WebTranslateIt

↓

Pipeline identifies untranslated strings

↓

Azure OpenAI translates missing strings

↓

Pipeline generates WTI-compatible files

↓

Pipeline uploads translations back to WTI

↓

Strings appear as **Unproofread**

↓

Human reviewer validates translations

---

# Design Principles

The project was guided by several principles.

## Keep humans in the loop

AI generates translations.

Humans approve them.

---

## Preserve existing tooling

WTI remains the source of truth.

No existing workflow needs to change.

---

## Automate repetitive work

Everything repetitive should be automated.

Everything requiring judgement should remain human.

---

## Optimise for practicality

The goal was not to build a perfect translator.

The goal was to build something that could realistically integrate into the release process.

---

# My Contributions

This was the area where I contributed most.

## Product

- Identified the business problem
- Proposed the hackathon idea
- Defined project scope

---

## Architecture

- Designed the complete pipeline
- Designed translation workflow
- Designed AI interaction

---

## Backend

Implemented:

- WTI fetch
- translation pipeline
- upload pipeline
- glossary injection
- translation memory
- translation cache
- language rules
- token optimisation

---

## Localisation

Created:

- project glossary
- terminology rules
- protected terms
- translation guidance

---

## Presentation

- created architecture diagrams
- created presentation slides
- presented final demo

---

# Success Criteria

The project would be considered successful if it could:

- automate the complete localisation workflow
- reduce operational cost
- reduce turnaround time
- maintain translation quality
- integrate with WebTranslateIt
- preserve human review
- demonstrate production potential

---

# System Architecture

## Overview

FCM Smart Translate was designed as a standalone automation tool.

The initial prototype is manually triggered using a single command, making it easy to run whenever translations are required. Although the current implementation is independent of the product release pipeline, the long-term vision is to integrate it into the release workflow so that translations can be generated automatically whenever new strings are added.

The system was intentionally designed to complement the existing localisation process rather than replace it.

WebTranslateIt (WTI) remains the single source of truth for all localisation files, whilst Azure OpenAI is responsible only for generating translation suggestions.

---

## High-Level Architecture

```
                 WebTranslateIt (WTI)
                         │
                         │ Fetch localisation files
                         ▼
                Translation Pipeline
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
Identify missing   Build AI Context   Translation Cache
translations        (Glossary + TM)
        │                │
        └────────────────┼────────────────┐
                         ▼
                  Azure OpenAI
                         │
                  AI Translation
                         │
                         ▼
            Generate WTI-compatible files
                         │
                         ▼
              Upload back to WebTranslateIt
               (Status = Unproofread)
```

---

# Translation Pipeline

The pipeline consists of five stages.

## Stage 1 – Fetch localisation files

The process begins by downloading localisation files from WebTranslateIt.

Each localisation folder contains:

- one English master file
- six target language files

The pipeline processes one folder at a time.

For every folder, the English file and all corresponding language files are downloaded before translation begins.

---

## Stage 2 – Identify untranslated strings

The English master file is compared against each target language.

A string is considered untranslated if:

- its value is null
- its value is empty

Only untranslated strings are selected for AI translation.

Already translated strings are ignored.

This reduces both execution time and token consumption.

---

## Stage 3 – Build translation context

Before calling the LLM, additional context is assembled.

The context consists of several components:

- project description
- translation prompt
- project glossary
- translation memory
- language rules
- translation cache

Together, these provide the model with enough information to generate translations that are consistent with the existing product terminology.

---

## Stage 4 – Generate translations

Azure OpenAI translates the selected strings.

Translation occurs:

- one localisation folder at a time
- one target language at a time
- for the entire file rather than individual strings

Translating an entire file improves consistency between related strings and reduces the number of API requests.

---

## Stage 5 – Upload translations

Once translation is complete:

- language files are generated
- files are converted into the format expected by WTI
- uploaded through the WTI API
- newly translated strings are marked as **Unproofread**

This allows the existing review workflow to remain unchanged.

---

# Prompt Engineering

Prompt engineering evolved continuously throughout the hackathon.

The first prompt was intentionally simple.

It instructed the model to act as a professional software translator and provided a brief description of the product.

Although the translations were understandable, they lacked consistency and frequently produced undesirable results.

Examples included:

- incorrect terminology
- inconsistent wording
- translating terms that should never be translated
- inconsistent tone between files

Rather than repeatedly tweaking the wording of the prompt, we gradually realised that the missing piece was context.

This became one of the biggest lessons from the project.

Prompt quality improved primarily because better context was supplied to the model rather than because the prompt itself became significantly more sophisticated.

---

## Prompt Evolution

### Version 1

Basic translator prompt.

Result:

- understandable
- generic
- inconsistent

---

### Version 2

Added project glossary.

Result:

- improved terminology
- significantly increased token usage

---

### Version 3

Added translation memory.

Result:

- improved consistency
- translations better matched previous agency output

---

### Version 4

Added language-specific rules.

Result:

- fewer incorrect translations
- better handling of special terminology

---

### Version 5

Added project context.

Result:

- better understanding of the product
- more appropriate translation style

---

### Version 6

Optimised glossary injection and introduced translation cache.

Result:

- lower token usage
- improved consistency
- better overall quality

---

# Context Engineering

One of the most important discoveries during the project was that translation quality depended far more on context than on prompt wording.

Instead of relying solely on a carefully written prompt, the pipeline assembled several sources of contextual information before each translation request.

These included:

- project description
- intended users
- UI localisation context
- project glossary
- professionally translated examples
- language rules
- previously generated translations

Each addition improved translation quality whilst reducing ambiguity.

This shifted the focus from prompt engineering towards context engineering.

---

# Project Context

Every request explained:

- what the product is
- who the end users are
- that translations are intended for software UI
- expected translation style
- formatting expectations

Providing this information reduced generic translations and produced wording that better matched the product.

Future improvements could include supplying component-level context such as:

- button labels
- menu items
- settings pages
- dialog titles

to further improve translation accuracy.

---

# Dynamic Glossary Retrieval

The project glossary contains approximately:

- 145 project-specific terms
- professionally translated into all supported languages

The glossary was stored as a JSON file.

Initially, the entire glossary was injected into every prompt.

Although this improved translation quality, it dramatically increased token consumption.

The glossary contains more than 1,300 lines.

Including it in every request quickly became impractical.

---

## Optimisation

Instead of injecting the complete glossary, only relevant entries are selected.

For every untranslated string:

- keywords are extracted
- glossary entries containing those keywords are selected
- only matching entries are included in the prompt

Example:

Input:

```
Vibration Velocity
```

Relevant glossary entries:

- vibration
- velocity

Only those entries are injected.

This significantly reduced prompt size whilst preserving most of the benefits of the glossary.

---

## Future Improvements

Current filtering is keyword-based.

Future versions could use:

- semantic search
- embeddings
- vector databases

to retrieve more relevant glossary entries automatically.

---

# Translation Memory

Translation memory was introduced to improve consistency.

When localisation files are downloaded, the first fifty professionally translated strings are extracted from the target language file.

These examples are then supplied to the model as reference translations.

The objective is to encourage the model to follow the same terminology and writing style already present within the product.

Initially, we considered providing the entire translation file.

However, this dramatically increased token consumption.

Restricting the memory to fifty examples provided a better balance between quality and cost.

---

## Current Limitations

The first fifty translated strings are selected regardless of relevance.

This works reasonably well but is not optimal.

Future improvements could include:

- semantic similarity
- keyword filtering
- retrieving examples from multiple localisation files

rather than relying solely on the current file.

# Cross-file Translation Cache

## Motivation

During development, we realised that many UI strings appeared repeatedly across different localisation files.

Examples included:

- Save
- Cancel
- Settings
- Status
- Configuration
- Device
- Sensor

Without any caching mechanism, these strings would be translated repeatedly, resulting in unnecessary API calls, higher token consumption and inconsistent wording.

Although each translation request was independent, many strings had already been translated earlier in the pipeline.

Reusing these translations became an obvious optimisation.

---

## Implementation

After completing the translation of a localisation file, the generated translations are stored in a temporary in-memory cache.

Before sending a new translation request, the pipeline checks whether the same English string has already been translated earlier in the execution.

If a cached translation exists:

- the cached translation is reused
- the string is excluded from the AI request

If no cached translation exists:

- the string is sent to Azure OpenAI
- the generated translation is added to the cache

---

## Benefits

The cache provided several advantages.

### Reduced API usage

Previously translated strings no longer required additional API calls.

---

### Reduced token consumption

Fewer strings needed to be included in prompts.

---

### Faster execution

Less work was performed by the model.

---

### Better consistency

Repeated strings always used identical translations.

Although the reduction in token usage was relatively small, consistency improved noticeably.

---

## Future Improvements

The current cache exists only during a single execution.

Future improvements could include:

- persistent cache
- shared cache between releases
- similarity matching instead of exact matching

---

# Language Rules

Generic translation alone was insufficient for producing production-quality output.

Certain words within the product required specific handling.

Some terms should always be translated in a particular way.

Others should never be translated at all.

Language-specific rules were therefore introduced to guide the model.

Examples included:

- protected product terminology
- formatting expectations
- terminology preferences
- words that should remain in English

These rules reduced incorrect translations and improved consistency across languages.

The rules continued to evolve throughout the hackathon as additional edge cases were discovered.

---

# Token Optimisation

Token consumption became one of the biggest engineering challenges during development.

Initially, our focus was entirely on improving translation quality.

Whenever the model produced an incorrect translation, the natural response was to provide more context.

Over time, the prompt accumulated:

- project description
- glossary
- translation memory
- language rules
- formatting instructions

Whilst this improved quality, prompt size increased significantly.

Eventually, token usage became an engineering problem in its own right.

---

## Optimisations Introduced

Several optimisations were implemented.

### Dynamic glossary retrieval

Instead of sending the complete glossary, only relevant entries were included.

---

### Limited translation memory

Only fifty professionally translated examples were used.

---

### Translation cache

Repeated strings were not translated again.

---

### Translate only missing strings

Existing translations were ignored.

---

### Folder-by-folder processing

The pipeline translated one localisation folder at a time.

This kept requests smaller and easier to manage.

---

## Key Lesson

Adding more context improves quality.

Adding unnecessary context increases cost.

Finding the right balance became one of the most important engineering decisions throughout the project.

---

# Benchmark UI

During the hackathon we built a simple React application to compare AI-generated translations against professionally translated content.

The benchmark UI allowed us to:

- compare translations side-by-side
- evaluate consistency
- identify incorrect terminology
- demonstrate the solution during the final presentation

This proved valuable both for internal evaluation and for presenting the project to judges.

---

# Engineering Challenges

Several challenges emerged during development.

---

## Translation Quality

The earliest prompts produced generic translations.

Many translations were technically correct but failed to match the terminology and style already used within the product.

This led to the introduction of:

- glossary
- translation memory
- language rules
- project context

---

## Token Consumption

Every quality improvement increased prompt size.

Balancing translation quality against API cost became one of the project's biggest challenges.

Many later improvements focused on reducing tokens without sacrificing quality.

---

## Consistency

The same English string should always produce the same translation.

Initially this was not always the case.

Translation memory, glossary improvements and translation cache significantly improved consistency.

---

## Limited Time

The project was completed during a five-day hackathon.

Many implementation decisions favoured simplicity and practicality over long-term optimisation.

Several ideas were deliberately postponed for future work.

---

# Results

The prototype successfully demonstrated an end-to-end AI-assisted localisation workflow.

Achievements included:

- fully automated translation pipeline
- successful WebTranslateIt integration
- automatic upload of translated files
- preservation of existing review workflow
- translation quality comparable to agency output
- significantly reduced turnaround time
- substantial reduction in operational cost

The benchmark demonstrated that many AI-generated translations closely matched professionally translated strings.

Most importantly, the complete workflow functioned successfully from start to finish.

---

# Feedback

The project received positive feedback during the hackathon.

Judges recognised that the project addressed a genuine business problem rather than demonstrating AI for its own sake.

The ability to integrate with the existing release process was viewed positively.

There was interest in exploring whether the solution could eventually become part of the product's localisation workflow.

As the current Translation Coordinator, this is the aspect of the project I am most excited about.

---

# Lessons Learned

## AI is only one part of the solution.

The majority of the engineering effort was spent designing the workflow surrounding the model.

---

## Context matters more than prompts.

Translation quality improved primarily because better context was supplied rather than because the prompt wording changed dramatically.

---

## Cost engineering is AI engineering.

Token consumption became a first-class engineering concern.

Optimising prompts and reducing unnecessary context was just as important as improving translation quality.

---

## Human review remains essential.

AI-generated translations should be reviewed before becoming part of the product.

Maintaining the existing review process increased confidence in the solution.

---

## Build around existing workflows.

The project succeeded because it enhanced the current localisation process instead of attempting to replace it.

Keeping WebTranslateIt as the source of truth made adoption considerably easier.

---

# Future Improvements

Several improvements were identified during the hackathon.

## Smarter Translation Memory

Instead of always selecting the first fifty translated strings:

- retrieve semantically similar examples
- search across multiple localisation files

---

## Semantic Glossary Retrieval

Replace keyword matching with:

- embeddings
- vector search
- semantic retrieval

---

## Persistent Translation Cache

Store translations between releases.

Avoid retranslating identical strings across future versions.

---

## Automatic Pipeline Trigger

Instead of manual execution, integrate the pipeline into the release process.

Possible triggers include:

- pull requests
- release branches
- scheduled jobs

---

## Fine-tuned Internal Model

Investigate whether a smaller in-house model could:

- reduce operational cost
- improve domain-specific terminology
- remove dependency on external APIs

---

# Personal Reflection

This project changed the way I think about AI software development.

Before the hackathon, I had primarily used tools such as ChatGPT and Cursor to assist with coding.

This project was my first opportunity to build an application where an LLM became part of the product itself.

One of the biggest surprises was how much engineering work exists around the model.

Calling the API was straightforward.

Designing a system capable of producing reliable, consistent and cost-effective translations was considerably more challenging.

Cursor significantly accelerated implementation.

Many routine coding tasks that would previously have taken hours were completed much more quickly, allowing more time to focus on architecture, experimentation and prompt design.

Looking back, the project reinforced an important lesson.

Building AI applications is not primarily about choosing a model.

It is about designing the surrounding system.

---

# Key Statistics

Duration

- 5 days

Team

- 3 members

Supported languages

- 6

Glossary

- approximately 145 project-specific terms

Glossary size

- more than 1,300 lines

Translation memory

- first 50 professionally translated strings

Pipeline trigger

- manual

Review status

- Unproofread

---

# My Primary Contributions

- Identified the business problem
- Proposed the project
- Led technical design
- Designed system architecture
- Implemented translation pipeline
- Integrated WebTranslateIt
- Built prompt strategy
- Created project glossary
- Implemented glossary optimisation
- Designed translation memory
- Designed translation cache
- Added language rules
- Optimised token consumption
- Prepared presentation
- Delivered final demo

---

# Potential Article Topics

- Building an AI-assisted localisation pipeline in five days
- Lessons from building my first LLM application
- Why context engineering matters more than prompt engineering
- Reducing localisation costs with AI
- Optimising token usage in production LLM workflows
- Designing AI systems around existing business processes
- What I learned as a Translation Coordinator building an AI workflow

---

# One-Sentence Summary

FCM Smart Translate demonstrates how carefully engineered context, workflow automation and human review can transform a costly manual localisation process into a practical AI-assisted pipeline.

---

# Appendix A — Hackathon Timeline

## Day 1

### Objectives

- Finalise the project idea
- Understand the WebTranslateIt APIs
- Design the high-level architecture
- Build an initial proof of concept

### Completed

- Agreed on the problem statement
- Decided to automate the existing localisation workflow
- Designed the overall pipeline
- Investigated the WTI APIs
- Built the first version of the translation pipeline

### Challenges

- Understanding the WTI API structure
- Deciding how AI should fit into the workflow

---

## Day 2

### Objectives

- Connect Azure OpenAI
- Generate the first AI translations
- Evaluate translation quality

### Completed

- Connected Azure OpenAI
- Generated the first translations
- Began evaluating translation quality

### Challenges

- Generic translations
- Incorrect terminology
- Inconsistent wording

### Key Learning

A simple prompt was not sufficient.

---

## Day 3

### Objectives

- Improve translation quality
- Introduce project-specific context

### Completed

- Created the project glossary
- Injected glossary into prompts
- Added project context
- Improved terminology

### Challenges

Prompt size increased dramatically.

Token consumption became a major concern.

### Key Learning

Quality improved, but at an unacceptable cost.

---

## Day 4

### Objectives

- Improve consistency
- Reduce incorrect translations

### Completed

- Added translation memory
- Added language-specific rules
- Improved glossary
- Improved prompt structure

### Challenges

Balancing translation quality with token usage.

### Key Learning

Context mattered more than prompt wording.

---

## Day 5

### Objectives

- Optimise the solution
- Prepare final demonstration

### Completed

- Implemented translation cache
- Reduced token usage
- Built benchmark UI
- Prepared presentation
- Presented the project

### Outcome

The complete pipeline worked end-to-end.

Positive feedback was received from judges and colleagues.

---

# Appendix B — Engineering Decisions

## Why WebTranslateIt remained the source of truth

Replacing the existing localisation platform would have introduced unnecessary complexity.

The objective was to improve the workflow rather than replace it.

---

## Why translations are uploaded as Unproofread

Human review remains an essential quality gate.

Keeping reviewers in the process increases confidence in AI-generated translations.

---

## Why process one localisation folder at a time

Advantages:

- smaller requests
- lower token usage
- simpler debugging
- better translation consistency

---

## Why use a JSON glossary

JSON is:

- easy to edit
- version-controlled
- lightweight
- easy to search
- language independent

---

## Why only the first 50 translated strings

Using the complete file significantly increased token consumption.

Fifty examples provided a reasonable balance between quality and cost during the hackathon.

---

## Why keyword filtering instead of semantic search

Keyword filtering was:

- simple
- quick to implement
- sufficient for the prototype

Semantic retrieval was identified as future work.

---

# Appendix C — Major Challenges

| Challenge | Solution |
|-----------|----------|
| Generic translations | Added project context |
| Incorrect terminology | Created glossary |
| Inconsistent wording | Translation memory |
| High token usage | Dynamic glossary retrieval |
| Repeated translations | Translation cache |
| Terms translated incorrectly | Language rules |
| Manual workflow | End-to-end automation |

---

# Appendix D — Future Roadmap

## Short Term

- Better glossary filtering
- Smarter translation memory
- Better project context
- Improved language rules

---

## Medium Term

- Semantic glossary retrieval
- Persistent translation cache
- Automatic execution
- Better benchmarking

---

## Long Term

- Fine-tuned internal LLM
- Embedding-based retrieval
- Release pipeline integration
- Human feedback learning
- Translation quality scoring

---

# Appendix E — Key Lessons

## Technical

- Context is more important than prompt wording.
- Translation quality depends on the surrounding system.
- Token optimisation is a core engineering problem.
- Small engineering improvements compound.
- Human review should remain part of the workflow.

---

## Product

- Solve a real business problem.
- Build around existing workflows.
- Reduce friction before replacing systems.
- Practical solutions create more impact than perfect ones.

---

## Personal

This was my first project where an LLM became part of the product rather than simply assisting me with development.

The biggest surprise was that integrating the model was straightforward.

Designing everything around the model was the real engineering challenge.

The project changed how I think about AI software engineering.

---

# Appendix F — Questions for Future Interviews

## Explain the project in one minute.

(Use the Executive Summary.)

---

## What problem were you solving?

High localisation cost, manual workflow and long turnaround times.

---

## Why AI?

Because translation is a language problem, and modern LLMs perform well when provided with sufficient context.

---

## Biggest engineering challenge?

Balancing translation quality with token consumption.

---

## Biggest lesson?

Context engineering contributed more to translation quality than prompt engineering.

---

## What would you improve next?

Semantic retrieval, persistent cache, release integration and improved translation memory.

---

# Appendix G — Supporting Assets

Store the following alongside this document.

- Presentation slides
- Architecture diagrams
- Pipeline diagrams
- Benchmark UI screenshots
- Demo screenshots
- Prompt versions
- Example glossary
- Example translation memory
- Token optimisation examples
- Before/after translation comparisons
- Cost comparison
- Future architecture sketches

---

# One-Sentence Summary

FCM Smart Translate is an AI-assisted localisation pipeline that automates the repetitive translation workflow whilst preserving human review, reducing operational cost and demonstrating how carefully engineered context can produce high-quality software translations.

---

# Five Key Takeaways

1. AI should enhance existing workflows before attempting to replace them.

2. Context engineering had a greater impact on translation quality than prompt engineering.

3. Token optimisation became one of the primary engineering challenges during development.

4. Human review remained a deliberate architectural decision rather than a limitation.

5. The success of the project came from solving a real operational problem rather than building an AI demo.