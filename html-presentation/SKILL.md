---
name: html-presentation
description: Turn a raw brain dump into a reviewed presentation plan, then a standalone single-file HTML presentation.
disable-model-invocation: true
---

# HTML Presentation

Build web-native presentations from raw human input. The default workflow is **brain dump → presentation plan → human review loop → HTML → validation**.

This is not a slide-deck generator. Treat the browser as the presentation medium: sections may scroll, components may expand, evidence may live in drawers, and motion may support the story. Preserve a clear page/section feel so the presenter can move backward and forward without exposing unrelated sections.

## 1. Intake

Accept any mixture of prose, notes, file paths, URLs, facts, goals, examples, images, existing decks, brand material, constraints, or partial ideas. Do not require the user to pre-organize the input.

If the invocation contains enough material to infer a presentation topic and purpose, start synthesis. If `/html-presentation` is invoked without usable material, ask for a brain dump or a source file and briefly explain that rough, unstructured input is expected.

Resolve only gaps that block useful synthesis. Prefer explicit assumptions in the plan over an intake questionnaire.

**Complete when:** you can state the likely audience, presentation goal, core subject, and any material constraints without inventing facts.

## 2. Synthesize the review artifact

Read `references/plan-contract.md` and produce a standalone Markdown presentation plan using that contract.

Research or inspect supplied resources when tools and access permit. Preserve provenance for factual claims. Never manufacture a source, metric, quote, outcome, or attribution to make the story stronger.

The plan is the editable contract between the human and the HTML implementation. Keep visible presentation copy intentionally light. Put supporting detail, provenance, speaker context, and optional deep dives outside the visible-copy fields.

At the end of the plan, propose one coherent visual direction grounded in the subject rather than default corporate styling.

Return the plan to the user and explicitly ask them to review, edit, reorder, delete, or add to it. Tell them they may edit the Markdown directly and return it. Do not treat first-pass synthesis as approval.

**Complete when:** every proposed section has a purpose, visible-content intent, visual/interaction idea, supporting context, and source provenance where relevant; the user has a concrete artifact they can edit.

## 3. Run the review loop

Treat user edits as authoritative intent. Reconcile them into the plan while preserving source truth and narrative coherence.

Repeat as many times as needed. Do not rush toward HTML because later steps are visible. Each revision should leave one clean current plan rather than an accumulating conversation diff.

When revising visible copy, read `references/human-copy.md`. Preserve the user's vocabulary, opinions, emphasis, and level of formality. Presentation copy should feel edited by a strong human communications or product-marketing team, not expanded by an assistant.

If changes create factual uncertainty, mark the uncertainty in the plan instead of smoothing it over.

Move to HTML when the user explicitly approves the plan, says it is ready, asks to build/render the HTML, or clearly requests an override of the review gate.

**Complete when:** there is one current plan and the user has signaled that implementation may begin.

## 4. Design the HTML presentation

Before coding, read `references/html-design.md` and `references/frontend-design.md`. If the presentation contains sourced claims, external resources, or deep-dive material, also read `references/source-handling.md`. If the plan carries talking points for the presenter and the talk has a time budget, also read `references/speaker-notes.md` and build the notes window.

Implement the approved plan as one `.html` file with inline CSS and inline JavaScript. The file must open directly from local disk without a server or backend.

Default interaction model:

- Persistent left navigation rail for sections.
- One active section/page in focus at a time.
- Section content may scroll vertically when the design benefits from it.
- Navigation changes the active section rather than creating accidental cross-section page breaks.
- Keyboard navigation and URL hashes mirror section navigation.
- Wheel/trackpad scrolling stays within an active section while it has remaining scroll range; an outward scroll at the top or bottom boundary moves to the previous or next section. Do not advance when the pointer is over the navigation rail or an open drawer.
- Supporting details, citations, definitions, and resources may open in a right-side drawer.
- Continuous/infinite-scroll mode is opt-in when the user asks for it or the approved plan clearly calls for it.

Use the browser's strengths: responsive composition, inline SVG, diagrams, expandable cards, layered imagery, purposeful motion, annotated screenshots, timelines, comparisons, interactive reveals, and spatial storytelling. Invent content-specific components when generic cards weaken the idea.

Keep the core presentation independent of network access. External links are allowed as destinations, not runtime dependencies. Do not depend on a Content Delivery Network (CDN), web font, hosted JavaScript library, remote stylesheet, or remote image for the presentation to render correctly.

Name the deliverable from the approved presentation title using a filesystem-safe name, for example `identity-assurance-strategy.html`.

**Complete when:** the approved narrative and visual direction are represented in a working local single-file HTML presentation.

## 5. Validate before delivery

Read `references/validation.md` and apply every applicable check. Fix failures before declaring completion.

At minimum verify: local-file operation, section navigation, keyboard navigation, drawer behavior when present, responsive layout, reduced-motion behavior, source links, absence of accidental runtime dependencies, no fabricated claims, and a human-copy pass on every visible headline/label/paragraph.

If the environment can render or open the file, inspect it visually rather than relying only on code review. If rendering is unavailable, state that limitation without pretending visual validation occurred.

If a single HTML artifact is impractically large for delivery, package the HTML and any unavoidable local media in a `.zip`; otherwise prefer the single HTML file.

**Complete when:** the file passes the applicable validation checks and the user receives the artifact with its final filename.

## Editing an existing presentation

When the user supplies an existing HTML presentation, preserve untouched sections unless the request calls for a broader redesign. Read the current structure first, identify the affected sections/components, then apply the same copy, design, source, and validation rules above.
