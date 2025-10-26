#!/usr/bin/env python3
import argparse, csv, json, re
from pathlib import Path

ART_M = {"el", "los", "un"}
ART_F = {"la", "las", "una"}
ART_ALL = ART_M | ART_F

def parse_tags_column_hint(lines):
    # Example: "#tags column:10" (1-based) -> 0-based index
    for ln in lines:
        if ln.startswith("#tags column:"):
            try:
                n = int(ln.split(":", 1)[1].strip())
                return max(1, n) - 1
            except Exception:
                pass
    return 9  # default to 10th col (0-based 9)

def strip_article(word):
    """
    Return (article_or_empty, lemma) from 'el compañero' -> ('el', 'compañero').
    If no leading article, returns ('', original).
    """
    if not word:
        return "", ""
    w = word.strip()
    m = re.match(r"^(\w+)\s+(.*)$", w)
    if m:
        art = m.group(1).lower()
        rest = m.group(2).strip()
        if art in ART_ALL:
            return art, rest
    return "", w

def infer_gender(es, gender):
    g = (gender or "").strip().lower()
    if g in {"m","f"}:
        return g
    art, _ = strip_article(es or "")
    if art in ART_M: return "m"
    if art in ART_F: return "f"
    return ""

def load_tsv(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().splitlines()
    tags_idx = parse_tags_column_hint(raw)
    rows = [ln for ln in raw if not ln.startswith("#") and ln.strip() != ""]
    parsed = [r.split("\t") for r in rows]
    return parsed, tags_idx

def normalize_rows(parsed, tags_idx):
    norm = []
    for i, cols in enumerate(parsed, 1):
        cols = cols + [""] * (max(10, tags_idx + 1) - len(cols))  # pad
        es           = cols[0].strip()
        gender       = infer_gender(es, cols[1])
        pos          = cols[2].strip().lower()
        meaning_en   = cols[3].strip()
        meaning_de   = cols[4].strip()
        meaning_es   = cols[5].strip()
        example_es   = cols[6].strip()
        example_src  = cols[7].strip()
        date_added   = cols[8].strip()
        tags         = cols[tags_idx].strip() if tags_idx < len(cols) else ""

        # Compute article + lemma for convenience (optional, but handy on site)
        art, lemma = strip_article(es)

        rec = {
            "id": f"S{str(i).zfill(5)}",
            "es": es,
            "display_article": art,   # optional for UI
            "lemma": lemma,           # 'compañero' from 'el compañero'
            "gender": gender,         # m/f/''
            "pos": pos,
            "meaning_en": meaning_en,
            "meaning_de": meaning_de,
            "meaning_es": meaning_es,
            "example_es": example_es,
            "example_src": example_src,
            "date_added": date_added,
            "tags": tags,
            "source": "",             # keep for future
            "theme": "",              # keep for future
            "note": ""
        }
        norm.append(rec)
    return norm

def write_csv(outpath, rows, order):
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=order)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in order})

def write_json(outpath, rows):
    outpath.parent.mkdir(parents=True, exist_ok=True)
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Anki TSV export")
    ap.add_argument("--csvout", required=True, help="Output CSV path")
    ap.add_argument("--jsonout", required=True, help="Output JSON path")
    args = ap.parse_args()

    parsed, tags_idx = load_tsv(Path(args.input))
    rows = normalize_rows(parsed, tags_idx)

    field_order = [
        "id","es","display_article","lemma","gender","pos",
        "meaning_en","meaning_de","meaning_es",
        "example_es","example_src","date_added","tags",
        "source","theme","note"
    ]
    write_csv(Path(args.csvout), rows, field_order)
    write_json(Path(args.jsonout), rows)

if __name__ == "__main__":
    main()
