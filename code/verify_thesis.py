#!/usr/bin/env python3
"""
Compare the numbers of the current thesis (thesis_claims.json) with the output of the code.

    python verify_thesis.py results/results.json --full
    python verify_thesis.py results/results.json --full --thesis thesis.docx   (also checks that key numbers are printed in the .docx)

Status: MATCH (within rounding of the printed digits), DIFF (the code output differs from the value printed in the thesis).
It reads results/results.json (run_experiment.py) and results_cybattt/cybattt_results.json (cybattt_pipeline.py, if present).
"""
import json, os, sys, subprocess, re

def g(R, path):
    if path.startswith("sensitivity_cusum."):          # grid keys contain dots ("0.05|0.01")
        key, field = path[len("sensitivity_cusum."):].rsplit(".", 1)
        return R["sensitivity_cusum"][key][field]
    cur = R
    for p in path.split("."):
        cur = cur[int(p)] if isinstance(cur, list) else cur[p]
    return cur

# strings that must appear in the thesis text (checked only with --thesis)
KEY_STRINGS = ["0.827", "0.971", "0.825 ± 0.005", "0.834", "0.0412", "0.0625", "109.6", "81.0", "48.7", "9.3", "0.047", "0.852", "0.987", "0.845 ± 0.014",
               "52 of 114", "96 of 105", "31,434", "27,642", "0.916", "6.2 days", "6.7 days"]
NO_CODE = [("Note 5 (Layer 1)", "precision 100% of the extracted control identifiers", "needs the source PDF or a hand-annotated gold file; the counts 52/114 and 96/105 are reproduced from controls.csv")]

def main(path, thesis=None):
    here = os.path.dirname(os.path.abspath(path)); claims = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thesis_claims.json")))
    src = {"results": json.load(open(path))}
    cyb = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_cybattt", "cybattt_results.json")
    if os.path.exists(cyb): src["cybattt"] = json.load(open(cyb))
    rows = []; nm = nd = 0
    for loc, label, p, val, tol, s in claims:
        if s not in src: rows.append((loc, label, val, None, "MISSING")); continue
        try: got = g(src[s], p)
        except (KeyError, IndexError, TypeError): rows.append((loc, label, val, None, "MISSING")); continue
        ok = abs(got - val) <= tol + 1e-12; nm += ok; nd += (not ok); rows.append((loc, label, val, got, "MATCH" if ok else "DIFF"))
    miss = [r for r in rows if r[4] == "MISSING"]; nd += len(miss)
    out = [f"# Thesis vs code", f"\n{nm} MATCH, {nd} DIFF/MISSING, {len(NO_CODE)} item without code.\n", "| Thesis location | Quantity | Thesis | Code | Status |", "|---|---|---|---|---|"]
    for loc, label, val, got, st in rows:
        out.append(f"| {loc} | {label} | {val} | {'-' if got is None else (round(got, 4) if isinstance(got, float) else got)} | {st} |")
    if thesis:
        txt = subprocess.run(["pandoc", thesis, "-t", "plain", "--wrap=none"], capture_output=True, text=True).stdout
        out += ["", "## Key numbers printed in the thesis text", "| String | Found |", "|---|---|"]
        for k in KEY_STRINGS: out.append(f"| {k} | {'yes' if k in txt else 'NO'} |")
    out += ["", "## Not reproducible by this package", "| Thesis location | Item | Reason |", "|---|---|---|"] + [f"| {a} | {b} | {c} |" for a, b, c in NO_CODE]
    txt = "\n".join(out); open(os.path.join(here, "reconciliation.md"), "w", encoding="utf8").write(txt)
    print(txt if "--full" in sys.argv else "\n".join([out[1], ""] + [l for l in out if l.endswith("DIFF |") or l.endswith("MISSING |")]))

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    th = sys.argv[sys.argv.index("--thesis") + 1] if "--thesis" in sys.argv else None
    main(a[0] if a else "results/results.json", th)
