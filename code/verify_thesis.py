#!/usr/bin/env python3
"""
Compare the numbers of the current thesis (thesis_claims.json) with the output of the code.

    python verify_thesis.py results/results.json --full
    python verify_thesis.py results/results.json --full --thesis thesis.docx   (also checks that key numbers are printed in the .docx)

Status: MATCH (within rounding of the printed digits), DIFF (the code output differs from the value printed in the thesis).
It reads results/results.json (run_experiment.py), results_extra/extra_results.json (extra_analysis.py),
results_cybattt/cybattt_results.json (cybattt_pipeline.py) and ../layer1_ecc/layer1_text_eval.json and
../layer1_ecc/linking_comparison.json (layer1_evaluate.py). When a freshly generated file is absent, the copy published
in ../results/ (extra_robustness/, cybattt/) is used instead, and the report states which file was read.
"""
import json, os, sys, subprocess, re

def g(R, path):
    if path.startswith("sensitivity_cusum."):          # grid keys contain dots ("0.05|0.01")
        key, field = path[len("sensitivity_cusum."):].rsplit(".", 1)
        return R["sensitivity_cusum"][key][field]
    cur, rest = R, path
    while rest:                                         # keys may themselves contain dots: take the longest matching key
        if isinstance(cur, list):
            head, _, rest = rest.partition("."); cur = cur[int(head)]; continue
        key = max((k for k in cur if rest == k or rest.startswith(k + ".")), key=len)
        cur = cur[key]; rest = rest[len(key) + 1:]
    return cur

# strings that must appear in the thesis text (checked only with --thesis)
KEY_STRINGS = ["0.36", "0.29", "0.60", "0.72", "5.9%", "7.2%", "0.827", "0.971", "0.825 ± 0.005", "0.834", "0.0412", "0.0625", "109.6", "81.0", "48.7", "9.3", "0.047", "0.852", "0.987", "0.845 ± 0.014",
               "52 of 114", "96 of 105", "31,434", "27,642", "0.916", "6.2 days", "6.7 days"]
NO_CODE = [("Section 3.3.1.1; Appendix D", "manual spot-check of 12 records of the Layer 1 reference set against the PDF", "manual check; the reference set itself is produced by layer1_extract_coord_*.py and evaluated by layer1_evaluate.py")]

def main(path, thesis=None):
    here = os.path.dirname(os.path.abspath(path)); claims = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "thesis_claims.json")))
    src = {"results": json.load(open(path))}; used = {"results": os.path.relpath(os.path.abspath(path), os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}
    code = os.path.dirname(os.path.abspath(__file__)); repo = os.path.dirname(code)
    candidates = {"extra": [os.path.join(code, "results_extra", "extra_results.json"), os.path.join(repo, "results", "extra_robustness", "extra_results.json")],
                  "cybattt": [os.path.join(code, "results_cybattt", "cybattt_results.json"), os.path.join(repo, "results", "cybattt", "cybattt_results.json")],
                  "layer1_text_eval": [os.path.join(repo, "layer1_ecc", "layer1_text_eval.json")],
                  "linking_comparison": [os.path.join(repo, "layer1_ecc", "linking_comparison.json")]}
    for k, paths in candidates.items():
        for c in paths:
            if os.path.exists(c):
                src[k] = json.load(open(c)); used[k] = os.path.relpath(c, repo); break
    rows = []; nm = nd = 0
    for loc, label, p, val, tol, s in claims:
        if s not in src: rows.append((loc, label, val, None, "MISSING")); continue
        try: got = g(src[s], p)
        except (KeyError, IndexError, TypeError, ValueError): rows.append((loc, label, val, None, "MISSING")); continue
        ok = abs(got - val) <= tol + 1e-12; nm += ok; nd += (not ok); rows.append((loc, label, val, got, "MATCH" if ok else "DIFF"))
    miss = [r for r in rows if r[4] == "MISSING"]; nd += len(miss)
    out = [f"# Thesis vs code", f"\n{nm} MATCH, {nd} DIFF/MISSING, {len(NO_CODE)} item without code.\n",
           "Files read: " + "; ".join(f"{k} = {v}" for k, v in used.items()) + "\n", "| Thesis location | Quantity | Thesis | Code | Status |", "|---|---|---|---|---|"]
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
