#!/usr/bin/env python3
"""
CybAttT external-validation experiment (thesis Sections 3.4.2.1 and 5.4, Table 5.4).

DATA : df_m.csv from https://github.com/HudaLughbi/CybAttT (columns text, anottator1-3, majority). Not redistributed here:
        download it first (see README).  --selftest runs the code on a tiny FAKE file only to check that it executes.

Input : CybAttT CSV with the tweet text and the three annotators' labels (one column per annotator).
        Column names differ between releases, so they are arguments.
Steps : (1) @mentions -> @user, links -> URL; (2) majority vote of the 3 annotators, tweets without a majority dropped;
        (3) exact duplicate texts dropped; (4) Fleiss kappa and pairwise Cohen kappa from the annotation columns;
        (5) same features / split / models as the synthetic experiment (char 2-4 TF-IDF, 4000 features, stratified 70/15/15,
            majority-class baseline instead of keyword rules, LogReg C tuned on validation, XGBoost 150 trees depth 5, 5-fold CV).
Output: <out>/cybattt_clean.csv, <out>/cybattt_results.json

Usage : python cybattt_pipeline.py --input CybAttT.csv --text_col text --annotator_cols ann1,ann2,ann3 --out results_cybattt
        python cybattt_pipeline.py --selftest
"""
import argparse, itertools, json, os, re
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, roc_auc_score, confusion_matrix, cohen_kappa_score
from sklearn.model_selection import train_test_split, StratifiedKFold
from xgboost import XGBClassifier

MENTION = re.compile(r"@\w+"); LINK = re.compile(r"https?://\S+|www\.\S+")
NAMES = ["high_risk_news", "normal_news", "not_news"]


def clean_text(t):
    return re.sub(r"\s+", " ", LINK.sub("URL", MENTION.sub("@user", str(t)))).strip()


def fleiss_kappa(M):
    """M: (n_items, n_categories) counts of raters per category; every item has the same number of raters."""
    n = M.sum(1)[0]; N = M.shape[0]
    p_j = M.sum(0) / (N * n); P_i = ((M ** 2).sum(1) - n) / (n * (n - 1))
    Pbar, Pe = P_i.mean(), (p_j ** 2).sum()
    return float((Pbar - Pe) / (1 - Pe))


def prepare(raw, text_col, ann_cols, label_names):
    labs = raw[ann_cols].apply(lambda s: s.map(label_names))
    counts = np.stack([(labs == k).sum(axis=1).values for k in range(len(set(label_names.values())))], 1)
    major = counts.max(1) > len(ann_cols) / 2
    L, C = labs[major], counts[major]                                   # agreement computed on the tweets that have a majority label
    kap = {"fleiss_majority_labeled": fleiss_kappa(C),
           "pairwise_cohen": {f"{a}|{b}": float(cohen_kappa_score(L[a], L[b])) for a, b in itertools.combinations(ann_cols, 2)}}
    df = pd.DataFrame({"text": raw[text_col].map(clean_text), "label": counts.argmax(1)})[major]
    n_raw, n_nomaj = len(raw), int((~major).sum())
    df = df.drop_duplicates("text").reset_index(drop=True)
    return df, kap, {"n_labeled": n_raw, "n_without_majority": n_nomaj, "n_after_dedup": int(len(df)),
                     "class_counts": {NAMES[k]: int((df.label == k).sum()) for k in range(3)}}


def run(df, seed, outdir):
    X_tr, X_tmp, y_tr, y_tmp = train_test_split(df.text, df.label, test_size=0.30, stratify=df.label, random_state=seed)
    X_va, X_te, y_va, y_te = train_test_split(X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=seed)
    mk = lambda: TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=5, max_features=4000, sublinear_tf=True)
    vec = mk(); A_tr = vec.fit_transform(X_tr); A_va = vec.transform(X_va); A_te = vec.transform(X_te)
    res = {"n_train": len(y_tr), "n_val": len(y_va), "n_test": len(y_te)}
    maj = int(y_tr.value_counts().idxmax()); res["majority_baseline_macro_f1"] = float(f1_score(y_te, np.full(len(y_te), maj), average="macro"))
    def met(pred, proba):
        return {"macro_f1": float(f1_score(y_te, pred, average="macro")), "auc_ovr_macro": float(roc_auc_score(y_te, proba, multi_class="ovr", average="macro")),
                "per_class_f1": dict(zip(NAMES, map(float, f1_score(y_te, pred, average=None)))), "confusion_matrix": confusion_matrix(y_te, pred).tolist()}
    best = None
    for C in [0.3, 1, 3, 10]:
        m = LogisticRegression(C=C, max_iter=500).fit(A_tr, y_tr); s = f1_score(y_va, m.predict(A_va), average="macro")
        if best is None or s > best[0]: best = (s, C, m)
    res["logreg"] = met(best[2].predict(A_te), best[2].predict_proba(A_te)); res["logreg"]["C"] = best[1]
    kw = dict(n_estimators=150, max_depth=5, learning_rate=0.1, subsample=0.8, colsample_bytree=0.5, tree_method="hist", n_jobs=1, random_state=seed)
    xgb = XGBClassifier(eval_metric="mlogloss", **kw).fit(A_tr, y_tr, eval_set=[(A_va, y_va)], verbose=False)
    p = xgb.predict_proba(A_te); res["xgboost"] = met(p.argmax(1), p)
    cm = np.array(res["xgboost"]["confusion_matrix"]); res["xgboost"]["high_risk_recall"] = float(cm[0, 0] / cm[0].sum()); res["xgboost"]["high_risk_hits"] = f"{cm[0,0]} of {cm[0].sum()}"
    Xall = pd.concat([X_tr, X_va]); yall = pd.concat([y_tr, y_va]); f1s = []
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=seed).split(Xall, yall):
        v = mk(); a = v.fit_transform(Xall.iloc[tr]); b = v.transform(Xall.iloc[te])
        f1s.append(float(f1_score(yall.iloc[te], XGBClassifier(**kw).fit(a, yall.iloc[tr]).predict(b), average="macro")))
    res["xgboost"]["cv5_fold_macro_f1"] = f1s; res["xgboost"]["cv5_mean"] = float(np.mean(f1s)); res["xgboost"]["cv5_sd"] = float(np.std(f1s))
    return res


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--input"); ap.add_argument("--text_col", default="text")
    ap.add_argument("--annotator_cols", default="anottator1,anottator2,anottator3", help="three comma-separated columns (spelling as in the CybAttT release)")
    ap.add_argument("--label_map", default='{"High_Risk_News":0,"Normal_News":1,"Not_News":2}', help="JSON: annotator value -> class index 0/1/2 (high/normal/not)")
    ap.add_argument("--out", default="results_cybattt"); ap.add_argument("--seed", type=int, default=42); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    if a.selftest:                                  # FAKE data, only to test that the code runs
        r = np.random.default_rng(0); n = 1500; y = r.choice(3, n, p=[0.05, 0.12, 0.83])
        words = [["breach", "ransomware", "attack", "hacked", "leak"], ["patch", "update", "report", "security", "vulnerability"], ["buy", "free", "sale", "win", "click"]]
        txt = [" ".join(r.choice(words[k], 6)) + f" @u{r.integers(50)} http://x.co/{i}" for i, k in enumerate(y)]
        flip = lambda: np.where(r.random(n) < 0.03, r.integers(0, 3, n), y)
        raw = pd.DataFrame({"text": txt, "ann1": flip(), "ann2": flip(), "ann3": flip()}); lm = {0: 0, 1: 1, 2: 2}; cols = ["ann1", "ann2", "ann3"]; tc = "text"
    else:
        raw = pd.read_csv(a.input); tc = a.text_col; cols = a.annotator_cols.split(","); lm = json.loads(a.label_map)
    df, kap, prep = prepare(raw, tc, cols, lm); df.to_csv(os.path.join(a.out, "cybattt_clean.csv"), index=False)
    R = {"source": "SELFTEST-FAKE-DATA" if a.selftest else a.input, "preparation": prep, "agreement": kap, "classification": run(df, a.seed, a.out)}
    json.dump(R, open(os.path.join(a.out, "cybattt_results.json"), "w"), indent=2); print(json.dumps(R, indent=2)[:2500])
