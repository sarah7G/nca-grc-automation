#!/usr/bin/env python3
"""
Layer 1 (rule-based baseline): extract control records from an NCA regulation document and evaluate the extraction.

This is NOT the AraBERT/AraBART parser of the design; it is a regular-expression extractor for the numbered
structure used in NCA documents (domain 1, subdomain 1-1, control 1-1-1, sub-control 1-1-1-1). It gives a measurable
baseline for RQ1 and a reference an AraBERT model must beat.

Input : the document as .txt, or .pdf (needs `pdftotext` from poppler). Use the real NCA document you downloaded.
Output: <out>/controls.csv  (control_id, level, domain, subdomain, text)
Evaluation (choose what you have):
  --expected_controls N   official number of controls stated in the document -> extraction-count check
  --gold gold.csv         YOUR manual annotation of a sample (columns control_id,text) -> ID precision/recall/F1
                          and token-level F1 of the extracted text. Annotate it by hand (e.g. 30-50 controls); do not generate it.
Usage : python layer1_extract.py --doc ECC-1-2018.pdf --out layer1_out --expected_controls 114 --gold gold.csv
"""
import argparse, csv, json, os, re, subprocess, sys

ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
ID = re.compile(r"^\s*(\d+(?:-\d+){0,3})[\s.:)]+(\S.*)$")

def load_text(path):
    if path.lower().endswith(".pdf"):
        try: return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError): sys.exit("pdftotext not available: convert the PDF to .txt first.")
    return open(path, encoding="utf8").read()

def extract(text):
    recs, cur, domain, sub = [], None, "", ""
    for line in text.translate(ARABIC_DIGITS).splitlines():
        m = ID.match(line)
        if m and not re.fullmatch(r"\d{4}", m.group(1)):       # ignore years
            cid, rest = m.group(1), m.group(2).strip(); level = cid.count("-") + 1
            if level == 1: domain, cur = rest, None
            elif level == 2: sub, cur = rest, None
            else: cur = {"control_id": cid, "level": level, "domain": domain, "subdomain": sub, "text": rest}; recs.append(cur)
        elif cur is not None and line.strip() and not re.match(r"^\s*(Objective|Controls?|Page \d+)\b", line, re.I):
            cur["text"] += " " + line.strip()
    for r in recs: r["text"] = re.sub(r"\s+", " ", r["text"]).strip()
    return recs

def tok_f1(a, b):
    a, b = a.lower().split(), b.lower().split()
    if not a or not b: return 0.0
    common = sum(min(a.count(w), b.count(w)) for w in set(a))
    if common == 0: return 0.0
    p, r = common / len(a), common / len(b); return 2 * p * r / (p + r)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--doc", required=True); ap.add_argument("--out", default="layer1_out")
    ap.add_argument("--expected_controls", type=int); ap.add_argument("--gold"); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True); recs = extract(load_text(a.doc))
    with open(os.path.join(a.out, "controls.csv"), "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=["control_id", "level", "domain", "subdomain", "text"]); w.writeheader(); w.writerows(recs)
    ctrl = [r for r in recs if r["level"] == 3]; res = {"n_records": len(recs), "n_controls_level3": len(ctrl), "n_subcontrols_level4": sum(r["level"] == 4 for r in recs)}
    if a.expected_controls: res["expected_controls"] = a.expected_controls; res["count_ratio_extracted_over_expected"] = len(ctrl) / a.expected_controls
    if a.gold:
        gold = {r["control_id"]: r["text"] for r in csv.DictReader(open(a.gold, encoding="utf8"))}; ext = {r["control_id"]: r["text"] for r in recs}
        tp = len(set(gold) & set(ext)); p = tp / len(ext) if ext else 0; r_ = tp / len(gold) if gold else 0
        res.update({"gold_n": len(gold), "id_precision_vs_all_extracted": p, "id_recall": r_, "id_f1": (2 * p * r_ / (p + r_)) if p + r_ else 0,
                    "mean_token_f1_on_matched": (sum(tok_f1(ext[k], gold[k]) for k in set(gold) & set(ext)) / tp) if tp else 0,
                    "note": "precision is computed against ALL extracted records, so it is only meaningful if the gold file covers the whole annotated section"})
    json.dump(res, open(os.path.join(a.out, "layer1_results.json"), "w"), indent=2); print(json.dumps(res, indent=2))
