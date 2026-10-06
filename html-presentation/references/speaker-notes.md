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
