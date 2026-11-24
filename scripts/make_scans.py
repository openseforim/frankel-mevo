"""Page images for the scan panel: docs/scans/<stem>.jpg (900 px wide, greyscale) from the page files in
config.PAGES_DIR.   py -3.13 -I scripts/make_scans.py p018 p019 ...   (existing files are kept)"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import config  # noqa: E402

OUT = ROOT / "docs" / "scans"
OUT.mkdir(parents=True, exist_ok=True)
for stem in sys.argv[1:]:
    out = OUT / f"{stem}.jpg"
    if out.exists():
        continue
    src = [p for p in (ROOT / config.PAGES_DIR).glob(f"{stem}.*")]
    im = Image.open(src[0]).convert("L")
    if im.width > 900:
        im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
    im.save(out, quality=70, optimize=True, progressive=True)
    print(out.name, im.size, f"{out.stat().st_size // 1024} KB")
