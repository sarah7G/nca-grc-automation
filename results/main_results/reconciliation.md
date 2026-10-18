# Thesis vs code

170 MATCH, 0 DIFF/MISSING, 1 item without code.

| Thesis location | Quantity | Thesis | Code | Status |
|---|---|---|---|---|
| Table 5.1, 5.4, 5.7 | Rule baseline macro F1 | 0.776 | 0.7758 | MATCH |
| Table 5.1, 5.4, 5.7 | XGBoost macro precision | 0.828 | 0.8285 | MATCH |
| Table 5.1, 5.4, 5.7 | XGBoost macro recall | 0.826 | 0.8259 | MATCH |
| Table 5.1, 5.4, 5.7 | XGBoost macro F1 | 0.827 | 0.8268 | MATCH |
| Table 5.1, 5.4, 5.7 | XGBoost AUC-ROC | 0.971 | 0.9711 | MATCH |
| Table 5.1, 5.4, 5.7 | XGBoost gain over rule baseline (pp) | 5.1 | 5.1002 | MATCH |
| 5.4 | LogReg macro F1 | 0.834 | 0.8343 | MATCH |
| 5.4 | LogReg AUC-ROC | 0.973 | 0.9729 | MATCH |
| 5.4 | F1 compliant | 0.839 | 0.8393 | MATCH |
| 5.4 | F1 non-compliant | 0.838 | 0.8375 | MATCH |
| 5.4 | F1 neutral | 0.803 | 0.8035 | MATCH |
| 3.4.2.1, 5.2 | n_train | 34132 | 34132 | MATCH |
| 3.4.2.1, 5.2 | n_val | 7314 | 7314 | MATCH |
| 3.4.2.1, 5.2 | n_test | 7314 | 7314 | MATCH |
| 5.5.2 | neutral precision | 0.83 | 0.8297 | MATCH |
| 5.5.2 | neutral recall | 0.779 | 0.7789 | MATCH |
| 5.5.2 | non-compliant recall | 0.841 | 0.841 | MATCH |
| 5.5.2 | neutral -> compliant (count) | 261 | 261 | MATCH |
| 5.5.2 | neutral -> non-compliant (count) | 223 | 223 | MATCH |
| 5.5.2 | non-compliant -> compliant (count) | 218 | 218 | MATCH |
| 5.5.2 | non-compliant -> neutral (count) | 188 | 188 | MATCH |
| Table 5.5 | CV fold 1 | 0.829 | 0.8286 | MATCH |
| Table 5.5 | CV fold 2 | 0.822 | 0.8217 | MATCH |
| Table 5.5 | CV fold 3 | 0.818 | 0.818 | MATCH |
| Table 5.5 | CV fold 4 | 0.831 | 0.8307 | MATCH |
| Table 5.5 | CV fold 5 | 0.828 | 0.8278 | MATCH |
| Table 5.5, 5.6, 5.7 | CV mean | 0.825 | 0.8254 | MATCH |
| Table 5.5, 5.6, 5.7 | CV SD | 0.005 | 0.0047 | MATCH |
| Table 3.2, 5.2, 5.4 | CUSUM k | 2.0 | 2.0 | MATCH |
| Table 3.2, 5.2, 5.4 | CUSUM h | 20 | 20 | MATCH |
| 5.4 | recall | 1.0 | 1.0 | MATCH |
| 5.4, 5.5.1 | false alarms / series-year | 0.047 | 0.0472 | MATCH |
| 5.4, 5.5.1 | series-level FPR | 0.059 | 0.0594 | MATCH |
| 3.4.2.2 | injected gaps (200 orgs) | 2268 | 2268 | MATCH |
| 5.4 | test events (30 orgs) | 344 | 344 | MATCH |
| Table 5.3 | 90 d: audit detection rate | 0.63 | 0.6308 | MATCH |
| Table 5.3 | 90 d: MTTD audit (all) | 38.5 | 38.5145 | MATCH |
| Table 5.3 | 90 d: MTTD pipeline (all) | 9.3 | 9.2645 | MATCH |
| Table 5.3 | 90 d: reduction all % | 75.9 | 75.9454 | MATCH |
| Table 5.3 | 90 d: CI low (all) | 74.1 | 74.118 | MATCH |
| Table 5.3 | 90 d: CI high (all) | 77.6 | 77.5627 | MATCH |
| Table 5.3 | 90 d: reduction paired % | 75.2 | 75.1631 | MATCH |
| Table 5.3 | 90 d: paired CI low | 72.4 | 72.3861 | MATCH |
| Table 5.3 | 90 d: paired CI high | 77.5 | 77.4971 | MATCH |
| Table 5.3 | 180 d: audit detection rate | 0.3 | 0.3023 | MATCH |
| Table 5.3 | 180 d: MTTD audit (all) | 48.7 | 48.6977 | MATCH |
| Table 5.3 | 180 d: MTTD pipeline (all) | 9.3 | 9.2645 | MATCH |
| Table 5.3 | 180 d: reduction all % | 81.0 | 80.9754 | MATCH |
| Table 5.3 | 180 d: CI low (all) | 79.7 | 79.7049 | MATCH |
| Table 5.3 | 180 d: CI high (all) | 82.2 | 82.2472 | MATCH |
| Table 5.3 | 180 d: reduction paired % | 76.4 | 76.419 | MATCH |
| Table 5.3 | 180 d: paired CI low | 72.9 | 72.9457 | MATCH |
| Table 5.3 | 180 d: paired CI high | 79.1 | 79.1403 | MATCH |
| Table 5.3 | 365 d: audit detection rate | 0.16 | 0.1599 | MATCH |
| Table 5.3 | 365 d: MTTD audit (all) | 54.3 | 54.3169 | MATCH |
| Table 5.3 | 365 d: MTTD pipeline (all) | 9.3 | 9.2645 | MATCH |
| Table 5.3 | 365 d: reduction all % | 82.9 | 82.9435 | MATCH |
| Table 5.3 | 365 d: CI low (all) | 82.0 | 81.9815 | MATCH |
| Table 5.3 | 365 d: CI high (all) | 83.8 | 83.7869 | MATCH |
| Table 5.3 | 365 d: reduction paired % | 77.8 | 77.8067 | MATCH |
| Table 5.3 | 365 d: paired CI low | 72.9 | 72.917 | MATCH |
| Table 5.3 | 365 d: paired CI high | 81.7 | 81.6752 | MATCH |
| 5.4 | paired events (180 d) | 104 | 104 | MATCH |
| Table 5.3b | fixed: recall | 1.0 | 1.0 | MATCH |
| Table 5.3b | fixed: false alarms/series-year | 0.044 | 0.0444 | MATCH |
| Table 5.3b | fixed: MTTD (d) | 6.2 | 6.186 | MATCH |
| Table 5.3b | fixed: reduction % | 87.3 | 87.297 | MATCH |
| Table 5.3b | fixed: CI low | 86.4 | 86.3779 | MATCH |
| Table 5.3b | fixed: CI high | 88.2 | 88.1948 | MATCH |
| Table 5.3b | ewma: recall | 1.0 | 1.0 | MATCH |
| Table 5.3b | ewma: false alarms/series-year | 0.117 | 0.1167 | MATCH |
| Table 5.3b | ewma: MTTD (d) | 6.7 | 6.6657 | MATCH |
| Table 5.3b | ewma: reduction % | 86.3 | 86.3121 | MATCH |
| Table 5.3b | ewma: CI low | 85.4 | 85.3506 | MATCH |
| Table 5.3b | ewma: CI high | 87.3 | 87.2504 | MATCH |
| Table 5.3b | cusum: recall | 1.0 | 1.0 | MATCH |
| Table 5.3b | cusum: false alarms/series-year | 0.047 | 0.0472 | MATCH |
| Table 5.3b | cusum: MTTD (d) | 9.3 | 9.2645 | MATCH |
| Table 5.3b | cusum: reduction % | 81.0 | 80.9754 | MATCH |
| Table 5.3b | cusum: CI low | 79.7 | 79.7049 | MATCH |
| Table 5.3b | cusum: CI high | 82.2 | 82.2472 | MATCH |
| Table 5.3c | gap 0.05 / noise 0.01: recall | 0.7 | 0.698 | MATCH |
| Table 5.3c | gap 0.05 / noise 0.01: MTTD | 34.4 | 34.3631 | MATCH |
| Table 5.3c | gap 0.05 / noise 0.02: recall | 0.42 | 0.4224 | MATCH |
| Table 5.3c | gap 0.05 / noise 0.02: MTTD | 47.5 | 47.4676 | MATCH |
| Table 5.3c | gap 0.05 / noise 0.04: recall | 0.03 | 0.0346 | MATCH |
| Table 5.3c | gap 0.05 / noise 0.04: MTTD | 62.2 | 62.1894 | MATCH |
| Table 5.3c | gap 0.05 / noise 0.08: recall | 0.0 | 0.0 | MATCH |
| Table 5.3c | gap 0.05 / noise 0.08: MTTD | 62.8 | 62.754 | MATCH |
| Table 5.3c | gap 0.1 / noise 0.01: recall | 0.98 | 0.9845 | MATCH |
| Table 5.3c | gap 0.1 / noise 0.01: MTTD | 15.4 | 15.3947 | MATCH |
| Table 5.3c | gap 0.1 / noise 0.02: recall | 0.94 | 0.9423 | MATCH |
| Table 5.3c | gap 0.1 / noise 0.02: MTTD | 21.4 | 21.3547 | MATCH |
| Table 5.3c | gap 0.1 / noise 0.04: recall | 0.51 | 0.505 | MATCH |
| Table 5.3c | gap 0.1 / noise 0.04: MTTD | 45.0 | 44.9729 | MATCH |
| Table 5.3c | gap 0.1 / noise 0.08: recall | 0.01 | 0.0097 | MATCH |
| Table 5.3c | gap 0.1 / noise 0.08: MTTD | 62.4 | 62.4091 | MATCH |
| Table 5.3c | gap 0.15 / noise 0.01: recall | 1.0 | 0.9996 | MATCH |
| Table 5.3c | gap 0.15 / noise 0.01: MTTD | 10.4 | 10.4142 | MATCH |
| Table 5.3c | gap 0.15 / noise 0.02: recall | 1.0 | 0.9982 | MATCH |
| Table 5.3c | gap 0.15 / noise 0.02: MTTD | 13.2 | 13.1933 | MATCH |
| Table 5.3c | gap 0.15 / noise 0.04: recall | 0.93 | 0.9252 | MATCH |
| Table 5.3c | gap 0.15 / noise 0.04: MTTD | 23.9 | 23.8752 | MATCH |
| Table 5.3c | gap 0.15 / noise 0.08: recall | 0.16 | 0.1587 | MATCH |
| Table 5.3c | gap 0.15 / noise 0.08: MTTD | 57.9 | 57.9305 | MATCH |
| Table 5.3c | gap 0.25 / noise 0.01: recall | 1.0 | 1.0 | MATCH |
| Table 5.3c | gap 0.25 / noise 0.01: MTTD | 7.7 | 7.6536 | MATCH |
| Table 5.3c | gap 0.25 / noise 0.02: recall | 1.0 | 1.0 | MATCH |
| Table 5.3c | gap 0.25 / noise 0.02: MTTD | 9.3 | 9.2927 | MATCH |
| Table 5.3c | gap 0.25 / noise 0.04: recall | 1.0 | 1.0 | MATCH |
| Table 5.3c | gap 0.25 / noise 0.04: MTTD | 13.5 | 13.4768 | MATCH |
| Table 5.3c | gap 0.25 / noise 0.08: recall | 0.88 | 0.875 | MATCH |
| Table 5.3c | gap 0.25 / noise 0.08: MTTD | 28.2 | 28.1875 | MATCH |
| Table 5.3c | gap 0.4 / noise 0.01: recall | 1.0 | 1.0 | MATCH |
| Table 5.3c | gap 0.4 / noise 0.01: MTTD | 5.7 | 5.7397 | MATCH |
| Table 5.3c | gap 0.4 / noise 0.02: recall | 1.0 | 1.0 | MATCH |
| Table 5.3c | gap 0.4 / noise 0.02: MTTD | 7.0 | 6.9658 | MATCH |
| Table 5.3c | gap 0.4 / noise 0.04: recall | 1.0 | 1.0 | MATCH |
| Table 5.3c | gap 0.4 / noise 0.04: MTTD | 9.7 | 9.7301 | MATCH |
| Table 5.3c | gap 0.4 / noise 0.08: recall | 1.0 | 0.9987 | MATCH |
| Table 5.3c | gap 0.4 / noise 0.08: MTTD | 15.2 | 15.2212 | MATCH |
| 5.1, 5.4 | MAE model 7 d | 0.0307 | 0.0307 | MATCH |
| 5.1, 5.4 | MAE moving avg 7 d | 0.0356 | 0.0356 | MATCH |
| 5.4 | MAE persistence 7 d | 0.0357 | 0.0357 | MATCH |
| 5.4 | improvement vs MA 7 d (%) | 13.8 | 13.8277 | MATCH |
| 5.1, 5.4 | MAE model 14 d | 0.0412 | 0.0412 | MATCH |
| 5.1, 5.4 | MAE moving avg 14 d | 0.046 | 0.046 | MATCH |
| 5.4 | MAE persistence 14 d | 0.0465 | 0.0465 | MATCH |
| 5.4 | improvement vs MA 14 d (%) | 10.4 | 10.4049 | MATCH |
| 5.1, 5.4 | MAE model 30 d | 0.0625 | 0.0625 | MATCH |
| 5.1, 5.4 | MAE moving avg 30 d | 0.0653 | 0.0653 | MATCH |
| 5.4 | MAE persistence 30 d | 0.0665 | 0.0665 | MATCH |
| 5.4 | improvement vs MA 30 d (%) | 4.3 | 4.2715 | MATCH |
| Table 5.2 | fixed_order: risk reduction | 0.317 | 0.317 | MATCH |
| Table 5.2 | fixed_order: score gain (points) | 2.64 | 2.6418 | MATCH |
| Table 5.2 | random: risk reduction | 0.3739 | 0.3739 | MATCH |
| Table 5.2 | random: score gain (points) | 3.12 | 3.1156 | MATCH |
| Table 5.2 | highest_risk: risk reduction | 0.6199 | 0.6199 | MATCH |
| Table 5.2 | highest_risk: score gain (points) | 5.17 | 5.1659 | MATCH |
| Table 5.2 | agent: risk reduction | 0.6645 | 0.6645 | MATCH |
| Table 5.2 | agent: score gain (points) | 5.54 | 5.5375 | MATCH |
| Table 5.2 | oracle: risk reduction | 0.6646 | 0.6646 | MATCH |
| Table 5.2 | oracle: score gain (points) | 5.54 | 5.5382 | MATCH |
| 5.1, 5.4 | agent vs fixed order % | 109.6 | 109.6084 | MATCH |
| 5.4 | agent vs random % | 77.7 | 77.734 | MATCH |
| 5.1, 5.4 | agent vs highest-risk % | 7.2 | 7.1922 | MATCH |
| 5.4 | learned effectiveness correlation | 0.9998 | 0.9998 | MATCH |
| note 5 / 3.4, 5.1 | controls extracted | 52 | 52 | MATCH |
| note 5 | control recall % | 45.6 | 45.614 | MATCH |
| note 5 | sub-controls extracted | 96 | 96 | MATCH |
| Table 5.4 / 3.4.2.1 | labeled tweets with majority | 36080 | 36080 | MATCH |
| Table 5.4 / 3.4.2.1 | after cleaning and de-duplication | 31434 | 31434 | MATCH |
| Table 5.4 / 3.4.2.1 | not news | 27642 | 27642 | MATCH |
| Table 5.4 / 3.4.2.1 | normal news | 3151 | 3151 | MATCH |
| Table 5.4 / 3.4.2.1 | high-risk news | 641 | 641 | MATCH |
| Table 5.4 / 3.4.2.1 | Fleiss kappa | 0.916 | 0.9161 | MATCH |
| Table 5.4 / 3.4.2.1 | train | 22003 | 22003 | MATCH |
| Table 5.4 / 3.4.2.1 | validation | 4715 | 4715 | MATCH |
| Table 5.4 / 3.4.2.1 | test | 4716 | 4716 | MATCH |
| Table 5.4 / 3.4.2.1 | majority baseline F1 | 0.312 | 0.3119 | MATCH |
| Table 5.4 / 3.4.2.1 | XGBoost macro F1 | 0.852 | 0.8524 | MATCH |
| Table 5.4 / 3.4.2.1 | XGBoost AUC | 0.987 | 0.9867 | MATCH |
| Table 5.4 / 3.4.2.1 | LogReg macro F1 | 0.865 | 0.8653 | MATCH |
| Table 5.4 / 3.4.2.1 | LogReg AUC | 0.988 | 0.9883 | MATCH |
| Table 5.4 / 3.4.2.1 | XGBoost F1 high-risk | 0.759 | 0.759 | MATCH |
| Table 5.4 / 3.4.2.1 | XGBoost F1 normal | 0.816 | 0.8158 | MATCH |
| Table 5.4 / 3.4.2.1 | XGBoost F1 not news | 0.982 | 0.9822 | MATCH |
| Table 5.4 / 3.4.2.1 | CV mean | 0.845 | 0.8449 | MATCH |
| Table 5.4 / 3.4.2.1 | CV SD | 0.014 | 0.0137 | MATCH |
| Table 5.4 / 3.4.2.1 | high-risk recall | 0.656 | 0.6562 | MATCH |

## Key numbers printed in the thesis text
| String | Found |
|---|---|
| 0.827 | yes |
| 0.971 | yes |
| 0.825 ± 0.005 | yes |
| 0.834 | yes |
| 0.0412 | yes |
| 0.0625 | yes |
| 109.6 | yes |
| 81.0 | yes |
| 48.7 | yes |
| 9.3 | yes |
| 0.047 | yes |
| 0.852 | yes |
| 0.987 | yes |
| 0.845 ± 0.014 | yes |
| 52 of 114 | yes |
| 96 of 105 | yes |
| 31,434 | yes |
| 27,642 | yes |
| 0.916 | yes |
| 6.2 days | yes |
| 6.7 days | yes |

## Not reproducible by this package
| Thesis location | Item | Reason |
|---|---|---|
| Note 5 (Layer 1) | precision 100% of the extracted control identifiers | needs the source PDF or a hand-annotated gold file; the counts 52/114 and 96/105 are reproduced from controls.csv |