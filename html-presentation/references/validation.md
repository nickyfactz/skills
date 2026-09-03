# Validation Gate

Run these checks after HTML implementation and after material revisions.

## Content integrity

- Every major section in the approved plan exists, unless the user approved a later change.
- Visible copy reflects the current approved wording/intent.
- No sourced number, quote, attribution, date, result, or claim was invented during design.
- Citations/source drawer entries point to the intended sources.
- User-authored goals and opinions are not misrepresented as externally verified facts.

## Human-copy pass

Read every visible headline, subtitle, label, button, callout, and paragraph.

Rewrite generic filler, redundant framing, unsupported superlatives, robotic list language, and vague corporate phrasing. Check that the most important copy still sounds like the presenter's point of view.

## Offline/runtime pass

Core presentation must work when opened directly from disk.

Check for accidental runtime dependencies such as:

- `<script src="...">` to a remote library;
- remote stylesheet `<link>` elements;
- required remote fonts;
- hotlinked images required for layout or meaning;
- fetch/XHR calls required to populate presentation content.

Ordinary external `<a href>` resources are allowed.

## Navigation pass

In paged mode verify:

- left-rail click navigation;
- active state;
- previous/next keyboard navigation;
- URL hash update and direct hash loading;
- first/last section boundary behavior;
- no inactive section leaking into the active visual flow.

If a right drawer exists verify:

- open from all intended triggers;
- close button;
- Escape close;
- keyboard focus remains usable;
- scroll-to-advance at section boundaries, without interrupting scrollable section content;
- drawer content scrolls independently when long.

## Layout pass

Inspect at multiple useful browser sizes rather than a single 16:9 canvas. At minimum consider:

- common laptop width;
- 1080p projector/display;
- narrower window/tablet-like width.

Check:

- no unintended horizontal scrolling;
- type remains comfortably readable;
- navigation does not cover content;
- long sections scroll naturally;
- short sections do not look stranded at the top unless intentionally composed that way;
- diagrams and images scale without clipping;
- overlays/drawers remain within the viewport.

## Motion pass

- Animations do not delay live navigation.
- Repeated navigation does not leave elements in broken transient states.
- `prefers-reduced-motion: reduce` produces a complete, readable static experience.

## Browser pass

When tooling permits, open/render the file locally and inspect the actual output. Exercise the main interactions. Fix visible defects and rerun the relevant checks.

If the environment cannot open a browser, report code/static validation separately from visual validation.

## Delivery pass

- Use a filesystem-safe presentation name.
- Prefer `[presentation-name].html`.
- Use a ZIP only when size or unavoidable local media makes single-file delivery impractical.
- Do not claim the presentation was visually tested unless it was actually rendered/opened.
