"""Settings of the Mevo ha-Yerushalmi reader, used by build_site.py and make_scans.py."""

SHORT = "Frankel, Mevo ha-Yerushalmi"
TITLE_HE = "מבוא הירושלמי"
TITLE_HTML = "Zacharias Frankel, <i>Mevo ha-Yerushalmi</i>"
SUBTITLE = "Introduction to the Jerusalem Talmud, with an English translation paragraph by paragraph"
EDITION = "Breslau 1870"
SCAN_NAME = "the Potsdam scan"
NOTES_HEAD = "Frankel's notes"
REST = "The introduction (chapters 1–10) and the lexicon of the amoraim"

# page files are the pages of the Potsdam PDF (file pNNN = PDF page NNN; page 1 is the library's cover sheet).
# The Potsdam viewer has no stable page address that could be checked, so the link goes to the title record.
PAGES_DIR = "data/pages_all"


def scan_url(stem):
    return "https://digital.ub.uni-potsdam.de/content/titleinfo/320753"


PARTS = {
    1: ("The author's foreword",
        "How the Venice text is cited, the Leiden manuscript, and a disappointment at Erfurt",
        ["p012", "p013"]),
}

ABOUT = """Zacharias Frankel (1801–1875), chief rabbi of Dresden and from 1854 the first head of the Jewish Theological
Seminary at Breslau, wrote <i>Mevo ha-Yerushalmi</i> (Breslau 1870) as the first modern introduction to the Jerusalem
Talmud: its origin, redaction and language, and an alphabetical lexicon of the amoraim of the Land of Israel. It is
still used for the sages of the Yerushalmi, and it has never been translated."""

BACKGROUND_BLURB = "Frankel, the Breslau seminary, and the study of the Yerushalmi."

INDEX_BODY = """<h2>The Hebrew text</h2>
<ul>
<li><b>Base text:</b> the first edition, Breslau 1870. Scan: University Library Potsdam,
<a href="https://digital.ub.uni-potsdam.de/content/titleinfo/320753">Digitales Brandenburg 320753</a> (Public Domain Mark).</li>
<li><b>OCR:</b> Kraken with the PP-OCRv6 model, line by line, then checked against the scan by eye.</li>
</ul>

<h2>Method</h2>
<ul>
<li><b>Rows.</b> One row is one heading or one paragraph of the print.</li>
<li><b>English.</b> Close to the Hebrew; Frankel's references are kept as he gives them, with the translator's additions
in gray brackets.</li>
<li><b>Uncertain renderings</b> have the mark ⚠ and a note at the end of the page.</li>
<li><b>Translator.</b> The translation is by Claude (Anthropic), directed and reviewed by Ezra Brand.</li>
</ul>

<h2>Translations that exist</h2>
<ul><li>None known.</li></ul>"""

WORK = {"schema": 1, "slug": "frankel-mevo", "order": 36, "kind": "translation",
        "title": "Zacharias Frankel, *Mevo ha-Yerushalmi*", "short_title": "*Mevo ha-Yerushalmi*", "title_he": TITLE_HE,
        "author": "Zacharias Frankel (1801–1875)",
        "status_label": "In progress · foreword (pilot)",
        "start": "part-01.html", "start_label": "The author's foreword",
        "summary": "The first modern introduction to the Jerusalem Talmud, with an English translation paragraph by paragraph.",
        "base_edition": {"label": "Breslau 1870; Potsdam scan", "scan_url": "https://digital.ub.uni-potsdam.de/content/titleinfo/320753"},
        "method": "Paragraph-aligned Hebrew and English; Hebrew from Kraken OCR checked against the scan.",
        "cite": "Zacharias Frankel, *Mevo ha-Yerushalmi*, Hebrew text with English translation, ed. Ezra Brand. Open Seforim",
        "url": "https://openseforim.org/frankel-mevo/", "repo": "https://github.com/openseforim/frankel-mevo", "doi": "10.5281/zenodo.24559622",
        "licence": {"name": "CC BY-SA 4.0", "url": "https://creativecommons.org/licenses/by-sa/4.0/"}}
