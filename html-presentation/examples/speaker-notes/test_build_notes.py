import tempfile
from pathlib import Path
import subprocess
import sys
import unittest

from build_notes import build

TEMPLATE = "<title>__TITLE__</title><main data-end='__END__'>__NOTES__</main>"


def slide(sid="one", title="Intro", minute="0:00", details="<p>Speak</p>"):
    return (
        f"<section data-min='{minute}' class='extra sec active' data-title='{title}' id='{sid}'>"
        f"<h2 class='heading'>Visible <em>{sid}</em> &amp; more</h2>"
        f"<template data-extra='yes' class='other details'>{details}</template></section>"
    )


class BuildTests(unittest.TestCase):
    def test_valid_variations_preserve_order_and_visible_bytes(self):
        source = slide() + slide("two", "Next &amp; last", "14:00")
        deck, notes, count = build(source, TEMPLATE, "Talk & more", "30:00")
        self.assertEqual(count, 2)
        self.assertLess(notes.index('id="one"'), notes.index('id="two"'))
        self.assertIn("Visible one &amp; more", notes)
        self.assertIn('data-title="Next &amp; last"', notes)
        self.assertEqual(
            deck,
            source.replace(
                "<template data-extra='yes' class='other details'><p>Speak</p></template>",
                "",
            ),
        )
        self.assertNotIn("Speak", deck)

    def test_multiline_offsets_preserve_unicode_and_line_endings(self):
        source = "<!doctype html>\r\n<!-- é -->\r\n" + slide(
            details="First\nsecond"
        ).replace(">", ">\n")
        deck, notes, count = build(source, TEMPLATE, "Talk", "30:00")
        self.assertEqual(count, 1)
        self.assertTrue(deck.startswith("<!doctype html>\r\n<!-- é -->\r\n"))
        self.assertNotIn("First", deck)
        self.assertIn("First\nsecond", notes)
        self.assertIn("</section>", deck)

    def test_nested_sections_and_templates_do_not_end_slide_early(self):
        content = "<section><p>Notes</p></section><template><b>Nested</b></template>"
        source = (
            slide(details=content)
            .replace("<h2", "<section><h2")
            .replace("</h2>", "</h2></section>")
        )
        deck, notes, count = build(source, TEMPLATE, "Talk", "30:00")
        self.assertEqual(count, 1)
        self.assertIn(content, notes)
        self.assertNotIn("Notes", deck)

    def test_script_comment_and_unrelated_template_are_preserved(self):
        prefix = '<script>const fake = \'<section class="sec">\';</script><!-- <template class="details"> -->'
        suffix = (
            '<template id="other"><section class="sec">not a slide</section></template>'
        )
        deck, _, count = build(prefix + slide() + suffix, TEMPLATE, "Talk", "30:00")
        self.assertEqual(count, 1)
        self.assertTrue(deck.startswith(prefix))
        self.assertTrue(deck.endswith(suffix))

    def test_attribute_values_are_escaped_once(self):
        source = slide("one&quot;two", "A &quot;quote&quot; &amp; B")
        _, notes, _ = build(source, TEMPLATE, "<Talk>", "30:00")
        self.assertIn('id="one&quot;two"', notes)
        self.assertIn('data-title="A &quot;quote&quot; &amp; B"', notes)
        self.assertIn("&lt;Talk&gt;", notes)

    def test_placeholders_in_notes_are_literal(self):
        _, notes, _ = build(
            slide(details="__TITLE__ __END__"), TEMPLATE, "Talk", "30:00"
        )
        self.assertIn("__TITLE__ __END__", notes)

    def test_invalid_input_fails_instead_of_skipping_slides(self):
        cases = {
            "missing notes": slide().replace(
                "<template data-extra='yes' class='other details'><p>Speak</p></template>",
                "",
            ),
            "duplicate notes": slide().replace(
                "</section>", '<template class="details">extra</template></section>'
            ),
            "missing title": slide().replace("data-title='Intro'", ""),
            "duplicate id": slide() + slide(),
            "invalid time": slide(minute="0:90"),
            "unclosed slide": slide().replace("</section>", ""),
            "unclosed template": slide().replace("</template>", ""),
            "nested slide": slide().replace("</section>", slide("two") + "</section>"),
            "no slides": "<p>Nothing</p>",
            "orphan notes": '<template class="details">oops</template>' + slide(),
        }
        for label, source in cases.items():
            with self.subTest(label=label), self.assertRaises(ValueError):
                build(source, TEMPLATE, "Talk", "30:00")

    def test_cli_does_not_publish_partial_output_on_invalid_input(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "deck.src.html").write_text(
                slide().replace("data-title='Intro'", "")
            )
            (root / "notes.tpl.html").write_text(TEMPLATE)
            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("build_notes.py")),
                    str(root / "deck.src.html"),
                    str(root / "notes.tpl.html"),
                    str(root / "out"),
                    "--title",
                    "Talk",
                ],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing data-title", result.stderr)
            self.assertFalse((root / "out").exists())


if __name__ == "__main__":
    unittest.main()
