#!/usr/bin/env python3
"""
Extra analyses requested by the thesis review (v2 code package; does NOT change any existing table).

  A. template-family-held-out evaluation (leave-one-template-index-out, 4 folds), strict: held-out templates also removed
     from the training confuser fragments
  B. domain-held-out evaluation (4 folds x 3 held-out domains)
  C. author-written paraphrase test set (NOT expert annotation)
  D. exact / near-duplicate overlap between train and test in the standard stratified split
  E. paired bootstrap CIs on the standard test set (XGBoost vs logistic regression; macro F1)
  F. remediation: linear regime (as in the thesis) + two non-linear reward regimes, bootstrap CIs, strongest baseline first
  G. forecaster: per-organisation MAE variability and bootstrap CI of the gain over the moving average
  H. Layer 1: structural checks computable from controls.csv (precision needs the PDF / a hand-annotated gold file)
  I. one EXECUTED traced record: post -> Layer-1 link -> classifier -> CUSUM -> forecast -> remediation ranking

    python extra_analysis.py --seed 42 [--quick] [--out results_extra]
Same RNG stream as run_experiment.py (posts first, then audit simulation), so the data are identical to results/.
"""
import argparse, json, os, time
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

import common
from common import DOMAINS, EN, AR, HASH, CLASSES, simulate_audits, cusum_alarms, eval_alarms, split_orgs, make_tweets
import layer1_link
from run_experiment import make_windows

OUT_DEFAULT = "results_extra"


# ------------------------------------------------------------------ posts with template bookkeeping
def make_tweets_meta(n, rng, p_confuser=0.35, p_dropout=0.15):
    """Identical RNG order to common.make_tweets; additionally records main/confuser template indices."""
    rows = []
    for _ in range(n):
        y = int(rng.choice(3, p=[0.35, 0.35, 0.30]))
        lang = "ar" if rng.random() < 0.5 else "en"
        T = AR if lang == "ar" else EN
        di = int(rng.integers(12)); d = DOMAINS[di]
        dom = d[1] if lang == "ar" else d[0]
        ti = int(rng.integers(4))
        text = T[y][ti].format(d=dom)
        y2, ti2 = -1, -1
        if rng.random() < p_confuser:
            y2 = int(rng.choice([c for c in range(3) if c != y]))
            ti2 = int(rng.integers(4))
            text += " " + T[y2][ti2].format(d=dom)
        toks = [t for t in text.split() if rng.random() > p_dropout]
        text = " ".join(toks) + " " + HASH[rng.integers(len(HASH))]
        rows.append((text.strip(), y, lang, dom, di, ti, y2, ti2))
    return pd.DataFrame(rows, columns=["text", "label", "lang", "domain", "domain_id", "tmpl", "conf_label", "conf_tmpl"])


def vec_():
    return TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=5, max_features=4000, sublinear_tf=True)


def xgb_(seed, quick):
    return XGBClassifier(n_estimators=60 if quick else 150, max_depth=5, learning_rate=0.1, subsample=0.8, colsample_bytree=0.5,
                         tree_method="hist", n_jobs=4, random_state=seed, eval_metric="mlogloss")


def fit_eval(Xtr, ytr, Xte, yte, seed, C, quick):
    v = vec_(); A = v.fit_transform(Xtr); B = v.transform(Xte)
    lr = LogisticRegression(C=C, max_iter=500).fit(A, ytr)
    xg = xgb_(seed, quick).fit(A, ytr)
    return {"xgboost_macro_f1": float(f1_score(yte, xg.predict(B), average="macro")),
            "logreg_macro_f1": float(f1_score(yte, lr.predict(B), average="macro")),
            "n_train": int(len(ytr)), "n_test": int(len(yte))}, v, lr, xg


def agg(folds, keys=("xgboost_macro_f1", "logreg_macro_f1")):
    return {k: {"mean": float(np.mean([f[k] for f in folds])), "sd": float(np.std([f[k] for f in folds])),
                "per_fold": [f[k] for f in folds]} for k in keys}


# ------------------------------------------------------------------ C. paraphrases (author-written)
PARA_EN = {0: ["The latest NCA review of our {d} found everything in order; we meet every requirement.",
               "{d} controls have been fully implemented and independently verified against ECC.",
               "We are pleased to report that {d} satisfies the Authority's essential controls.",
               "After remediation, our {d} environment now conforms to the NCA standard.",
               "Auditors signed off on {d}: all ECC requirements are satisfied."],
           1: ["Our {d} setup does not satisfy the NCA controls and several findings remain unresolved.",
               "The assessment exposed serious shortcomings in {d}; required safeguards are absent.",
               "We are still failing the ECC requirements for {d}, with no corrective action in place.",
               "{d} falls short of the Authority's baseline and the audit flagged it as a breach.",
               "Auditors rejected {d}: mandatory controls were never put in place."],
           2: ["A new report this week looks at how {d} is changing across the industry.",
               "Join our online session on {d} and emerging threats next month.",
               "Security teams are discussing {d} after the latest industry survey.",
               "Reminder: registration for the cyber conference on {d} closes soon.",
               "Experts share opinions about {d} in a new podcast episode."]}
PARA_AR = {0: ["أظهرت مراجعة الهيئة الأخيرة أن {d} لدينا مستوفٍ لجميع المتطلبات.",
               "تم تنفيذ ضوابط {d} بالكامل والتحقق منها بشكل مستقل.",
               "يسعدنا الإعلان أن {d} يطابق الضوابط الأساسية للأمن السيبراني.",
               "بعد المعالجة أصبحت بيئة {d} لدينا ملتزمة بمعيار الهيئة.",
               "اعتمد المدققون {d} وجميع المتطلبات مستوفاة."],
           1: ["إجراءات {d} لدينا لا تلبي ضوابط الهيئة وما زالت ملاحظات عديدة دون حل.",
               "كشف التقييم قصورا خطيرا في {d} والضمانات المطلوبة غير موجودة.",
               "ما زلنا لا نستوفي متطلبات الضوابط في {d} دون أي إجراء تصحيحي.",
               "{d} دون الحد الأدنى للهيئة وصنفه التدقيق كمخالفة.",
               "رفض المدققون {d} لأن الضوابط الإلزامية لم تُطبق أصلا."],
           2: ["تقرير جديد هذا الأسبوع يتناول تطور {d} في القطاع.",
               "انضموا إلى جلستنا الإلكترونية حول {d} والتهديدات الناشئة الشهر القادم.",
               "يناقش فريق الأمن {d} بعد آخر استطلاع للقطاع.",
               "تذكير: التسجيل في المؤتمر السيبراني حول {d} يغلق قريبا.",
               "يشارك خبراء آراءهم حول {d} في حلقة بودكاست جديدة."]}


def paraphrase_set():
    rows = []
    for lang, P in (("en", PARA_EN), ("ar", PARA_AR)):
        for y, lst in P.items():
            for s in lst:
                for di, d in enumerate(DOMAINS):
                    rows.append((s.format(d=d[1] if lang == "ar" else d[0]), y, lang, di))
    return pd.DataFrame(rows, columns=["text", "label", "lang", "domain_id"])


# ------------------------------------------------------------------ E. bootstrap
def boot_f1(y, p1, p2, B, seed):
    r = np.random.default_rng(seed); n = len(y); d = []; a = []; b = []
    for _ in range(B):
        i = r.integers(0, n, n)
        f1 = f1_score(y[i], p1[i], average="macro"); f2 = f1_score(y[i], p2[i], average="macro")
        a.append(f1); b.append(f2); d.append(f2 - f1)
    ci = lambda x: [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]
    return {"xgboost_ci95": ci(a), "logreg_ci95": ci(b), "logreg_minus_xgboost_diff_ci95": ci(d),
            "prob_logreg_better": float(np.mean(np.array(d) > 0))}


# ------------------------------------------------------------------ F. remediation under several reward regimes
REGIMES = {"linear (thesis)": lambda r, e: r * e,
           "concave: sqrt(risk) x effectiveness": lambda r, e: np.sqrt(np.clip(r, 0, None)) * e,
           "threshold: only risk > 0.3 pays": lambda r, e: r * e * (r > 0.3)}


def remediation_regimes(true, n_orgs, seed, quick, K=4, B=1000):
    out = {}
    for name, rf in REGIMES.items():
        rng = np.random.default_rng(seed + 33)
        eff = np.random.default_rng(seed + 1).uniform(0.2, 0.8, 12)
        perm = np.random.default_rng(seed + 22).permutation(n_orgs); cut = int(0.85 * n_orgs)
        snap = lambda orgs, n: np.array([true[rng.choice(orgs), :, rng.integers(60, true.shape[2])] for _ in range(n)])
        S_tr = snap(perm[:cut], 3000 if quick else 20000); S_te = snap(perm[cut:], 3000)
        w = np.zeros(12); b = np.zeros(12); lr = 0.05
        for ep, r in enumerate(S_tr):
            eps = max(0.05, 0.5 * (1 - ep / len(S_tr))); chosen = []
            for _ in range(K):
                q = w * r + b; q[chosen] = -np.inf
                a = int(rng.choice([d for d in range(12) if d not in chosen])) if rng.random() < eps else int(q.argmax())
                rew = float(rf(r[a], eff[a])) + rng.normal(0, 0.01)
                err = rew - (w[a] * r[a] + b[a]); w[a] += lr * err * r[a]; b[a] += lr * err; chosen.append(a)

        def pick(r, pol):
            if pol == "agent": return list(np.argsort(-(w * r + b))[:K])
            if pol == "fixed_order": return list(range(K))
            if pol == "random": return list(rng.choice(12, K, replace=False))
            if pol == "highest_risk": return list(np.argsort(-r)[:K])
            if pol == "oracle": return list(np.argsort(-rf(r, eff))[:K])
        res = {pol: np.array([sum(float(rf(r[a], eff[a])) for a in pick(r, pol)) for r in S_te])
               for pol in ["highest_risk", "agent", "oracle", "random", "fixed_order"]}
        br = np.random.default_rng(seed + 5); n = len(S_te); gains = []; gap = []
        for _ in range(B):
            i = br.integers(0, n, n)
            gains.append(100 * (res["agent"][i].mean() / res["highest_risk"][i].mean() - 1))
            gap.append(100 * (res["agent"][i].mean() / res["oracle"][i].mean()))
        ci = lambda x: [float(np.percentile(x, 2.5)), float(np.percentile(x, 97.5))]
        out[name] = {"mean_total_reward": {k: float(v.mean()) for k, v in res.items()},
                     "agent_vs_highest_risk_pct": float(100 * (res["agent"].mean() / res["highest_risk"].mean() - 1)),
                     "agent_vs_highest_risk_ci95": ci(gains),
                     "agent_vs_fixed_order_pct": float(100 * (res["agent"].mean() / res["fixed_order"].mean() - 1)),
                     "agent_share_of_oracle_pct": float(100 * res["agent"].mean() / res["oracle"].mean()),
                     "agent_share_of_oracle_ci95": ci(gap), "n_test_states": int(n)}
    return out, (w, b)


# ------------------------------------------------------------------ G. forecaster (also returns models for I)
def forecaster_variability(obs, n_orgs, seed, quick, B=1000):
    perm = np.random.default_rng(seed + 22).permutation(n_orgs)
    ntr, nva = int(0.70 * n_orgs), int(0.15 * n_orgs)
    tr, va, te = perm[:ntr], perm[ntr:ntr + nva], perm[ntr + nva:]
    res, models = {}, {}
    for h in [7, 14, 30]:
        Xtr, ytr, _ = make_windows(obs, tr, h); Xva, yva, _ = make_windows(obs, va, h)
        m = HistGradientBoostingRegressor(max_iter=80 if quick else 250, learning_rate=0.08, early_stopping=True,
                                          random_state=seed).fit(np.vstack([Xtr, Xva]), np.concatenate([ytr, yva]))
        models[h] = m; per = []
        for o in te:
            X, y, base = make_windows(obs, [o], h)
            per.append((np.abs(y - m.predict(X)).mean(), np.abs(y - base[:, 1]).mean(), np.abs(y - base[:, 0]).mean()))
        per = np.array(per); br = np.random.default_rng(seed + h); gain = []
        for _ in range(B):
            i = br.integers(0, len(per), len(per)); s = per[i].mean(0); gain.append(100 * (1 - s[0] / s[1]))
        res[f"h{h}"] = {"n_test_orgs": int(len(te)),
                        "mae_model_mean_over_orgs": float(per[:, 0].mean()), "mae_model_sd_over_orgs": float(per[:, 0].std(ddof=1)),
                        "mae_ma7_mean_over_orgs": float(per[:, 1].mean()), "mae_persistence_mean_over_orgs": float(per[:, 2].mean()),
                        "gain_vs_ma7_pct_mean": float(100 * (1 - per[:, 0].mean() / per[:, 1].mean())),
                        "gain_vs_ma7_pct_ci95": [float(np.percentile(gain, 2.5)), float(np.percentile(gain, 97.5))],
                        "share_orgs_model_beats_ma7": float(np.mean(per[:, 0] < per[:, 1]))}
    return res, models


# ------------------------------------------------------------------ main
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42); ap.add_argument("--n_tweets", type=int, default=48760)
    ap.add_argument("--n_orgs", type=int, default=200); ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--controls", default="controls.csv"); ap.add_argument("--main_results", default="results/results.json")
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    if a.quick: a.n_tweets, a.n_orgs = 6000, 60
    os.makedirs(a.out, exist_ok=True); t0 = time.time(); R = {"config": vars(a).copy(), "environment": common.env_info()}
    rng = np.random.default_rng(a.seed)
    df = make_tweets_meta(a.n_tweets, rng)
    # sanity: same posts as common.make_tweets with the same seed
    chk = make_tweets(min(a.n_tweets, 3000), np.random.default_rng(a.seed))
    assert (chk.text.values == df.text.values[:len(chk)]).all(), "generator replica differs from common.make_tweets"
    R["generator_replica_identical_to_common_make_tweets_first_3000"] = True
    true, obs, events = simulate_audits(a.n_orgs, rng)
    C = 1.0
    if os.path.exists(a.main_results):
        C = json.load(open(a.main_results))["classifier"]["logreg"]["C"]
    R["logreg_C_frozen_from_main_run"] = C

    # ---- baseline replica of the standard split (same as run_classifier)
    X_tr, X_tmp, y_tr, y_tmp = train_test_split(df.text, df.label, test_size=0.30, stratify=df.label, random_state=a.seed)
    X_va, X_te, y_va, y_te = train_test_split(X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=a.seed)
    v0 = vec_(); A0 = v0.fit_transform(X_tr); T0 = v0.transform(X_te)
    best = None
    for c_ in [0.3, 1, 3, 10]:
        m = LogisticRegression(C=c_, max_iter=500).fit(A0, y_tr); s = f1_score(y_va, m.predict(v0.transform(X_va)), average="macro")
        if best is None or s > best[0]: best = (s, c_, m)
    lr0 = best[2]
    xg0 = xgb_(a.seed, a.quick).fit(A0, y_tr, eval_set=[(v0.transform(X_va), y_va)], verbose=False)
    p_x = xg0.predict(T0); p_l = lr0.predict(T0)
    R["standard_split_replica"] = {"xgboost_macro_f1": float(f1_score(y_te, p_x, average="macro")),
                                   "logreg_macro_f1": float(f1_score(y_te, p_l, average="macro")), "C": best[1]}
    print("replica", R["standard_split_replica"], round(time.time() - t0), flush=True)

    # ---- E. bootstrap on the standard test set
    R["E_bootstrap_standard_test"] = boot_f1(y_te.values, p_x, p_l, 200 if a.quick else 1000, a.seed)

    # ---- D. overlap
    tr_idx, te_idx = X_tr.index, X_te.index
    trtexts = set(df.loc[tr_idx, "text"]); exact = float(df.loc[te_idx, "text"].isin(trtexts).mean())
    sig = lambda d: list(zip(d.lang, d.label, d.tmpl, d.domain_id, d.conf_label, d.conf_tmpl))
    trsig = set(sig(df.loc[tr_idx])); near = float(np.mean([s in trsig for s in sig(df.loc[te_idx])]))
    trfam = set(zip(df.loc[tr_idx].lang, df.loc[tr_idx].label, df.loc[tr_idx].tmpl))
    famshare = float(np.mean([f in trfam for f in zip(df.loc[te_idx].lang, df.loc[te_idx].label, df.loc[te_idx].tmpl)]))
    R["D_overlap_standard_split"] = {"test_posts_with_exact_text_in_train": exact,
                                     "test_posts_whose_generating_signature_(lang,class,template,domain,confuser) occurs in train": near,
                                     "test_posts_whose_main_template_family_occurs_in_train": famshare,
                                     "n_template_families": int(len(set(zip(df.lang, df.label, df.tmpl)))),
                                     "note": "signature = generating parameters before token dropout; a match means a near-duplicate up to dropped tokens/hashtag"}

    # ---- A. template-held-out (leave one template index out; strict)
    folds = []
    for k in range(4):
        te_m = df.tmpl == k
        tr_m = (df.tmpl != k) & (df.conf_tmpl != k)
        f, *_ = fit_eval(df.text[tr_m], df.label[tr_m], df.text[te_m], df.label[te_m], a.seed, C, a.quick); f["held_out_template_index"] = k
        folds.append(f); print("A fold", k, f, round(time.time() - t0), flush=True)
    R["A_template_held_out_strict"] = {"folds": folds, **agg(folds),
                                       "note": "test posts are built on main templates never seen in training (neither as main text nor as confuser fragment)"}

    # ---- B. domain-held-out
    dperm = np.random.default_rng(a.seed + 7).permutation(12); folds = []
    for k in range(4):
        held = set(dperm[3 * k:3 * k + 3].tolist()); te_m = df.domain_id.isin(held)
        f, *_ = fit_eval(df.text[~te_m], df.label[~te_m], df.text[te_m], df.label[te_m], a.seed, C, a.quick); f["held_out_domain_ids"] = sorted(held)
        folds.append(f); print("B fold", k, f, round(time.time() - t0), flush=True)
    R["B_domain_held_out"] = {"folds": folds, **agg(folds)}

    # ---- C. paraphrase test (train on the standard training partition)
    pp = paraphrase_set(); Bp = v0.transform(pp.text)
    R["C_paraphrase_author_written"] = {"n_posts": int(len(pp)), "n_distinct_sentences": int(len(pp) // 12),
                                        "xgboost_macro_f1": float(f1_score(pp.label, xg0.predict(Bp), average="macro")),
                                        "logreg_macro_f1": float(f1_score(pp.label, lr0.predict(Bp), average="macro")),
                                        "per_language_xgboost": {l: float(f1_score(pp.label[pp.lang == l], xg0.predict(Bp[(pp.lang == l).values]), average="macro")) for l in ["en", "ar"]},
                                        "per_language_logreg": {l: float(f1_score(pp.label[pp.lang == l], lr0.predict(Bp[(pp.lang == l).values]), average="macro")) for l in ["en", "ar"]},
                                        "note": "30 sentences (5 per class and language) written by the thesis author, balanced; labels by construction; not expert annotation; small"}
    print("C", R["C_paraphrase_author_written"], flush=True)

    # ---- F. remediation regimes
    R["F_remediation_regimes"], (w_, b_) = remediation_regimes(true, a.n_orgs, a.seed, a.quick); print("F done", round(time.time() - t0), flush=True)

    # ---- G. forecaster variability
    R["G_forecaster_variability"], fmodels = forecaster_variability(obs, a.n_orgs, a.seed, a.quick); print("G done", round(time.time() - t0), flush=True)

    # ---- H. Layer 1 structural checks
    kb = layer1_link.load_controls(a.controls)
    ids = kb.control_id.tolist()
    R["H_layer1_structural"] = {"n_records": len(kb), "duplicate_ids": int(len(ids) - len(set(ids))),
                                "ids_with_unknown_ecc_subdomain": int((~kb.ecc_sub.isin(common.ECC_SUB)).sum()),
                                "ids_with_unknown_main_domain": int((~kb.control_id.str.extract(r"^(\d+)-")[0].isin(common.ECC_MAIN)).sum()),
                                "level3_per_subdomain_min_max": [int(kb[kb.level == 3].groupby("ecc_sub").size().min()), int(kb[kb.level == 3].groupby("ecc_sub").size().max())],
                                "note": "These checks do not give precision. Precision/recall against the source needs the ECC-1:2018 PDF or a hand-annotated gold.csv (layer1_extract.py --gold)."}

    # ---- I. executed traced record
    val, test = split_orgs(a.n_orgs, a.seed); cp = json.load(open(a.main_results))["drift_and_mttd"] if os.path.exists(a.main_results) else {"cusum_k": 2.0, "cusum_h": 20}
    k_, h_ = cp["cusum_k"], cp["cusum_h"]
    al = cusum_alarms(obs, h_, k_); m_, ev = eval_alarms(al, events, list(test)); ev = ev[ev.d_pipe.notna()].reset_index(drop=True)
    e0 = ev.iloc[0]; o, dom = int(e0.org), int(e0.dom); day = int(e0.onset + e0.d_pipe)
    # post: first English non-compliant test-partition post of this domain
    cand = df.loc[X_te.index]; cand = cand[(cand.lang == "en") & (cand.label == 1) & (cand.domain_id == dom)]
    post = cand.iloc[0]
    proba = xg0.predict_proba(v0.transform([post.text]))[0]
    kbv = layer1_link._vectorizer("word"); K = kbv.fit_transform(kb.text); sims = (kbv.transform([post.text]) @ K.T).toarray()[0]
    top = int(sims.argmax())
    mu = obs[o, dom, :30].mean(); sd = obs[o, dom, :30].std() + 1e-6; S = 0.0; stat_at = None
    for t in range(30, day + 1):
        S_prev = S; S = max(0.0, S + (obs[o, dom, t] - mu) / sd - k_)
        if t == day: stat_at = float(S)
        if S > h_ and t < day: S = 0.0
    w30 = obs[o, dom, day - 29:day + 1]
    feat = lambda w, d: np.concatenate([w, [w[-7:].mean(), w.mean(), w.std(), w[-7:].mean() - w[-14:-7].mean()], np.eye(12)[d]])[None]
    risk_now = true[o, :, day]
    ranking = list(np.argsort(-(w_ * risk_now + b_))[:4])
    R["I_traced_record_executed"] = {
        "note": "Executed run on synthetic data. The post and the audit series are joined only through the shared simulated domain; this shows that module outputs can be chained in one record, not that the post is evidence about the simulated organisation.",
        "org": o, "domain": DOMAINS[dom][0], "alarm_day": day, "event_onset": int(e0.onset), "detection_delay_days": float(e0.d_pipe),
        "post_text": post.text, "post_true_label": CLASSES[int(post.label)],
        "layer1_link": {"method": "word TF-IDF cosine", "matched_control_id": kb.control_id.iloc[top], "matched_subdomain": str(kb.ecc_sub_name.iloc[top]),
                        "similarity": float(sims[top]), "matched_control_is_in_post_domain": bool(kb.sim_domain_id.iloc[top] == dom)},
        "layer3_classification": {"predicted": CLASSES[int(proba.argmax())], "probabilities": {c: float(p) for c, p in zip(CLASSES, proba)}},
        "layer3_drift": {"cusum_k": k_, "cusum_h": h_, "cusum_statistic_at_alarm_day": stat_at, "alarm": True},
        "layer3_forecast": {"current_observed_risk": float(obs[o, dom, day]),
                            "forecast_7d": float(fmodels[7].predict(feat(w30, dom))[0]), "forecast_30d": float(fmodels[30].predict(feat(w30, dom))[0])},
        "layer3_remediation_top4_domains": [DOMAINS[i][0] for i in ranking], "remediation_policy": "linear-Q contextual bandit (one-step)"}
    R["runtime_seconds"] = round(time.time() - t0)
    json.dump(R, open(os.path.join(a.out, "extra_results.json"), "w"), indent=2, ensure_ascii=False)
    print(json.dumps(R, indent=1, ensure_ascii=False)[:6000])
