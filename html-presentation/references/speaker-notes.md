# Speaker notes window

A second browser window that follows the deck, shows the presenter layer for the current section, and runs a clock against the plan's minutes. The presenter opens it with `N`, drags it to the laptop screen, and puts the deck on the projector.

Build it when the plan carries talking points the presenter must say but not show, and the talk has a time budget. A talk with neither needs only the deck.

The working files are in `examples/speaker-notes/`:

| File | Role |
|---|---|
| `notes.tpl.html` | The notes window. Standalone, no network. `__NOTES__`, `__TITLE__` and `__END__` are filled at build time. |
| `deck-notes.js` | The deck side: open the window, send state, take commands. Paste into the deck's script. |
| `build_notes.py` | Splits one source file into the deck and the notes window. |

## One source

The presenter layer lives inside the deck source, in each section, as `<template class="details">`. A `<template>` renders nothing, so the deck is correct before the build and the notes cannot drift from their slide. The build removes the templates from the delivered deck and assembles them into the notes window.

Each `<section>` carries three attributes the build reads:

```html
<section class="sec" id="gateway" data-title="The AI Gateway" data-min="14:00">
  ...visible slide...
  <template class="details">
    <h3>Lines</h3>
    <ul><li>The agent holds a run token and nothing else.</li></ul>
    <p class="src">Sources: inference_proxy.py, config.yaml.</p>
  </template>
</section>
```

`data-min` is the minute the section starts, from the plan. `data-title` is the rail label. The notes window shows them with the slide's own heading, so the presenter sees what the room sees.

Write the template as the plan's talking points, in HTML: `<h3>` groups, `<ul>` lines, a `<table>` for a set of values, `<p class="src">` for provenance. Add a `<p class="cue">` when the slide has a demo action to perform. Each line is one thing to say, and the sources are the plan's provenance, moved to where the presenter reads them.

## Link and clock

The two windows talk over `postMessage`, tagged `sf` (`deck-notes.js` has the three payloads). The deck sends its state on every move and every reveal step. The notes window shows "linked to the deck" and follows. Its arrow keys and section buttons send commands back, so the presenter drives from either window. Opened on its own, the notes window falls back to moving itself.

The clock starts when the deck first moves past section 0, or on the button. It turns red once the elapsed time passes the next section's `data-min`, and on the last section once it passes `--end`. Red means behind the plan, in one glance.

## Build

```sh
python3 examples/speaker-notes/build_notes.py deck.src.html examples/speaker-notes/notes.tpl.html out/ --title "The talk" --end 45:00
```

It writes `out/deck.html` and `out/speaker-notes.html` beside each other; the deck opens the notes by that relative name. A deck that needs more in each note, such as a "then" line that leads into the next section, extends the article template in the script.

**Complete when:** `N` opens the window, moving the deck moves the notes, the arrow keys in the notes window move the deck, the clock turns red past a section's minute, and the delivered deck contains no `<template class="details">`.

## Validation and window trust

The builder reads HTML structurally, so attribute order, quote style, extra classes,
inline tags in headings, and nested non-slide sections are supported. Slides are
all `section.sec` elements in document order. Each must have a unique `id`, a
`data-title`, a `data-min` in `m:ss` format, and exactly one presenter template
(`template.details`). Missing or duplicate notes, nested slides, and incomplete
sections/templates fail before output is written. Only presenter templates are
stripped; unrelated templates and the remaining deck source are preserved.

Only use trusted deck sources: presenter HTML is copied as authored, not sanitized.

The deck accepts messages only from the specific notes window it opened; the
notes accept state only from their original opener. Both check the sender origin
and validate indices/state before navigation. HTTP(S) messages use the exact
origin as their target. Local files use the browser's opaque `null` origin and
require `*` as the target, but still enforce window identity. Do not navigate the
linked windows to untrusted content. Repeated `N` focuses the existing notes;
closing it and pressing `N` creates a new peer. If the deck closes, notes navigate
locally again.

## Regression checks

From `html-presentation/examples/speaker-notes/`, Python 3 and Node.js are enough
for the dependency-free runtime tests:

```sh
python3 -m unittest discover -p 'test_*.py' -v
node --test test_messages.js
```

Development-only formatting/linting tools are pinned; the generated deck and
notes still have no runtime dependencies:

```sh
python3 -m venv .venv
# Use .venv/Scripts/python on Windows.
.venv/bin/python -m pip install -r requirements-dev.txt
npm ci --ignore-scripts
.venv/bin/ruff format --check .
.venv/bin/ruff check .
npm run format:check
npm run lint
```

Use `.venv/bin/ruff format .` and `npm run format` to apply formatting. The Biome
unused-variable exception is limited to `deck-notes.js`: its functions are pasted
into a larger deck script and called by that deck's navigation/key handlers.
The automated tests cover parsing, output ordering, missing notes, sender/origin
checks, invalid state, popup replacement, and standalone navigation. Also run the
interactive completion checks above in a browser for both local files and HTTP
when browser tooling is available.
