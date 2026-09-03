# Presentation Plan Contract

Use this file when converting raw input into the Markdown artifact the human reviews before HTML implementation.

The plan is intentionally richer than the final visible presentation. It separates **what the audience sees** from **what the presenter/agent needs to know**.

## Output shape

Use this structure unless the content genuinely needs a different one:

```markdown
# [Presentation title]

## Presentation intent
- **Audience:**
- **Goal:**
- **Desired outcome:**
- **Presenter stance:** what the presenter believes / wants the room to understand
- **Format:** paged sections | continuous scroll
- **Estimated discussion length:** only if known or useful

## Thesis
[One or two sentences describing the central idea or promise of the presentation.]

## Narrative arc
[Short explanation of why the sections occur in this order and where the major turns are.]

## Source ledger
[S1] URL / file / supplied statement — what it supports — confidence or caveat if needed
[S2] ...

## Sections

### 01 — [Human-facing section name]
- **Job:** what this section must accomplish in the room
- **Audience takeaway:** one sentence
- **Visible headline:** proposed on-screen language
- **Visible support:** 0–4 concise supporting items, labels, or short lines
- **Visual treatment:** diagram / hero image / annotated screenshot / timeline / comparison / spatial layout / custom idea
- **Interaction:** none / reveal / expand / toggle / drawer / embedded media / other
- **Deep-dive drawer:** optional material that should be available but not compete with the main visual layer
- **Talking points:** presenter context, detail, nuance, examples
- **Evidence:** [S1], [S3] or `user-supplied / unsourced` as appropriate
- **Transition:** what idea naturally moves the discussion into the next section

[Repeat for each section]

## Design direction
- **Concept:** one coherent visual thesis grounded in the subject
- **Mood:**
- **Palette:** role-based description; exact values are optional at planning time
- **Typography:** desired character, not a dependency on online fonts
- **Composition:** how density, whitespace, imagery, and component scale should feel
- **Motion:** one or two purposeful motion motifs
- **Navigation feel:**
- **Imagery / diagrams:**
- **Signature moment:** one memorable visual or interaction worth taking a design risk on
- **Avoid:** content-specific design traps, not generic taste rules

## Open questions / assumptions
[Only unresolved items that could materially change content or design.]

## Parking lot
[Useful details intentionally excluded from the primary visual narrative; candidates for speaker notes, source drawer, appendix-like sections, or removal.]
```

## Planning rules

### Organize the human; do not sanitize them

The brain dump is source material, not bad writing that needs to be normalized. Recover the user's thesis, priorities, vocabulary, tension, examples, and desired outcome. Keep strong or idiosyncratic language when it carries meaning.

### Separate layers

Keep these distinct:

1. **Visible layer** — what should be readable in the presentation during discussion.
2. **Presenter layer** — nuance, examples, objections, and explanation.
3. **Evidence layer** — sources and provenance.
4. **Optional layer** — details available through a drawer, expansion, or linked resource.

A dense brain dump should usually make the presenter/evidence layers richer, not the visible layer denser.

### Headline test

Prefer headlines that make a claim, frame a question, or create tension. Topic labels are acceptable only when the section is genuinely navigational.

### Visual-first mapping

Before choosing bullets, classify the information shape. Examples:

- Change over time → timeline / progressive scene / animated path
- Before vs after → comparison / split composition
- Architecture → layered system diagram
- Process → flow / staged journey
- Portfolio → map / constellation / clustered landscape
- Evidence → annotated artifact / data visual / quote with context
- One decisive idea → oversized statement / image-led hero
- Many optional details → compact focal layer + drawer/expandable details

Do not force every section through the same card grid.

### Density

The visible layer is for projection and discussion, not document completeness. Prefer fewer, stronger pieces of copy with large visual hierarchy. Move secondary explanation to talking points or the deep-dive drawer.

### Sources

Every factual claim that depends on supplied research should be traceable to the source ledger. It is acceptable for user-authored goals, opinions, plans, and internal statements to be marked as user-supplied rather than externally sourced.

### Review handoff

After producing the plan, explicitly tell the user:

- this is the editable pre-HTML artifact;
- they can change wording, ordering, section boundaries, emphasis, visuals, and omissions directly;
- they should return the edited Markdown or describe changes;
- HTML implementation starts after they indicate the plan is ready.
