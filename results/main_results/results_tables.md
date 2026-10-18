# Results (simulated data; produced by run_experiment.py)

Seed 42; Python 3.12.3, xgboost 3.4.1, scikit-learn 1.8.0, numpy 2.4.4, pandas 3.0.2.
48760 synthetic posts, 200 simulated organisations x 12 domains x 365 days, 2268 injected gaps.

## Layer 1 - ECC-1:2018 knowledge base (controls.csv)

| Item | Value |
|---|---|
| Controls extracted (level 3) | 52 of 114 (45.6%) |
| Sub-controls extracted (level 4) | 96 of 105 (91.4%) |
| ECC sub-domains covered | 29 of 29 |
| Records with inline ids (merged controls) | 41 |

### Simulated domain -> ECC-1:2018

| Simulated domain | ECC sub-domain(s) | Controls in KB |
|---|---|---|
| governance | 1-1, 1-2, 1-3, 1-4 | 6 |
| risk management | 1-5 | 6 |
| asset management | 2-1 | 1 |
| access control | 2-2 | 6 |
| cryptography | 2-8 | 6 |
| network security | 2-5 | 10 |
| vulnerability management | 2-10 | 6 |
| logging and monitoring | 2-12 | 6 |
| incident response | 2-13 | 6 |
| business continuity | 3-1 | 5 |
| third-party security | 4-1 | 6 |
| security awareness | 1-10 | 10 |

### Linking English test posts to controls (TF-IDF cosine; correct = ECC domain of top control equals generating domain)

| Variant | Posts | Top-1 acc. (all) | Top-3 acc. (all) | Top-1 acc. (posts naming the domain) | Top-1 acc. (posts not naming it) |
|---|---|---|---|---|---|
| word TF-IDF, full KB | 3658 | 0.397 | 0.540 | 0.501 | 0.156 |
| char n-gram TF-IDF, full KB | 3658 | 0.522 | 0.645 | 0.636 | 0.256 |
| word TF-IDF, KB restricted to the 12 domains | 3658 | 0.433 | 0.598 | 0.537 | 0.189 |

Chance level 1/12 = 0.083.

## Compliance Status Classifier (test set)

| Model | Macro P | Macro R | Macro F1 | AUC-ROC (OvR) |
|---|---|---|---|---|
| Keyword-rule baseline | - | - | 0.776 | - |
| Logistic regression | 0.835 | 0.834 | 0.834 | 0.973 |
| XGBoost | 0.828 | 0.826 | 0.827 | 0.971 |

Split 34132/7314/7314. XGBoost per-class F1: compliant 0.839, non_compliant 0.838, neutral 0.803; gain over rule baseline 5.1 pp. Confusion matrix (rows = true compliant / non-compliant / neutral): [[2206, 204, 162], [218, 2147, 188], [261, 223, 1705]].

### 5-fold CV (Table 5.5)

| Fold | Macro F1 |
|---|---|
| 1 | 0.829 |
| 2 | 0.822 |
| 3 | 0.818 |
| 4 | 0.831 |
| 5 | 0.828 |
| Mean +/- SD | 0.825 +/- 0.005 |

## Drift detector (CUSUM) and MTTD (test organisations)

CUSUM k=2.0, h=20 (tuned on validation orgs; false-alarm limit 0.05 per series-year met on validation: True). Event recall 1.000; false alarms per series-year 0.047; series-level FPR 0.059; 344 test events.

| Audit cycle | Detection rate audit / pipeline | MTTD audit, all (d) | MTTD pipeline, all (d) | Reduction %, all [95% CI] | Reduction %, paired [95% CI] | Paired n |
|---|---|---|---|---|---|---|
| 90 d | 0.63 / 1.00 | 38.5 | 9.3 | 75.9 [74.1, 77.6] | 75.2 [72.4, 77.5] | 217 |
| 180 d | 0.30 / 1.00 | 48.7 | 9.3 | 81.0 [79.7, 82.2] | 76.4 [72.9, 79.1] | 104 |
| 365 d | 0.16 / 1.00 | 54.3 | 9.3 | 82.9 [82.0, 83.8] | 77.8 [72.9, 81.7] | 55 |

### Equal-frequency detectors at a common false-alarm budget (Table 5.3b; test orgs; reduction vs 180-day audit)

| Detector | Parameters | Recall | False alarms / series-year | MTTD, all events (d) | Reduction % [95% CI] |
|---|---|---|---|---|---|
| Fixed-threshold alert | {'delta': 0.12} | 1.000 | 0.044 | 6.2 | 87.3 [86.4, 88.2] |
| EWMA control chart | {'lam': 0.3, 'L': 8.0} | 1.000 | 0.117 | 6.7 | 86.3 [85.4, 87.3] |
| CUSUM | {'k': 2.0, 'h': 20} | 1.000 | 0.047 | 9.3 | 81.0 [79.7, 82.2] |

### Sensitivity of CUSUM, k and h fixed (Table 5.3c): recall / MTTD (days, all events) / false alarms per series-year

| Gap magnitude \ noise SD | 0.01 | 0.02 | 0.04 | 0.08 |
|---|---|---|---|---|
| 0.05 | 0.70 / 34.4 / 0.325 | 0.42 / 47.5 / 0.046 | 0.03 / 62.2 / 0.000 | 0.00 / 62.8 / 0.000 |
| 0.1 | 0.98 / 15.4 / 0.336 | 0.94 / 21.4 / 0.053 | 0.51 / 45.0 / 0.000 | 0.01 / 62.4 / 0.000 |
| 0.15 | 1.00 / 10.4 / 0.360 | 1.00 / 13.2 / 0.050 | 0.93 / 23.9 / 0.001 | 0.16 / 57.9 / 0.000 |
| 0.25 | 1.00 / 7.7 / 0.324 | 1.00 / 9.3 / 0.043 | 1.00 / 13.5 / 0.001 | 0.88 / 28.2 / 0.000 |
| 0.4 | 1.00 / 5.7 / 0.364 | 1.00 / 7.0 / 0.060 | 1.00 / 9.7 / 0.000 | 1.00 / 15.2 / 0.000 |

(Onset times are known by construction. 'All events' charges an undetected event its full duration, a lower bound on its delay; 'paired' uses only events detected by both methods.)

## Risk forecaster (test organisations)

| Horizon | MAE model | MAE 7-day MA | MAE persistence | Improvement vs MA % | Improvement vs persistence % |
|---|---|---|---|---|---|
| 7 d | 0.0307 | 0.0356 | 0.0357 | 13.8 | 14.0 |
| 14 d | 0.0412 | 0.0460 | 0.0465 | 10.4 | 11.4 |
| 30 d | 0.0625 | 0.0653 | 0.0665 | 4.3 | 5.9 |

(Observation noise sd = 0.02 puts a floor of about 0.016 on any MAE.)

## Remediation prioritiser (K=4 actions/episode)

| Policy | Mean total risk reduction | Compliance-score gain (points) |
|---|---|---|
| fixed_order | 0.3170 | 2.64 |
| random | 0.3739 | 3.12 |
| highest_risk | 0.6199 | 5.17 |
| agent | 0.6645 | 5.54 |
| oracle | 0.6646 | 5.54 |

Agent vs fixed order: 109.6%; vs random: 77.7%; vs highest-risk-first: 7.2%; share of oracle: 100.0%; correlation of learned weights with hidden effectiveness: 0.9998.