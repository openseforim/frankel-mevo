"""Build a Frankel reader: docs/part-NN.html per translated part, docs/index.html, docs/background.html (if any),
docs/work.json. The work-specific settings are in scripts/config.py.

  py -3.13 -I scripts/build_site.py

Hebrew: checked pages data/he/pNNN.txt (page files of the scan PDF), line for line as printed, with marks:
  '@ N'      the printed page number (first line)
  '# text'   a heading, one unit each
  blank line a paragraph break (paragraphs run on across pages)
  '---'      the footnote rule: the lines after it are the page's footnotes, each starting 'N)'
English: data/en/part-NN.en.txt, one block per Hebrew unit, blank lines between; data/en/part-NN.fn.en.txt, one block
per footnote ('N) ...'), in order; ⚠n uncertain, explained in part-NN.notes.json."""
import html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import config as C  # noqa: E402
DOCS = ROOT / "docs"
e = html.escape
TOK = re.compile(r"\{page:(p\d{3})\}")

PARTS = C.PARTS
PRINTED = {}  # page file -> printed page number (filled from the checked pages' first line '@ N', if any)

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,600;1,400&family=Noto+Serif+Hebrew:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
<link rel="stylesheet" href="/assets/os.css">
<script src="/assets/os.js" defer></script>
</head>
<body>
"""


def read_blocks(path):
    blocks, cur = [], []
    for raw in path.read_text(encoding="utf-8").split("\n"):
        line = raw.strip()
        if line:
            cur.append(line)
        elif cur:
            blocks.append(" ".join(cur)); cur = []
    if cur:
        blocks.append(" ".join(cur))
    return blocks


def parse_pages(stems):
    """Units (('h'|'p', text)) and footnotes ((page stem, number, text)) of a run of checked pages."""
    units, notes, para = [], [], []
    call = re.compile(r"(?<=[א-ת׳״'\")])\s?(\d{1,2})\)")
    nonlocal_seq = [0]  # the print numbers notes per page; the reader numbers them through the part
    for stem in stems:
        local = {}
        lines = (ROOT / "data" / "he" / f"{stem}.txt").read_text(encoding="utf-8").splitlines()
        if lines and lines[0].startswith("@"):
            PRINTED[stem] = lines[0][1:].strip(); lines = lines[1:]
        body, fn = lines, []
        if "---" in [l.strip() for l in lines]:
            k = [l.strip() for l in lines].index("---")
            body, fn = lines[:k], lines[k + 1:]
        first = True
        for l in body:
            s = l.strip()
            def num(m):
                nonlocal_seq[0] += 1; local[m.group(1)] = nonlocal_seq[0]
                return f"⟦{nonlocal_seq[0]}⟧"
            s = call.sub(num, s)
            if first and s:
                s = f"{{page:{stem}}} " + s
                first = False
            if not s:
                if para:
                    units.append(("p", " ".join(para))); para = []
            elif s.lstrip("{}page:v_0123456789 ").startswith("#"):
                if para:
                    units.append(("p", " ".join(para))); para = []
                tok = re.match(r"(\{page:[^}]+\}\s*)?#\s*(.*)", s)
                units.append(("h", (tok.group(1) or "") + tok.group(2)))
            else:
                para.append(s)
        cur = None
        for l in fn:
            s = l.strip()
            m = re.match(r"^(\d+)\)\s*(.*)", s)
            if m:
                if m.group(1) not in local:
                    sys.exit(f"{stem}: footnote {m.group(1)} has no call in the text")
                cur = [stem, str(local[m.group(1)]), m.group(2)]; notes.append(cur)
            elif cur and s:
                cur[2] += " " + s
    if para:
        units.append(("p", " ".join(para)))
    return units, notes


def page_label(stem):
    return PRINTED.get(stem) or str(int(stem[1:]))


def fmt_he(text, stem_for_calls):
    out = e(text, quote=False)
    def box(m):
        stem = m.group(1)
        return (f'<a class="scanlink" href="{C.scan_url(stem)}" data-scan-img="scans/{stem}.jpg" '
                f'data-scan-label="p. {page_label(stem)}" title="Page {page_label(stem)} ({C.SCAN_NAME})">p. {page_label(stem)}</a>')
    out = TOK.sub(box, out)
    # footnote calls, renumbered through the part by parse_pages as ⟦n⟧
    return re.sub(r"⟦(\d+)⟧", lambda m: f'<sup class="fn"><a href="#fn-{m.group(1)}">{m.group(1)}</a></sup>', out)


def fmt_en(text):
    text = e(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]", r'<span class="ref">[\1]</span>', text)
    text = re.sub(r"\{(\d{1,2})\}", r'<sup class="fn" id="fnref-\1"><a href="#fn-\1">\1</a></sup>', text)
    return re.sub(r"\s*⚠(\d+)", r' <a class="warn" href="#n\1" id="r\1" title="uncertain rendering">⚠\1</a>', text)


def part_page(num):
    title, subtitle, stems = PARTS[num]
    units, notes = parse_pages(stems)
    en = read_blocks(ROOT / "data" / "en" / f"part-{num:02d}.en.txt")
    fn_en = read_blocks(ROOT / "data" / "en" / f"part-{num:02d}.fn.en.txt")
    warn = json.loads((ROOT / "data" / "en" / f"part-{num:02d}.notes.json").read_text(encoding="utf-8"))
    if len(units) != len(en) or len(notes) != len(fn_en):
        sys.exit(f"part {num}: Hebrew {len(units)} units / {len(notes)} footnotes, English {len(en)} / {len(fn_en)}")
    for stem in stems:
        if not (DOCS / "scans" / f"{stem}.jpg").exists():
            sys.exit(f"part {num}: no page image docs/scans/{stem}.jpg; run scripts/make_scans.py")
    rows, cur = [], None
    for i, ((kind, h), x) in enumerate(zip(units, en), 1):
        cls = "row head" if kind == "h" else "row"
        starts = [m.group(1) for m in TOK.finditer(h)]
        pg = ([cur] if cur and not h.startswith("{page:") else []) + starts
        cur = starts[-1] if starts else cur
        nums = [page_label(x) for x in pg]
        lab = f"row {i}, " + (f"p. {nums[0]}" if len(nums) == 1 else f"pp. {nums[0]}–{nums[-1]}")
        rows.append(f'<div class="{cls}" id="u{i}" data-label="{lab}"><a class="ln" href="#u{i}">{i}</a>'
                    f'<p class="en">{fmt_en(x)}</p><p class="he" lang="he" dir="rtl">{fmt_he(h, None)}</p></div>')
    fnrows = []
    for (stem, n, h), x in zip(notes, fn_en):
        x = re.sub(r"^\d+\)\s*", "", x)
        fnrows.append(f'<div class="row fnrow" id="fn-{n}" data-label="note {n} (p. {page_label(stem)})"><a class="ln back" href="#fnref-{n}" title="Back to the text">{n}<span aria-hidden="true"> ↩</span></a>'
                      f'<p class="en">{fmt_en(x)} <a class="fnback" href="#fnref-{n}">↩ back to the text</a></p><p class="he" lang="he" dir="rtl">{e(h, quote=False)}'
                      f' <span class="fnpage">(p. {page_label(stem)})</span></p></div>')
    marks = set(re.findall(r"⚠(\d+)", " ".join(en + fn_en)))
    if marks - set(warn):
        sys.exit(f"part {num}: notes missing for ⚠{sorted(marks - set(warn))}")
    warn_rows = "\n".join(f'<li id="n{k}"><a href="#r{k}">⚠{k}</a> <span lang="he" dir="rtl" class="he-inline">{e(v["he"])}</span>'
                          f' — {e(v["note"], quote=False)}</li>' for k, v in warn.items())
    pages = ", ".join(page_label(s) for s in stems)
    page = HEAD.format(title=f"{e(title)} — {C.SHORT}") + f"""<header class="chapter">
<nav class="crumb" aria-label="Parts"><span><a href="index.html">All parts</a> · Part {num}</span></nav>
<p class="title-he" lang="he" dir="rtl">{C.TITLE_HE}</p>
<h1>{e(title)}</h1>
<p class="sub">{e(subtitle)}</p>
<details class="about"><summary>About this text</summary>
<p class="meta">Pp. {pages} ({C.EDITION}). One row is one heading or one paragraph of the print; the author's own
footnotes, if any, follow the text. Boxes marked "p. N" in the Hebrew show where a printed page begins; they link to
{C.SCAN_NAME}, and the <b>Scan</b> button at the top shows the page beside the text. References in
<span class="ref">[gray brackets]</span> are the translator's. <a class="warn" href="#notes">⚠</a> marks an uncertain
rendering. The Hebrew was checked against the scan line by line; spelling and abbreviations are as printed.</p>
</details>
</header>
<main class="prose">
{chr(10).join(rows)}
{(chr(10) + '<h2 class="fnhead">' + C.NOTES_HEAD + '</h2>' + chr(10) + chr(10).join(fnrows)) if fnrows else ""}
</main>
<footer id="notes">
{('<h2>Uncertain renderings</h2>' + chr(10) + '<ul class="notes">' + chr(10) + warn_rows + chr(10) + '</ul>') if warn_rows else ''}
<nav class="crumb foot" aria-label="Parts"><span><a href="index.html">All parts</a></span></nav>
</footer>
</body>
</html>
"""
    (DOCS / f"part-{num:02d}.html").write_text(page, encoding="utf-8")
    print(f"wrote docs/part-{num:02d}.html: {len(units)} units, {len(notes)} footnotes")
    return len(units)


def index_page(counts):
    rows = "\n".join(f'<tr class="done"><td><a href="part-{k:02d}.html">{k}</a></td><td><a href="part-{k:02d}.html">{e(PARTS[k][0])}</a>: '
                     f'{e(PARTS[k][1])}</td><td>{", ".join(page_label(s) for s in PARTS[k][2])}</td><td>{counts[k]} units</td></tr>'
                     for k in sorted(PARTS))
    bg = ('<p><b><a href="background.html">Background for the reader</a></b>: ' + C.BACKGROUND_BLURB + "</p>"
          if (ROOT / "BACKGROUND.md").exists() else "")
    page = HEAD.format(title=f"{C.SHORT}: Hebrew and English") + f"""<header>
<h1>{C.TITLE_HTML}</h1>
<p class="sub">{C.SUBTITLE} · <span lang="he" dir="rtl">{C.TITLE_HE}</span></p>
<p class="meta">{C.ABOUT}</p>
</header>
<article>
<h2>Parts</h2>
<div class="tablewrap">
<table>
<tr><th>Part</th><th>Contents</th><th>Pages</th><th>Status</th></tr>
{rows}
<tr><td>{max(PARTS) + 1}–</td><td>{C.REST}</td><td></td><td>OCR only, not checked or translated</td></tr>
</table>
</div>
<a class="cta" href="part-01.html">Read part 1, side by side →</a>
{bg}
{C.INDEX_BODY}
</article>
</body>
</html>
"""
    (DOCS / "index.html").write_text(page, encoding="utf-8")
    print("wrote docs/index.html")


def background_page():
    if not (ROOT / "BACKGROUND.md").exists():
        return
    import markdown
    md = re.sub(r"^# .*\n", "", (ROOT / "BACKGROUND.md").read_text(encoding="utf-8"), count=1)
    page = HEAD.format(title=f"Background for the reader — {C.SHORT}") + f"""<header class="chapter">
<nav class="crumb" aria-label="Parts"><span><a href="index.html">All parts</a> · Background</span></nav>
<p class="title-he" lang="he" dir="rtl">{C.TITLE_HE}</p>
<h1>Background for the reader</h1>
</header>
<article class="bgnote">
{markdown.markdown(md, extensions=["extra"])}
</article>
</body>
</html>
"""
    (DOCS / "background.html").write_text(page, encoding="utf-8")
    print("wrote docs/background.html")


def work_json():
    (DOCS / "work.json").write_text(json.dumps(C.WORK, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    DOCS.mkdir(exist_ok=True)
    counts = {k: part_page(k) for k in sorted(PARTS)}
    index_page(counts)
    background_page()
    work_json()


if __name__ == "__main__":
    main()
    import subprocess
    tool = ROOT.parent / "openseforim-site" / "tools" / "postbuild.py"
    if tool.exists():
        subprocess.run([sys.executable, str(tool), C.WORK["slug"], str(DOCS)], check=False)
