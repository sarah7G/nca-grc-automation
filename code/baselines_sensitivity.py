#!/usr/bin/env python3
"""
Tables 5.3b and 5.3c of the thesis (previously NOT backed by code).

5.3b  Equal-frequency detectors: CUSUM vs fixed-threshold alert vs EWMA control chart. Every detector looks at the
      same daily observed series and the same injected gaps, and is tuned on the 30 validation organisations to
      maximise recall subject to <= 0.05 false alarms per series-year (then lowest mean delay); results on the 30 test
      organisations. Reduction vs the 180-day periodic audit uses the SAME audit delays for every detector.
5.3c  Sensitivity of CUSUM (k, h fixed at the values chosen for the main experiment) to gap magnitude and observation noise.

Standalone:  python baselines_sensitivity.py --seed 42 [--quick]      (writes results/baselines_sensitivity.json)
It is also called by run_experiment.py, which merges the output into results.json.
"""
import argparse, json, os
import numpy as np
from common import (simulate_audits, cusum_alarms, fixed_alarms, ewma_alarms, eval_alarms, audit_delays,
                    boot_reduction, split_orgs)

BUDGET = 0.05
GRIDS = {"cusum": [{"k": k, "h": h} for k in [0.5, 1.0, 1.5, 2.0] for h in [3, 4, 5, 6, 8, 10, 15, 20, 30]],
         "fixed": [{"delta": float(round(d, 3))} for d in np.arange(0.03, 0.2001, 0.01)],
         "ewma": [{"lam": l, "L": L} for l in [0.05, 0.1, 0.2, 0.3] for L in [2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]]}


def alarms(kind, obs, p):
    if kind == "cusum": return cusum_alarms(obs, p["h"], p["k"])
    if kind == "fixed": return fixed_alarms(obs, p["delta"])
    return ewma_alarms(obs, p["lam"], p["L"])


def tune(kind, obs, events, val):
    ev = events[events.org.isin(val)].copy(); ev["org"] = ev.org.map({o: i for i, o in enumerate(val)})
    best, fallback = None, None
    for p in GRIDS[kind]:
        m, e = eval_alarms(alarms(kind, obs[val], p), ev, list(range(len(val))))
        delay = float(np.nanmean(e.d_pipe)) if m["recall"] > 0 else 1e9
        cand = (p, m, delay)
        if fallback is None or m["false_alarms_per_series_year"] < fallback[1]["false_alarms_per_series_year"]: fallback = cand
        if m["false_alarms_per_series_year"] <= BUDGET and (best is None or (m["recall"], -delay) > (best[1]["recall"], -best[2])): best = cand
    chosen = best if best else fallback
    return {"params": chosen[0], "budget_met_on_validation": best is not None, "validation": chosen[1]}


def mttd_all(ev):
    dur = (ev.end - ev.onset).values.astype(float); dp = ev.d_pipe.values
    return np.where(np.isnan(dp), dur, dp)


def compare_detectors(obs, events, n_orgs, seed, cusum_params=None):
    """Table 5.3b. If cusum_params is given (k, h selected by the main experiment) they are reused so row 'CUSUM' equals Table 5.3."""
    val, test = split_orgs(n_orgs, seed); test = list(test)
    out = {}
    d_a = audit_delays(obs, events, test, 180, np.random.default_rng(seed + 180))     # identical audit delays for all detectors
    for kind, label in [("fixed", "Fixed-threshold alert"), ("ewma", "EWMA control chart"), ("cusum", "CUSUM")]:
        t = tune(kind, obs, events, val)
        if kind == "cusum" and cusum_params: t["params"] = cusum_params
        m, ev = eval_alarms(alarms(kind, obs, t["params"]), events, test)
        dp_all = mttd_all(ev); org_e = ev.org.values
        dur = (ev.end - ev.onset).values.astype(float); da_all = np.where(np.isnan(d_a), dur, d_a)
        out[kind] = {"label": label, "params": t["params"], "budget_met_on_validation": t["budget_met_on_validation"],
                     "recall": m["recall"], "false_alarms_per_series_year": m["false_alarms_per_series_year"],
                     "fpr_series_level": m["fpr_series_level"], "mttd_days_all": float(dp_all.mean()),
                     "mttd_days_detected_only": float(np.nanmean(ev.d_pipe.values)),
                     "reduction_vs_180d_pct": float(100 * (1 - dp_all.mean() / da_all.mean())),
                     "reduction_ci95_pct": boot_reduction(dp_all, da_all, org_e, seed), "n_test_events": int(len(ev))}
    return out


def sensitivity_grid(n_orgs, seed, k, h, mags=(0.05, 0.10, 0.15, 0.25, 0.40), sigmas=(0.01, 0.02, 0.04, 0.08)):
    """Table 5.3c. New simulation per cell (all n_orgs organisations, cell-specific seed); detector fixed at (k, h)."""
    cells = {}
    for i, m_ in enumerate(mags):
        for j, s_ in enumerate(sigmas):
            _, obs, ev = simulate_audits(n_orgs, np.random.default_rng(seed + 1000 + 10 * i + j), sigma_obs=s_, mag=m_)
            m, e = eval_alarms(cusum_alarms(obs, h, k), ev, list(range(n_orgs)))
            cells[f"{m_}|{s_}"] = {"mag": m_, "noise_sd": s_, "recall": m["recall"], "mttd_days_all": float(mttd_all(e).mean()),
                                   "false_alarms_per_series_year": m["false_alarms_per_series_year"], "n_events": int(len(e))}
    return cells


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("--seed", type=int, default=42); ap.add_argument("--n_orgs", type=int, default=200)
    ap.add_argument("--out", default="results"); ap.add_argument("--quick", action="store_true"); a = ap.parse_args()
    if a.quick: a.n_orgs = 60
    os.makedirs(a.out, exist_ok=True)
    # same generator call order as run_experiment.py: tweets first (consume RNG), then audits
    from common import make_tweets
    rng = np.random.default_rng(a.seed); make_tweets(6000 if a.quick else 48760, rng)
    _, obs, ev = simulate_audits(a.n_orgs, rng)
    R = {"table_5_3b": compare_detectors(obs, ev, a.n_orgs, a.seed)}
    c = R["table_5_3b"]["cusum"]["params"]; R["table_5_3c"] = sensitivity_grid(a.n_orgs, a.seed, c["k"], c["h"])
    json.dump(R, open(os.path.join(a.out, "baselines_sensitivity.json"), "w"), indent=2); print(json.dumps(R["table_5_3b"], indent=2))
