#!/usr/bin/env python3
"""
Layer 1 evaluation (thesis Sections 3.3.1.1, 5.3, 5.6 and Appendix D).

Regenerates the two Layer 1 evaluation files that are reported in the thesis:

  layer1_text_eval.json     identifier precision/recall of the baseline extractor (controls.csv) against the
                            reference set built from the ECC-1:2018 PDF (layer1_reference_from_pdf.json),
                            and token-level F1 of the extracted text for the matched records.
  linking_comparison.json   TF-IDF linking of the English test posts to controls with the baseline knowledge base
                            (controls.csv, 148 records) and with the coordinate-based knowledge base (219 records).

Usage (from code/):
    python layer1_evaluate.py --controls controls.csv \
        --reference ../layer1_ecc/layer1_reference_from_pdf.json \
        --tweets results/tweets_used.csv --out ../layer1_ecc

The reference set is a programmatic extraction with a 12-record manual spot-check; it is not an expert adjudication.
"""
import argparse, json, os
from collections import Counter
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split
import layer1_link



def token_f1(a, b):
    """Bag-of-tokens F1; tokens = lower-cased whitespace-separated strings."""
    ta, tb = Counter(a.lower().split()), Counter(b.lower().split())
    if not ta or not tb:
        return 0.0
    overlap = sum((ta & tb).values())
    if overlap == 0:
        return 0.0
    p, r = overlap / sum(ta.values()), overlap / sum(tb.values())
    return 2 * p * r / (p + r)


def id_eval(pred, gold):
    """pred, gold: DataFrames with control_id and text (one level)."""
    P, G = set(pred.control_id), set(gold.control_id)
    tp, fp, fn = len(P & G), len(P - G), len(G - P)
    g = dict(zip(gold.control_id, gold.text))
    f1s, exact = [], 0
    for cid, txt in zip(pred.control_id, pred.text):
        if cid in g:
            f1s.append(token_f1(txt, g[cid]))
            exact += int(" ".join(txt.split()).lower() == " ".join(g[cid].split()).lower())
    return {"gold": len(G), "extracted": len(P), "TP": tp, "FP": fp, "FN": fn,
            "precision_id": tp / len(P) if P else None, "recall_id": tp / len(G),
            "mean_token_f1_matched": float(np.mean(f1s)) if f1s else None,
            "exact_text_match": exact, "matched": len(f1s), "token_f1_ge_0.9": int(sum(f >= 0.9 for f in f1s))}


def english_test_posts(tweets_csv, seed):
    """Same stratified 70/15/15 split as run_experiment.run_classifier (seed 42)."""
    df = pd.read_csv(tweets_csv)
    _, X_tmp, _, y_tmp = train_test_split(df.text, df.label, test_size=0.30, stratify=df.label, random_state=seed)
    _, X_te, _, _ = train_test_split(X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=seed)
    te = df.loc[X_te.index]
    return te[te.lang == "en"]


def link_summary(posts, kb):
    w = layer1_link.link_posts(posts, kb, "word"); c = layer1_link.link_posts(posts, kb, "char")
    return {"n_kb": int(len(kb)), "word_top1": w["accuracy_top1_all"],
            "word_top1_no_domain_name": w["accuracy_top1_posts_without_domain_name"],
            "char_top1": c["accuracy_top1_all"], "char_top3": c["accuracy_top3_all"],
            "char_top1_with_name": c["accuracy_top1_posts_with_domain_name"],
            "char_top1_no_name": c["accuracy_top1_posts_without_domain_name"], "n_posts": w["n_posts"]}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--controls", default="controls.csv")
    ap.add_argument("--reference", default="../layer1_ecc/layer1_reference_from_pdf.json")
    ap.add_argument("--tweets", default="results/tweets_used.csv")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="../layer1_ecc")
    a = ap.parse_args()

    base = layer1_link.load_controls(a.controls)
    ref = pd.DataFrame(json.load(open(a.reference, encoding="utf8")))
    text_eval = {"controls": id_eval(base[base.level == 3], ref[ref.level == 3]),
                 "sub-controls": id_eval(base[base.level == 4], ref[ref.level == 4])}
    json.dump(text_eval, open(f"{a.out}/layer1_text_eval.json", "w"), indent=1)

    coord = ref[["control_id", "level", "text"]].copy(); coord["domain"] = ""; coord["subdomain"] = ""
    coord.to_csv("_coord_tmp.csv", index=False)
    coord_kb = layer1_link.load_controls("_coord_tmp.csv"); os.remove("_coord_tmp.csv")
    posts = english_test_posts(a.tweets, a.seed)
    comp = {"baseline_kb": link_summary(posts, base), "coordinate_kb": link_summary(posts, coord_kb)}
    json.dump(comp, open(f"{a.out}/linking_comparison.json", "w"), indent=1)
    print(json.dumps({"text_eval": text_eval, "linking": comp}, indent=1))
