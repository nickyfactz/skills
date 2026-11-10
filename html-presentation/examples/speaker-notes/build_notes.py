#!/usr/bin/env python3
"""Split a deck into audience slides and one presenter note per section.sec.

Only presenter templates are removed; other source bytes remain unchanged.
Invalid or incomplete slide metadata fails before any output is written.
"""

import argparse
import html
from html.parser import HTMLParser
from pathlib import Path
import re


class DeckParser(HTMLParser):
    """Collect slide metadata and exact source spans without reserializing HTML."""

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.line_offsets = [0] + [match.end() for match in re.finditer("\n", source)]
        self.slides = []
        self.removals = []
        self.slide = None
        self.section_depth = 0
        self.template_depth = 0
        self.details_start = None
        self.heading_tag = None

    def source_offset(self):
        line, column = self.getpos()
        return self.line_offsets[line - 1] + column

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = (attrs.get("class") or "").split()
        if tag == "template":
            if self.template_depth == 0 and "details" in classes:
                if self.slide is None:
                    raise ValueError("presenter template outside a section.sec")
                if self.slide["details"] is not None:
                    raise ValueError(
                        f"duplicate presenter template in {self.slide['id']}"
                    )
                self.details_start = self.source_offset()
                self.details_body = self.source_offset() + len(self.get_starttag_text())
            self.template_depth += 1
            return
        if self.template_depth:
            return

        if tag == "section":
            self.section_depth += 1
            if "sec" in classes:
                if self.slide is not None:
                    raise ValueError("nested section.sec slides are not supported")
                for key in ("id", "data-title", "data-min"):
                    if not attrs.get(key):
                        raise ValueError(f"section.sec is missing {key}")
                if any(slide["id"] == attrs["id"] for slide in self.slides):
                    raise ValueError(f"duplicate slide id: {attrs['id']}")
                if not re.fullmatch(r"\d+:[0-5]\d", attrs["data-min"]):
                    raise ValueError(f"invalid data-min in {attrs['id']}: use m:ss")
                self.slide = {
                    "id": attrs["id"],
                    "title": attrs["data-title"],
                    "minute": attrs["data-min"],
                    "depth": self.section_depth,
                    "details": None,
                    "heading": [],
                }
        if self.slide is not None and tag in ("h1", "h2"):
            if not self.slide["heading"] and self.heading_tag is None:
                self.heading_tag = tag

    def handle_endtag(self, tag):
        if tag == "template" and self.template_depth:
            self.template_depth -= 1
            if self.template_depth == 0 and self.details_start is not None:
                self.slide["details"] = self.source[
                    self.details_body : self.source_offset()
                ].strip()
                end = self.source.index(">", self.source_offset()) + 1
                self.removals.append((self.details_start, end))
                self.details_start = None
            return
        if self.template_depth:
            return
        if tag == self.heading_tag:
            self.heading_tag = None
        if tag == "section":
            if self.slide is not None and self.section_depth == self.slide["depth"]:
                if self.slide["details"] is None:
                    raise ValueError(
                        f"missing presenter template in {self.slide['id']}"
                    )
                self.slides.append(self.slide)
                self.slide = None
                self.heading_tag = None
            self.section_depth -= 1
            if self.section_depth < 0:
                raise ValueError("unmatched </section>")

    def handle_startendtag(self, tag, attrs):
        if tag in ("section", "template"):
            raise ValueError(f"<{tag}/> needs an explicit closing tag")
        # HTML void tags (e.g. <br/>) do not affect section/template ownership.

    def handle_data(self, data):
        if self.slide is not None and self.heading_tag and not self.template_depth:
            self.slide["heading"].append(data)

    def parse(self):
        self.feed(self.source)
        self.close()
        if self.section_depth or self.template_depth:
            raise ValueError("unclosed section or template")
        if not self.slides:
            raise ValueError("no section.sec slides found")
        if len(self.slides) != len(self.removals):
            raise ValueError("slide and presenter-template counts differ")
        deck = self.source
        for start, end in reversed(self.removals):
            deck = deck[:start] + deck[end:]
        return deck, self.slides


def build(source, template, title, end):
    if not re.fullmatch(r"\d+:[0-5]\d", end):
        raise ValueError("invalid --end: use m:ss")
    for placeholder in ("__NOTES__", "__TITLE__", "__END__"):
        if placeholder not in template:
            raise ValueError(f"notes template is missing {placeholder}")

    deck, slides = DeckParser(source).parse()
    articles = []
    for slide in slides:
        sid = html.escape(slide["id"], quote=True)
        label = html.escape(slide["title"], quote=True)
        minute = html.escape(slide["minute"], quote=True)
        heading = html.escape(" ".join("".join(slide["heading"]).split()))
        articles.append(
            f'<article class="note" id="{sid}" data-title="{label}" data-min="{minute}">'
            f'<div class="min">{minute}</div><h1>{label}</h1>'
            f'<p class="screen">On screen: <b>{heading}</b></p><p class="step"></p>\n'
            f"{slide['details']}\n</article>"
        )
    replacements = {
        "__NOTES__": "\n".join(articles),
        "__TITLE__": html.escape(title, quote=True),
        "__END__": end,
    }
    # A single substitution pass cannot reinterpret placeholders inside user notes.
    notes = re.sub(
        r"__NOTES__|__TITLE__|__END__", lambda m: replacements[m[0]], template
    )
    return deck, notes, len(slides)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("src")
    parser.add_argument("template")
    parser.add_argument("out")
    parser.add_argument("--title", required=True, help="the deck title")
    parser.add_argument("--end", default="45:00", help="talk end time, m:ss")
    args = parser.parse_args()
    source = Path(args.src)
    try:
        deck, notes, count = build(
            source.read_text(encoding="utf-8"),
            Path(args.template).read_text(encoding="utf-8"),
            args.title,
            args.end,
        )
    except ValueError as error:
        parser.error(str(error))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "speaker-notes.html").write_text(notes, encoding="utf-8")
    (out / source.name.replace(".src", "")).write_text(deck, encoding="utf-8")
    print(f"{count} sections")


if __name__ == "__main__":
    main()
