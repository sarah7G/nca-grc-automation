#!/usr/bin/env python3
"""
Single reproducible entry point for ALL results of the thesis (Chapters 3 and 5).

    python run_experiment.py --seed 42            full run  (~15-25 min on one CPU core)
    python run_experiment.py --seed 42 --quick    smoke test (numbers differ from the thesis)

Everything is SYNTHETIC or SIMULATED unless --tweets_csv is given.  Copy numbers into the thesis ONLY from
results/results.json / results/results_tables.md; verify_thesis.py lists every thesis number next to the code output.

Modules
  Layer 1  controls.csv (output of layer1_extract.py on ECC-1:2018) as knowledge base: extraction report,
           12-domain -> ECC table, linking of English posts to controls (TF-IDF cosine)        -> layer1_link.py
  Layer 3  1. Compliance Status Classifier (TF-IDF + XGBoost; logistic regression; keyword rule; 5-fold CV per fold)
           2. Control Drift Detector (CUSUM) + MTTD vs periodic audits (90/180/365 d)
           3. Equal-frequency baselines (fixed threshold, EWMA) and sensitivity grid               -> baselines_sensitivity.py
           4. Risk forecaster (gradient boosting) vs moving average / persistence
           5. Remediation prioritiser (linear-Q contextual bandit) vs fixed / random / highest-risk / oracle
"""
import argparse, json, os, time
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import f1_score, roc_auc_score, confusion_matrix, mean_absolute_error, precision_score, recall_score
from sklearn.model_selection import train_test_split, StratifiedKFold
from xgboost import XGBClassifier

from common import (CLASSES, make_tweets, rule_baseline, simulate_audits, cusum_alarms, eval_alarms, audit_delays,
                    boot_reduction, split_orgs, env_info)
import layer1_link, baselines_sensitivity


# ----------------------------------------------------------------------------- 2. classifier
def run_classifier(df, seed, quick, outdir):
    X_tr, X_tmp, y_tr, y_tmp = train_test_split(df.text, df.label, test_size=0.30, stratify=df.label, random_state=seed)
    X_va, X_te, y_va, y_te = train_test_split(X_tmp, y_tmp, test_size=0.50, stratify=y_tmp, random_state=seed)
    mk_vec = lambda: TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4), min_df=5, max_features=4000, sublinear_tf=True)
    vec = mk_vec(); A_tr = vec.fit_transform(X_tr); A_va = vec.transform(X_va); A_te = vec.transform(X_te)
    res = {"n_train": len(y_tr), "n_val": len(y_va), "n_test": len(y_te)}

    def metrics(y, pred, proba):
        return {"macro_f1": float(f1_score(y, pred, average="macro")),
                "macro_precision": float(precision_score(y, pred, average="macro")),
                "macro_recall": float(recall_score(y, pred, average="macro")),
                "per_class_f1": dict(zip(CLASSES, map(float, f1_score(y, pred, average=None)))),
                "per_class_precision": dict(zip(CLASSES, map(float, precision_score(y, pred, average=None)))),
                "per_class_recall": dict(zip(CLASSES, map(float, recall_score(y, pred, average=None)))),
                "auc_ovr_macro": float(roc_auc_score(y, proba, multi_class="ovr", average="macro"))}

    rb = rule_baseline(X_te.values)
    res["rule_baseline"] = {"macro_f1": float(f1_score(y_te, rb, average="macro"))}
    best = None
    for C in [0.3, 1, 3, 10]:                       # tuned on validation set only
        m = LogisticRegression(C=C, max_iter=500).fit(A_tr, y_tr)
        s = f1_score(y_va, m.predict(A_va), average="macro")
        if best is None or s > best[0]: best = (s, C, m)
    lr = best[2]
    res["logreg"] = metrics(y_te, lr.predict(A_te), lr.predict_proba(A_te)); res["logreg"]["C"] = best[1]

    ne = 60 if quick else 150
    xgb_kw = dict(n_estimators=ne, max_depth=5, learning_rate=0.1, subsample=0.8, colsample_bytree=0.5, tree_method="hist", n_jobs=1, random_state=seed)
    xgb = XGBClassifier(eval_metric="mlogloss", **xgb_kw)
    xgb.fit(A_tr, y_tr, eval_set=[(A_va, y_va)], verbose=False)
    p = xgb.predict_proba(A_te); pred = p.argmax(1)
    res["xgboost"] = metrics(y_te, pred, p)
    res["xgboost"]["f1_gain_over_rule_baseline_pp"] = 100 * (res["xgboost"]["macro_f1"] - res["rule_baseline"]["macro_f1"])
    cm = confusion_matrix(y_te, pred); res["xgboost"]["confusion_matrix"] = cm.tolist()

    # 5-fold stratified CV on train+val (XGBoost, same settings) -- the five fold values of Table 5.5 come from here
    Xall = pd.concat([X_tr, X_va]); yall = pd.concat([y_tr, y_va]); f1s = []
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=seed).split(Xall, yall):
        v = mk_vec(); a = v.fit_transform(Xall.iloc[tr]); b = v.transform(Xall.iloc[te])
        m = XGBClassifier(**xgb_kw).fit(a, yall.iloc[tr])
        f1s.append(float(f1_score(yall.iloc[te], m.predict(b), average="macro")))
    res["xgboost"]["cv5_fold_macro_f1"] = f1s
    res["xgboost"]["cv5_macro_f1_mean"] = float(np.mean(f1s)); res["xgboost"]["cv5_macro_f1_sd"] = float(np.std(f1s))

    fig, ax = plt.subplots(figsize=(4.2, 3.8))
    ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(3)); ax.set_xticklabels(CLASSES, rotation=25); ax.set_yticks(range(3)); ax.set_yticklabels(CLASSES)
    for i in range(3):
        for j in range(3): ax.text(j, i, cm[i, j], ha="center", va="center")
    ax.set_title("Compliance Status Classifier (test)"); fig.tight_layout()
    fig.savefig(os.path.join(outdir, "fig_confusion.png"), dpi=150); plt.close(fig)
    return res, X_te.index


# ----------------------------------------------------------------------------- 4. drift detector vs periodic audit
def run_drift_mttd(obs, events, n_orgs, seed, outdir):
    val, test = split_orgs(n_orgs, seed)       # thresholds tuned on val orgs, reported on test orgs
    res = {"n_val_orgs": len(val), "n_test_orgs": len(test)}
    t = baselines_sensitivity.tune("cusum", obs, events, val)        # best recall (then lowest delay) s.t. <= 0.05 false alarms / series-year
    res["far_constraint_met_on_validation"] = t["budget_met_on_validation"]
    k_sel, h = t["params"]["k"], t["params"]["h"]
    res["cusum_k"] = k_sel; res["cusum_h"] = h
    al = cusum_alarms(obs, h, k_sel)
    m, ev = eval_alarms(al, events, list(test)); res["drift_detector_test"] = m
    res["n_test_events"] = int(len(ev))
    sens = {}
    dur = (ev.end - ev.onset).values.astype(float)
    for cycle in [90, 180, 365]:
        d_a = audit_delays(obs, events, list(test), cycle, np.random.default_rng(seed + cycle))
        dp = ev.d_pipe.values; both = ~np.isnan(dp) & ~np.isnan(d_a); org_e = ev.org.values
        dp_all = np.where(np.isnan(dp), dur, dp); da_all = np.where(np.isnan(d_a), dur, d_a)
        sens[str(cycle)] = {"audit_cycle_days": cycle, "audit_detection_rate": float(np.mean(~np.isnan(d_a))),
                            "pipeline_detection_rate": float(np.mean(~np.isnan(dp))), "n_paired_events": int(both.sum()),
                            "mttd_pipeline_days_paired": float(dp[both].mean()), "mttd_audit_days_paired": float(d_a[both].mean()),
                            "mttd_reduction_pct": float(100 * (1 - dp[both].mean() / d_a[both].mean())),
                            "reduction_ci95_pct": boot_reduction(dp[both], d_a[both], org_e[both], seed),
                            "mttd_pipeline_days_all": float(dp_all.mean()), "mttd_audit_days_all": float(da_all.mean()),
                            "mttd_reduction_pct_all": float(100 * (1 - dp_all.mean() / da_all.mean())),
                            "reduction_ci95_pct_all": boot_reduction(dp_all, da_all, org_e, seed)}
    res["mttd_by_audit_cycle"] = sens
    fig, ax = plt.subplots(figsize=(5.4, 3.4)); xs = np.arange(3); w = 0.38
    ax.bar(xs - w / 2, [sens[c]["mttd_audit_days_all"] for c in sens], w, label="periodic audit")
    ax.bar(xs + w / 2, [sens[c]["mttd_pipeline_days_all"] for c in sens], w, label="CUSUM pipeline")
    ax.set_xticks(xs); ax.set_xticklabels([f"{c}-day cycle" for c in sens]); ax.set_ylabel("MTTD (days, all events)")
    ax.legend(); fig.tight_layout(); fig.savefig(os.path.join(outdir, "fig_mttd.png"), dpi=150); plt.close(fig)
    return res


# ----------------------------------------------------------------------------- 5. forecaster
def make_windows(obs, orgs, h, stride=5, L=30):
    X, y, base = [], [], []
    for o in orgs:
        for d in range(obs.shape[1]):
            s = obs[o, d]
            for t in range(L - 1, obs.shape[2] - 1 - h, stride):
                w = s[t - L + 1:t + 1]
                oh = np.zeros(12); oh[d] = 1
                X.append(np.concatenate([w, [w[-7:].mean(), w.mean(), w.std(), w[-7:].mean() - w[-14:-7].mean()], oh]))
                y.append(s[t + h]); base.append((w[-1], w[-7:].mean()))
    return np.array(X), np.array(y), np.array(base)


def run_forecaster(obs, n_orgs, seed, quick, outdir):
    perm = np.random.default_rng(seed + 22).permutation(n_orgs)
    ntr, nva = int(0.70 * n_orgs), int(0.15 * n_orgs)
    tr, va, te = perm[:ntr], perm[ntr:ntr + nva], perm[ntr + nva:]
    res = {}
    for h in [7, 14, 30]:
        Xtr, ytr, _ = make_windows(obs, tr, h); Xva, yva, _ = make_windows(obs, va, h); Xte, yte, bte = make_windows(obs, te, h)
        m = HistGradientBoostingRegressor(max_iter=80 if quick else 250, learning_rate=0.08, early_stopping=True,
                                          random_state=seed).fit(np.vstack([Xtr, Xva]), np.concatenate([ytr, yva]))
        mae = mean_absolute_error(yte, m.predict(Xte)); ma7 = mean_absolute_error(yte, bte[:, 1]); per = mean_absolute_error(yte, bte[:, 0])
        res[f"h{h}"] = {"mae_model": float(mae), "mae_moving_avg7": float(ma7), "mae_persistence": float(per),
                        "improvement_vs_moving_avg_pct": float(100 * (1 - mae / ma7)),
                        "improvement_vs_persistence_pct": float(100 * (1 - mae / per)), "n_test_windows": int(len(yte))}
    fig, ax = plt.subplots(figsize=(5, 3.4)); xs = np.arange(3)
    for i, (k, lab) in enumerate([("mae_model", "gradient boosting"), ("mae_moving_avg7", "7-day moving avg"), ("mae_persistence", "persistence")]):
        ax.bar(xs + (i - 1) * 0.27, [res[f"h{h}"][k] for h in [7, 14, 30]], 0.27, label=lab)
    ax.set_xticks(xs); ax.set_xticklabels(["7d", "14d", "30d"]); ax.set_ylabel("MAE (risk score)"); ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(os.path.join(outdir, "fig_forecast.png"), dpi=150); plt.close(fig)
    return res


# ----------------------------------------------------------------------------- 6. remediation (linear-Q bandit)
def run_remediation(true, n_orgs, seed, quick, K=4):
    rng = np.random.default_rng(seed + 33)
    eff = np.random.default_rng(seed + 1).uniform(0.2, 0.8, 12)      # hidden per-domain remediation effectiveness
    perm = np.random.default_rng(seed + 22).permutation(n_orgs); cut = int(0.85 * n_orgs)
    snap = lambda orgs, n: np.array([true[rng.choice(orgs), :, rng.integers(60, true.shape[2])] for _ in range(n)])
    S_tr = snap(perm[:cut], 3000 if quick else 20000); S_te = snap(perm[cut:], 3000)
    w = np.zeros(12); b = np.zeros(12); lr = 0.05
    for ep, r in enumerate(S_tr):
        eps = max(0.05, 0.5 * (1 - ep / len(S_tr))); chosen = []
        for _ in range(K):
            q = w * r + b; q[chosen] = -np.inf
            a = int(rng.choice([d for d in range(12) if d not in chosen])) if rng.random() < eps else int(q.argmax())
            rew = r[a] * eff[a] + rng.normal(0, 0.01)
            err = rew - (w[a] * r[a] + b[a]); w[a] += lr * err * r[a]; b[a] += lr * err; chosen.append(a)

    def pick(r, policy):
        if policy == "agent": return list(np.argsort(-(w * r + b))[:K])
        if policy == "fixed_order": return list(range(K))
        if policy == "random": return list(rng.choice(12, K, replace=False))
        if policy == "highest_risk": return list(np.argsort(-r)[:K])
        if policy == "oracle": return list(np.argsort(-(r * eff))[:K])
    out = {}
    for pol in ["fixed_order", "random", "highest_risk", "agent", "oracle"]:
        out[pol] = np.array([sum(r[a] * eff[a] for a in pick(r, pol)) for r in S_te])
    base_red = out["fixed_order"].mean()
    return {"budget_actions_per_episode": K, "n_test_states": len(S_te),
            "mean_total_risk_reduction": {k: float(v.mean()) for k, v in out.items()},
            "compliance_score_gain_points_mean": {k: float((v / 12).mean() * 100) for k, v in out.items()},
            "agent_improvement_over_fixed_order_pct": float(100 * (out["agent"].mean() / base_red - 1)),
            "agent_improvement_over_random_pct": float(100 * (out["agent"].mean() / out["random"].mean() - 1)),
            "agent_improvement_over_highest_risk_pct": float(100 * (out["agent"].mean() / out["highest_risk"].mean() - 1)),
            "agent_share_of_oracle_pct": float(100 * out["agent"].mean() / out["oracle"].mean()),
            "learned_effectiveness_corr_with_truth": float(np.corrcoef(w, eff)[0, 1])}


# ----------------------------------------------------------------------------- tables
def md_tables(R):
    c = R["classifier"]; d = R["drift_and_mttd"]; f = R["forecaster"]; r = R["remediation"]; l1 = R["layer1"]; b = R["detector_comparison"]; g = R["sensitivity_cusum"]
    x = c["xgboost"]; e = R["environment"]
    L = ["# Results (simulated data; produced by run_experiment.py)\n",
         f"Seed {R['config']['seed']}; Python {e['python']}, xgboost {e['xgboost']}, scikit-learn {e['scikit_learn']}, numpy {e['numpy']}, pandas {e['pandas']}.",
         f"{R['config']['n_tweets']} synthetic posts, {R['config']['n_orgs']} simulated organisations x 12 domains x 365 days, {R['audit_simulation']['n_events']} injected gaps.\n",
         "## Layer 1 - ECC-1:2018 knowledge base (controls.csv)\n", "| Item | Value |", "|---|---|"]
    ex = l1["extraction"]
    L += [f"| Controls extracted (level 3) | {ex['n_controls_level3']} of {ex['official_controls']} ({ex['control_recall_pct']:.1f}%) |",
          f"| Sub-controls extracted (level 4) | {ex['n_subcontrols_level4']} of {ex['official_subcontrols']} ({ex['subcontrol_recall_pct']:.1f}%) |",
          f"| ECC sub-domains covered | {ex['subdomains_covered']} of {ex['subdomains_official']} |",
          f"| Records with inline ids (merged controls) | {ex['records_with_inline_ids_(merged_controls)']} |", "",
          "### Simulated domain -> ECC-1:2018\n", "| Simulated domain | ECC sub-domain(s) | Controls in KB |", "|---|---|---|"]
    for row in l1["domain_table"]: L.append(f"| {row['simulated_domain']} | {row['ecc_subdomain_codes']} | {row['n_controls_in_kb']} |")
    lk = l1["linking"]
    L += ["", "### Linking English test posts to controls (TF-IDF cosine; correct = ECC domain of top control equals generating domain)\n",
          "| Variant | Posts | Top-1 acc. (all) | Top-3 acc. (all) | Top-1 acc. (posts naming the domain) | Top-1 acc. (posts not naming it) |", "|---|---|---|---|---|---|"]
    for name, v in [("word TF-IDF, full KB", lk["word_tfidf"]), ("char n-gram TF-IDF, full KB", lk["char_tfidf"]),
                    ("word TF-IDF, KB restricted to the 12 domains", lk["kb_restricted_to_12_domains"]["word_tfidf"])]:
        f2 = lambda z: "-" if z is None else f"{z:.3f}"
        L.append(f"| {name} | {v['n_posts']} | {v['accuracy_top1_all']:.3f} | {v['accuracy_top3_all']:.3f} | {f2(v['accuracy_top1_posts_with_domain_name'])} | {f2(v['accuracy_top1_posts_without_domain_name'])} |")
    L += [f"\nChance level 1/12 = {1/12:.3f}.\n",
          "## Compliance Status Classifier (test set)\n", "| Model | Macro P | Macro R | Macro F1 | AUC-ROC (OvR) |", "|---|---|---|---|---|",
          f"| Keyword-rule baseline | - | - | {c['rule_baseline']['macro_f1']:.3f} | - |",
          f"| Logistic regression | {c['logreg']['macro_precision']:.3f} | {c['logreg']['macro_recall']:.3f} | {c['logreg']['macro_f1']:.3f} | {c['logreg']['auc_ovr_macro']:.3f} |",
          f"| XGBoost | {x['macro_precision']:.3f} | {x['macro_recall']:.3f} | {x['macro_f1']:.3f} | {x['auc_ovr_macro']:.3f} |",
          f"\nSplit {c['n_train']}/{c['n_val']}/{c['n_test']}. XGBoost per-class F1: " + ", ".join(f"{k} {v:.3f}" for k, v in x["per_class_f1"].items()) +
          f"; gain over rule baseline {x['f1_gain_over_rule_baseline_pp']:.1f} pp. Confusion matrix (rows = true compliant / non-compliant / neutral): {x['confusion_matrix']}.\n",
          "### 5-fold CV (Table 5.5)\n", "| Fold | Macro F1 |", "|---|---|"]
    L += [f"| {i} | {v:.3f} |" for i, v in enumerate(x["cv5_fold_macro_f1"], 1)] + [f"| Mean +/- SD | {x['cv5_macro_f1_mean']:.3f} +/- {x['cv5_macro_f1_sd']:.3f} |", "",
          "## Drift detector (CUSUM) and MTTD (test organisations)\n",
          f"CUSUM k={d['cusum_k']}, h={d['cusum_h']} (tuned on validation orgs; false-alarm limit 0.05 per series-year met on validation: {d['far_constraint_met_on_validation']}). Event recall {d['drift_detector_test']['recall']:.3f}; false alarms per series-year {d['drift_detector_test']['false_alarms_per_series_year']:.3f}; series-level FPR {d['drift_detector_test']['fpr_series_level']:.3f}; {d['n_test_events']} test events.\n",
          "| Audit cycle | Detection rate audit / pipeline | MTTD audit, all (d) | MTTD pipeline, all (d) | Reduction %, all [95% CI] | Reduction %, paired [95% CI] | Paired n |", "|---|---|---|---|---|---|---|"]
    for k, v in d["mttd_by_audit_cycle"].items():
        L.append(f"| {k} d | {v['audit_detection_rate']:.2f} / {v['pipeline_detection_rate']:.2f} | {v['mttd_audit_days_all']:.1f} | {v['mttd_pipeline_days_all']:.1f} | {v['mttd_reduction_pct_all']:.1f} [{v['reduction_ci95_pct_all'][0]:.1f}, {v['reduction_ci95_pct_all'][1]:.1f}] | {v['mttd_reduction_pct']:.1f} [{v['reduction_ci95_pct'][0]:.1f}, {v['reduction_ci95_pct'][1]:.1f}] | {v['n_paired_events']} |")
    L += ["\n### Equal-frequency detectors at a common false-alarm budget (Table 5.3b; test orgs; reduction vs 180-day audit)\n",
          "| Detector | Parameters | Recall | False alarms / series-year | MTTD, all events (d) | Reduction % [95% CI] |", "|---|---|---|---|---|---|"]
    for k in ["fixed", "ewma", "cusum"]:
        v = b[k]; L.append(f"| {v['label']} | {v['params']} | {v['recall']:.3f} | {v['false_alarms_per_series_year']:.3f} | {v['mttd_days_all']:.1f} | {v['reduction_ci95_pct'] and v['reduction_vs_180d_pct']:.1f} [{v['reduction_ci95_pct'][0]:.1f}, {v['reduction_ci95_pct'][1]:.1f}] |")
    mags = sorted({v["mag"] for v in g.values()}); sig = sorted({v["noise_sd"] for v in g.values()})
    L += ["\n### Sensitivity of CUSUM, k and h fixed (Table 5.3c): recall / MTTD (days, all events) / false alarms per series-year\n",
          "| Gap magnitude \\ noise SD | " + " | ".join(str(s) for s in sig) + " |", "|---|" + "---|" * len(sig)]
    for m_ in mags:
        L.append(f"| {m_} | " + " | ".join(f"{g[f'{m_}|{s}']['recall']:.2f} / {g[f'{m_}|{s}']['mttd_days_all']:.1f} / {g[f'{m_}|{s}']['false_alarms_per_series_year']:.3f}" for s in sig) + " |")
    L += ["\n(Onset times are known by construction. 'All events' charges an undetected event its full duration, a lower bound on its delay; 'paired' uses only events detected by both methods.)\n",
          "## Risk forecaster (test organisations)\n", "| Horizon | MAE model | MAE 7-day MA | MAE persistence | Improvement vs MA % | Improvement vs persistence % |", "|---|---|---|---|---|---|"]
    for h in [7, 14, 30]:
        v = f[f"h{h}"]; L.append(f"| {h} d | {v['mae_model']:.4f} | {v['mae_moving_avg7']:.4f} | {v['mae_persistence']:.4f} | {v['improvement_vs_moving_avg_pct']:.1f} | {v['improvement_vs_persistence_pct']:.1f} |")
    L += ["\n(Observation noise sd = 0.02 puts a floor of about 0.016 on any MAE.)\n", "## Remediation prioritiser (K=%d actions/episode)\n" % r["budget_actions_per_episode"],
          "| Policy | Mean total risk reduction | Compliance-score gain (points) |", "|---|---|---|"]
    for k in r["mean_total_risk_reduction"]:
        L.append(f"| {k} | {r['mean_total_risk_reduction'][k]:.4f} | {r['compliance_score_gain_points_mean'][k]:.2f} |")
    L.append(f"\nAgent vs fixed order: {r['agent_improvement_over_fixed_order_pct']:.1f}%; vs random: {r['agent_improvement_over_random_pct']:.1f}%; vs highest-risk-first: {r['agent_improvement_over_highest_risk_pct']:.1f}%; share of oracle: {r['agent_share_of_oracle_pct']:.1f}%; correlation of learned weights with hidden effectiveness: {r['learned_effectiveness_corr_with_truth']:.4f}.")
    return "\n".join(L)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=42); ap.add_argument("--n_tweets", type=int, default=48760)
    ap.add_argument("--n_orgs", type=int, default=200); ap.add_argument("--out", default="results")
    ap.add_argument("--controls", default="controls.csv", help="Layer-1 output (layer1_extract.py on ECC-1:2018)")
    ap.add_argument("--tweets_csv", default=None, help="optional real labelled data with columns text,label (0/1/2)")
    ap.add_argument("--quick", action="store_true")
    a = ap.parse_args()
    if a.quick: a.n_tweets, a.n_orgs = 6000, 60
    OUT = a.out; os.makedirs(OUT, exist_ok=True); rng = np.random.default_rng(a.seed); t0 = time.time()
    R = {"config": vars(a).copy(), "environment": env_info()}
    df = pd.read_csv(a.tweets_csv) if a.tweets_csv else make_tweets(a.n_tweets, rng)
    df.to_csv(os.path.join(OUT, "tweets_used.csv"), index=False)
    R["config"]["tweets_source"] = a.tweets_csv or "synthetic"

    # ---- Layer 1: knowledge base + linking
    kb = layer1_link.load_controls(a.controls)
    R["layer1"] = {"extraction": layer1_link.extraction_report(kb), "domain_table": layer1_link.domain_table(kb)}
    R["classifier"], test_idx = run_classifier(df, a.seed, a.quick, OUT); print("classifier done", round(time.time() - t0), flush=True)
    if "domain_id" in df.columns and "lang" in df.columns:
        te = df.loc[test_idx]; R["layer1"]["linking"] = layer1_link.link_report(te[te.lang == "en"], kb)
    else:
        R["layer1"]["linking"] = None
    print("layer1 linking done", round(time.time() - t0), flush=True)

    # ---- simulated audits
    true, obs, events = simulate_audits(a.n_orgs, rng); events.to_csv(os.path.join(OUT, "audit_events.csv"), index=False)
    R["audit_simulation"] = {"n_orgs": a.n_orgs, "n_events": int(len(events)), "T": 365, "sigma_obs": 0.02, "gap_threshold_tau": 0.10}
    R["drift_and_mttd"] = run_drift_mttd(obs, events, a.n_orgs, a.seed, OUT); print("drift done", round(time.time() - t0), flush=True)
    cp = {"k": R["drift_and_mttd"]["cusum_k"], "h": R["drift_and_mttd"]["cusum_h"]}
    R["detector_comparison"] = baselines_sensitivity.compare_detectors(obs, events, a.n_orgs, a.seed, cusum_params=cp)
    R["sensitivity_cusum"] = baselines_sensitivity.sensitivity_grid(a.n_orgs, a.seed, cp["k"], cp["h"])
    print("baselines + sensitivity done", round(time.time() - t0), flush=True)
    R["forecaster"] = run_forecaster(obs, a.n_orgs, a.seed, a.quick, OUT); print("forecast done", round(time.time() - t0), flush=True)
    R["remediation"] = run_remediation(true, a.n_orgs, a.seed, a.quick); print("remediation done", round(time.time() - t0), flush=True)
    R["runtime_seconds"] = round(time.time() - t0)
    json.dump(R, open(os.path.join(OUT, "results.json"), "w"), indent=2, ensure_ascii=False)
    open(os.path.join(OUT, "results_tables.md"), "w", encoding="utf8").write(md_tables(R))
    print(md_tables(R))
