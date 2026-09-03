# HTML Presentation Design

Use this reference only after the presentation plan is approved or the user explicitly requests direct HTML generation.

## Design stance

Treat the work as an interactive editorial experience, not a PowerPoint translated into HTML. The subject should determine the visual language. Pick a coherent direction before implementing components and carry it through typography, spacing, color, imagery, motion, and interaction.

A presentation may resemble a premium product launch page, digital museum exhibit, data story, technical explainer, visual essay, field guide, or another fitting web-native form. Avoid a generic dashboard made of interchangeable rounded cards unless the content truly calls for one.

## Default shell

Use a single document with:

- `<nav>` left rail containing presentation title/identity and section controls;
- `<main>` containing semantic `<section>` elements;
- exactly one active section visible in paged mode;
- an optional right `<aside>` drawer for sources, definitions, details, or resources;
- inline `<style>` and inline `<script>`;
- hash-addressable section IDs;
- responsive behavior for narrow windows.

The left rail should support direct jumping and active-state feedback. On smaller screens it may collapse into a compact control while preserving section navigation.

## Page feel without slide constraints

A section is a chapter-sized viewport, not a 16:9 canvas.

- Allow vertical scrolling inside an active section when the content or composition benefits from it.
- Presentation forward/back behavior should leverage standard inputs, scrolling on the siderail moves the section, clicking jumps to the clicked section, and arrow keys advance and revert.
- Keybind 'P' to toggle presentation mode, this collapses the side rail, when the rail is hidden a small UI toast informs the user how to expand it 'Press P for the rail' then fades out.
- Keep inactive sections out of the visual flow in paged mode so there are no accidental half-visible neighboring sections.
- Do not shrink type or compress composition merely to force content into one viewport.
- Use natural web dimensions and `min-height` rather than fixed slide ratios.
- Let hero sections breathe; let evidence-heavy sections extend.

## Content-specific components

Map information shape to visual form before coding. Potential forms include:

- annotated architecture diagrams;
- inline Scalable Vector Graphics (SVG) flows;
- layered system maps;
- timelines and eras;
- before/after transformations;
- interactive comparison toggles;
- expandable evidence cards;
- source-backed quote treatments;
- browser/device frames around screenshots;
- relationship networks;
- maturity ladders;
- process paths;
- metric canvases where numbers are genuinely central;
- image-led chapters;
- custom illustrations built from CSS/SVG;
- resource or footnote drawers.

Invent a component when the content has a shape the existing vocabulary does not express well.

## Aesthetic direction

Ground the design in the subject's own world: materials, interfaces, artifacts, diagrams, symbols, screenshots, environments, or cultural references. Choose palette and typography deliberately rather than reaching for default "AI" gradients or common startup styling.

Aim for one memorable signature moment: a strong opening composition, an orchestrated transition, a diagram that builds itself, a meaningful interaction, or another defensible visual risk.

## Typography

The file must remain offline-safe. Prefer system and locally available font stacks unless the user has explicitly supplied a distributable font asset and the environment permits embedding it. Do not require Google Fonts or another online font service.

Use a clear type scale with deliberate contrast between display, body, labels, and annotations. Long-form detail belongs in drawers or scrolled detail areas, not as tiny presentation text.

## Color and texture

Define a small token system with CSS custom properties. Colors should encode hierarchy and content where possible, not merely decorate components. Texture, gradients, shadows, glass, grain, borders, and background effects are optional tools; use only what supports the chosen direction.

## Motion

Use motion as choreography, not confetti.

- Favor a few intentional sequences over animation on every object.
- Connect motion to navigation, revealing structure, comparing states, or drawing attention.
- Support `prefers-reduced-motion` and provide an equivalent static state.
- Avoid motion that blocks navigation or forces the presenter to wait.

## Interaction

Interactions must be understandable without instructions during a live discussion.

Recommended patterns:

- click section in left rail;
- ArrowLeft / ArrowRight or PageUp / PageDown to navigate sections;
- Escape closes drawers/modals;
- clickable `Details`, citation, or resource affordances open the right drawer;
- optional expand/collapse within a section;
- hash updates make sections addressable.

Do not create interaction simply to prove the page is interactive.

## Offline single-file rules

Core rendering and navigation must work from a `file://` URL.

Prefer:

- inline CSS;
- vanilla JavaScript;
- inline SVG;
- CSS-generated decorative graphics;
- embedded data-URI images for manageable user-supplied assets.

External web URLs may appear as ordinary links. They are content destinations, not required dependencies.

If the user explicitly requests embedded online video, treat it as an optional online enhancement and make sure the rest of the presentation remains usable when offline. Large local video/audio assets may justify a ZIP rather than turning the HTML into an enormous base64 payload.

## Accessibility and robustness

- Use semantic elements and real buttons/links for controls.
- Keep keyboard focus visible.
- Supply useful alt text for meaningful images.
- Ensure sufficient contrast for primary reading text.
- Avoid horizontal overflow at common laptop and projector widths.
- Preserve usable zoom behavior.
- Keep JavaScript simple enough to survive direct local opening in mainstream browsers.

