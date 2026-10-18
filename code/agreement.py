#!/usr/bin/env python3
"""Agreement between the human reviewer(s) and the model labels on the review sample (see label_tweets_llm.py)."""
import argparse, csv, json
import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix, accuracy_score
ap = argparse.ArgumentParser(); ap.add_argument("--labeled", required=True); ap.add_argument("--review", required=True); ap.add_argument("--out", default="agreement.json")
a = ap.parse_args()
lab = [int(r["label"]) for r in csv.DictReader(open(a.labeled, encoding="utf8"))]
rev = [r for r in csv.DictReader(open(a.review, encoding="utf8")) if r["human_label"].strip() != ""]
if not rev: raise SystemExit("No human labels found: fill the human_label column (0/1/2) first.")
h = np.array([int(r["human_label"]) for r in rev]); m = np.array([lab[int(r["row_id"])] for r in rev])
res = {"n_reviewed": int(len(h)), "accuracy_model_vs_human": float(accuracy_score(h, m)), "cohen_kappa": float(cohen_kappa_score(h, m)),
       "confusion_rows_human_cols_model": confusion_matrix(h, m, labels=[0, 1, 2]).tolist()}
json.dump(res, open(a.out, "w"), indent=2); print(json.dumps(res, indent=2))
