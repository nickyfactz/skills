#!/usr/bin/env python3
"""Split one deck source into the deck and its speaker notes.

    build_notes.py deck.src.html notes.tpl.html out/ --title "The talk" --end 45:00

The source is the deck with one `<template class="details">` inside each
`<section>`. Each section carries `id`, `data-title` and `data-min` (the
minute the section starts, `m:ss`). The template holds that section's
presenter layer: talking points, tables, sources, as HTML.

Output: `out/<deck>.html` with every template removed, and
`out/speaker-notes.html` with one `<article class="note">` per section.
"""
import argparse, html, pathlib, re, sys

SEC = re.compile(r'<section class="sec" id="([^"]+)" data-title="([^"]+)" data-min="([^"]+)">(.*?)</section>', re.S)
TPL = re.compile(r'\n[ \t]*<template class="details">.*?</template>', re.S)

def heading(body):
    m = re.search(r'<h[12]>(.*?)</h[12]>', body, re.S)
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip() if m else ''

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('template'); ap.add_argument('out')
    ap.add_argument('--title', required=True, help='the deck title, for the notes window title bar')
    ap.add_argument('--end', default='45:00', help='when the talk ends, m:ss; the clock turns red past it on the last section')
    a = ap.parse_args()
    src = pathlib.Path(a.src).read_text()
    notes = []
    for m in SEC.finditer(src):
        sid, title, mn, body = m.groups()
        t = re.search(r'<template class="details">(.*?)</template>', body, re.S)
        det = t.group(1).strip() if t else ''
        notes.append(
            '<article class="note" id="%s" data-title="%s" data-min="%s">'
            '<div class="min">%s</div><h1>%s</h1>'
            '<p class="screen">On screen: <b>%s</b></p><p class="step"></p>\n%s\n</article>'
            % (sid, html.escape(title), mn, mn, html.escape(title), html.escape(heading(body)), det))
    if not notes:
        sys.exit('no <section class="sec" id=... data-title=... data-min=...> found')
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    tpl = pathlib.Path(a.template).read_text()
    (out / 'speaker-notes.html').write_text(
        tpl.replace('__NOTES__', '\n'.join(notes)).replace('__TITLE__', html.escape(a.title)).replace('__END__', a.end))
    deck = TPL.sub('', src)
    assert '<template' not in deck, 'a template survived the strip'
    (out / pathlib.Path(a.src).name.replace('.src', '')).write_text(deck)
    print('%d sections' % len(notes))

if __name__ == '__main__':
    main()
