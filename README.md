# Zacharias Frankel, *Mevo ha-Yerushalmi*: Hebrew and English

Site: <https://openseforim.org/frankel-mevo/>

Zacharias Frankel (1801–1875), first head of the Jewish Theological Seminary at Breslau, wrote *Mevo ha-Yerushalmi*
(Breslau 1870), the first modern introduction to the Jerusalem Talmud: its origin, redaction and language, and an
alphabetical lexicon of the amoraim of the Land of Israel. It has never been translated. This repository holds a Hebrew
text checked against the scan, an English translation paragraph by paragraph, and the scripts that build the reader.

## Status

| Part | Pages | Status |
|---|---|---|
| 1. The author's foreword | VII–VIII (files p012–p013) | 24-Nov-2026. Hebrew checked against the scan line by line; 5 paragraphs translated. |
| 2– | the introduction and the lexicon | OCR only (`data/he_raw/`), not checked or translated |

## Sources

- **Base text:** the first edition, Breslau 1870, from University Library Potsdam,
  [Digitales Brandenburg 320753](https://digital.ub.uni-potsdam.de/content/titleinfo/320753) (Public Domain Mark).
  Page files `pNNN` are the pages of the library's PDF (page 1 is the library's cover sheet). The scan is about
  1000 px wide per page, low for OCR but clean.
- **Translations that exist:** none known.

## Method

- **OCR:** [Kraken](https://kraken.re/) with the PP-OCRv6 medium model, line by line, on Kaggle GPUs (24-Nov-2026),
  pages scaled up 2x before reading. Lines are found from the row ink profile, then read with
  `ocr --no-segmentation --base-dir R`. Raw output for the whole book: `data/he_raw/` (not checked). The title pages,
  preface pages and some index pages came out empty or short and are still to be done.
- **Checking:** every line compared with the scan by eye; spelling and abbreviations as printed.
- **English:** close to the Hebrew; biblical phrases identified in [gray brackets]. The translation is by Claude
  (Anthropic), directed and reviewed by Ezra Brand.

## Files

- `data/he/pNNN.txt`: checked Hebrew, one file per page (`@ N` printed page; `#` heading; blank line = paragraph break;
  `---` then the page's notes).
- `data/en/part-NN.en.txt`, `part-NN.fn.en.txt`, `part-NN.notes.json`: English rows, notes, uncertain renderings.
- `scripts/config.py`: the work's settings; `scripts/build_site.py` builds `docs/`; `scripts/make_scans.py` makes the
  page images for the scan panel.

## Licence

Text and translation: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The Hebrew original is in the
public domain.
