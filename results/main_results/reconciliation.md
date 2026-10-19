# Thesis vs code

279 MATCH, 0 DIFF/MISSING, 1 item without code.

Files read: results = results/main_results/results.json; extra = results/extra_robustness/extra_results.json; cybattt = results/cybattt/cybattt_results.json; layer1_text_eval = layer1_ecc/layer1_text_eval.json; linking_comparison = layer1_ecc/linking_comparison.json

| Thesis location | Quantity | Thesis | Code | Status |
|---|---|---|---|---|
| Table 5.1; Section 5.4 | Rule baseline macro F1 | 0.776 | 0.7758 | MATCH |
| Table 5.1; Section 5.4 | XGBoost macro precision | 0.828 | 0.8285 | MATCH |
| Table 5.1; Section 5.4 | XGBoost macro recall | 0.826 | 0.8259 | MATCH |
| Table 5.1; Section 5.4 | XGBoost macro F1 | 0.827 | 0.8268 | MATCH |
| Table 5.1; Section 5.4 | XGBoost AUC-ROC | 0.971 | 0.9711 | MATCH |
| Table 5.1; Section 5.4 | XGBoost gain over rule baseline (pp) | 5.1 | 5.1002 | MATCH |
| Section 5.4 | LogReg macro F1 | 0.834 | 0.8343 | MATCH |
| Section 5.4 | LogReg AUC-ROC | 0.973 | 0.9729 | MATCH |
| Section 5.4 | F1 compliant | 0.839 | 0.8393 | MATCH |
| Section 5.4 | F1 non-compliant | 0.838 | 0.8375 | MATCH |
| Section 5.4 | F1 neutral | 0.803 | 0.8035 | MATCH |
| Sections 3.4.2.1, 5.2 | n_train | 34132 | 34132 | MATCH |
| Sections 3.4.2.1, 5.2 | n_val | 7314 | 7314 | MATCH |
| Sections 3.4.2.1, 5.2 | n_test | 7314 | 7314 | MATCH |
| Section 5.5.2 | neutral precision | 0.83 | 0.8297 | MATCH |
| Section 5.5.2 | neutral recall | 0.779 | 0.7789 | MATCH |
| Section 5.5.2 | non-compliant recall | 0.841 | 0.841 | MATCH |
| Section 5.5.2 | neutral -> compliant (count) | 261 | 261 | MATCH |
| Section 5.5.2 | neutral -> non-compliant (count) | 223 | 223 | MATCH |
| Section 5.5.2 | non-compliant -> compliant (count) | 218 | 218 | MATCH |
| Section 5.5.2 | non-compliant -> neutral (count) | 188 | 188 | MATCH |
| Table 5.8 | CV fold 1 | 0.829 | 0.8286 | MATCH |
| Table 5.8 | CV fold 2 | 0.822 | 0.8217 | MATCH |
| Table 5.8 | CV fold 3 | 0.818 | 0.818 | MATCH |
| Table 5.8 | CV fold 4 | 0.831 | 0.8307 | MATCH |
| Table 5.8 | CV fold 5 | 0.828 | 0.8278 | MATCH |
| Table 5.8; Section 5.6 | CV mean | 0.825 | 0.8254 | MATCH |
| Table 5.8; Section 5.6 | CV SD | 0.005 | 0.0047 | MATCH |
| Tables 3.2, 4.2; Section 5.4 | CUSUM k | 2.0 | 2.0 | MATCH |
| Tables 3.2, 4.2; Section 5.4 | CUSUM h | 20 | 20 | MATCH |
| Section 5.4 | recall | 1.0 | 1.0 | MATCH |
| Table 5.1; Sections 5.4, 5.5.1 | false alarms / series-year | 0.047 | 0.0472 | MATCH |
| Table 5.1; Sections 5.4, 5.5.1 | series-level FPR | 0.059 | 0.0594 | MATCH |
| Section 3.4.2.2 | injected gaps (200 orgs) | 2268 | 2268 | MATCH |
| Section 5.4 | test events (30 orgs) | 344 | 344 | MATCH |
| Table 5.6 | 90 d: audit detection rate | 0.63 | 0.6308 | MATCH |
| Table 5.6 | 90 d: MTTD audit (all) | 38.5 | 38.5145 | MATCH |
| Table 5.6 | 90 d: MTTD pipeline (all) | 9.3 | 9.2645 | MATCH |
| Table 5.6 | 90 d: reduction all % | 75.9 | 75.9454 | MATCH |
| Table 5.6 | 90 d: CI low (all) | 74.1 | 74.118 | MATCH |
| Table 5.6 | 90 d: CI high (all) | 77.6 | 77.5627 | MATCH |
| Table 5.6 | 90 d: reduction paired % | 75.2 | 75.1631 | MATCH |
| Table 5.6 | 90 d: paired CI low | 72.4 | 72.3861 | MATCH |
| Table 5.6 | 90 d: paired CI high | 77.5 | 77.4971 | MATCH |
| Table 5.6 | 180 d: audit detection rate | 0.3 | 0.3023 | MATCH |
| Table 5.6 | 180 d: MTTD audit (all) | 48.7 | 48.6977 | MATCH |
| Table 5.6 | 180 d: MTTD pipeline (all) | 9.3 | 9.2645 | MATCH |
| Table 5.6 | 180 d: reduction all % | 81.0 | 80.9754 | MATCH |
| Table 5.6 | 180 d: CI low (all) | 79.7 | 79.7049 | MATCH |
| Table 5.6 | 180 d: CI high (all) | 82.2 | 82.2472 | MATCH |
| Table 5.6 | 180 d: reduction paired % | 76.4 | 76.419 | MATCH |
| Table 5.6 | 180 d: paired CI low | 72.9 | 72.9457 | MATCH |
| Table 5.6 | 180 d: paired CI high | 79.1 | 79.1403 | MATCH |
| Table 5.6 | 365 d: audit detection rate | 0.16 | 0.1599 | MATCH |
| Table 5.6 | 365 d: MTTD audit (all) | 54.3 | 54.3169 | MATCH |
| Table 5.6 | 365 d: MTTD pipeline (all) | 9.3 | 9.2645 | MATCH |
| Table 5.6 | 365 d: reduction all % | 82.9 | 82.9435 | MATCH |
| Table 5.6 | 365 d: CI low (all) | 82.0 | 81.9815 | MATCH |
| Table 5.6 | 365 d: CI high (all) | 83.8 | 83.7869 | MATCH |
| Table 5.6 | 365 d: reduction paired % | 77.8 | 77.8067 | MATCH |
| Table 5.6 | 365 d: paired CI low | 72.9 | 72.917 | MATCH |
| Table 5.6 | 365 d: paired CI high | 81.7 | 81.6752 | MATCH |
| Section 5.4 | paired events (180 d) | 104 | 104 | MATCH |
| Table 5.4 | fixed: recall | 1.0 | 1.0 | MATCH |
| Table 5.4 | fixed: false alarms/series-year | 0.044 | 0.0444 | MATCH |
| Table 5.4 | fixed: MTTD (d) | 6.2 | 6.186 | MATCH |
| Table 5.4 | fixed: reduction % | 87.3 | 87.297 | MATCH |
| Table 5.4 | fixed: CI low | 86.4 | 86.3779 | MATCH |
| Table 5.4 | fixed: CI high | 88.2 | 88.1948 | MATCH |
| Table 5.4 | ewma: recall | 1.0 | 1.0 | MATCH |
| Table 5.4 | ewma: false alarms/series-year | 0.117 | 0.1167 | MATCH |
| Table 5.4 | ewma: MTTD (d) | 6.7 | 6.6657 | MATCH |
| Table 5.4 | ewma: reduction % | 86.3 | 86.3121 | MATCH |
| Table 5.4 | ewma: CI low | 85.4 | 85.3506 | MATCH |
| Table 5.4 | ewma: CI high | 87.3 | 87.2504 | MATCH |
| Table 5.4 | cusum: recall | 1.0 | 1.0 | MATCH |
| Table 5.4 | cusum: false alarms/series-year | 0.047 | 0.0472 | MATCH |
| Table 5.4 | cusum: MTTD (d) | 9.3 | 9.2645 | MATCH |
| Table 5.4 | cusum: reduction % | 81.0 | 80.9754 | MATCH |
| Table 5.4 | cusum: CI low | 79.7 | 79.7049 | MATCH |
| Table 5.4 | cusum: CI high | 82.2 | 82.2472 | MATCH |
| Table 5.5 | gap 0.05 / noise 0.01: recall | 0.7 | 0.698 | MATCH |
| Table 5.5 | gap 0.05 / noise 0.01: MTTD | 34.4 | 34.3631 | MATCH |
| Table 5.5 | gap 0.05 / noise 0.02: recall | 0.42 | 0.4224 | MATCH |
| Table 5.5 | gap 0.05 / noise 0.02: MTTD | 47.5 | 47.4676 | MATCH |
| Table 5.5 | gap 0.05 / noise 0.04: recall | 0.03 | 0.0346 | MATCH |
| Table 5.5 | gap 0.05 / noise 0.04: MTTD | 62.2 | 62.1894 | MATCH |
| Table 5.5 | gap 0.05 / noise 0.08: recall | 0.0 | 0.0 | MATCH |
| Table 5.5 | gap 0.05 / noise 0.08: MTTD | 62.8 | 62.754 | MATCH |
| Table 5.5 | gap 0.1 / noise 0.01: recall | 0.98 | 0.9845 | MATCH |
| Table 5.5 | gap 0.1 / noise 0.01: MTTD | 15.4 | 15.3947 | MATCH |
| Table 5.5 | gap 0.1 / noise 0.02: recall | 0.94 | 0.9423 | MATCH |
| Table 5.5 | gap 0.1 / noise 0.02: MTTD | 21.4 | 21.3547 | MATCH |
| Table 5.5 | gap 0.1 / noise 0.04: recall | 0.51 | 0.505 | MATCH |
| Table 5.5 | gap 0.1 / noise 0.04: MTTD | 45.0 | 44.9729 | MATCH |
| Table 5.5 | gap 0.1 / noise 0.08: recall | 0.01 | 0.0097 | MATCH |
| Table 5.5 | gap 0.1 / noise 0.08: MTTD | 62.4 | 62.4091 | MATCH |
| Table 5.5 | gap 0.15 / noise 0.01: recall | 1.0 | 0.9996 | MATCH |
| Table 5.5 | gap 0.15 / noise 0.01: MTTD | 10.4 | 10.4142 | MATCH |
| Table 5.5 | gap 0.15 / noise 0.02: recall | 1.0 | 0.9982 | MATCH |
| Table 5.5 | gap 0.15 / noise 0.02: MTTD | 13.2 | 13.1933 | MATCH |
| Table 5.5 | gap 0.15 / noise 0.04: recall | 0.93 | 0.9252 | MATCH |
| Table 5.5 | gap 0.15 / noise 0.04: MTTD | 23.9 | 23.8752 | MATCH |
| Table 5.5 | gap 0.15 / noise 0.08: recall | 0.16 | 0.1587 | MATCH |
| Table 5.5 | gap 0.15 / noise 0.08: MTTD | 57.9 | 57.9305 | MATCH |
| Table 5.5 | gap 0.25 / noise 0.01: recall | 1.0 | 1.0 | MATCH |
| Table 5.5 | gap 0.25 / noise 0.01: MTTD | 7.7 | 7.6536 | MATCH |
| Table 5.5 | gap 0.25 / noise 0.02: recall | 1.0 | 1.0 | MATCH |
| Table 5.5 | gap 0.25 / noise 0.02: MTTD | 9.3 | 9.2927 | MATCH |
| Table 5.5 | gap 0.25 / noise 0.04: recall | 1.0 | 1.0 | MATCH |
| Table 5.5 | gap 0.25 / noise 0.04: MTTD | 13.5 | 13.4768 | MATCH |
| Table 5.5 | gap 0.25 / noise 0.08: recall | 0.88 | 0.875 | MATCH |
| Table 5.5 | gap 0.25 / noise 0.08: MTTD | 28.2 | 28.1875 | MATCH |
| Table 5.5 | gap 0.4 / noise 0.01: recall | 1.0 | 1.0 | MATCH |
| Table 5.5 | gap 0.4 / noise 0.01: MTTD | 5.7 | 5.7397 | MATCH |
| Table 5.5 | gap 0.4 / noise 0.02: recall | 1.0 | 1.0 | MATCH |
| Table 5.5 | gap 0.4 / noise 0.02: MTTD | 7.0 | 6.9658 | MATCH |
| Table 5.5 | gap 0.4 / noise 0.04: recall | 1.0 | 1.0 | MATCH |
| Table 5.5 | gap 0.4 / noise 0.04: MTTD | 9.7 | 9.7301 | MATCH |
| Table 5.5 | gap 0.4 / noise 0.08: recall | 1.0 | 0.9987 | MATCH |
| Table 5.5 | gap 0.4 / noise 0.08: MTTD | 15.2 | 15.2212 | MATCH |
| Table 5.1; Section 5.4 | MAE model 7 d | 0.0307 | 0.0307 | MATCH |
| Table 5.1; Section 5.4 | MAE moving avg 7 d | 0.0356 | 0.0356 | MATCH |
| Section 5.4 | MAE persistence 7 d | 0.0357 | 0.0357 | MATCH |
| Section 5.4 | improvement vs MA 7 d (%) | 13.8 | 13.8277 | MATCH |
| Table 5.1; Section 5.4 | MAE model 14 d | 0.0412 | 0.0412 | MATCH |
| Table 5.1; Section 5.4 | MAE moving avg 14 d | 0.046 | 0.046 | MATCH |
| Section 5.4 | MAE persistence 14 d | 0.0465 | 0.0465 | MATCH |
| Section 5.4 | improvement vs MA 14 d (%) | 10.4 | 10.4049 | MATCH |
| Table 5.1; Section 5.4 | MAE model 30 d | 0.0625 | 0.0625 | MATCH |
| Table 5.1; Section 5.4 | MAE moving avg 30 d | 0.0653 | 0.0653 | MATCH |
| Section 5.4 | MAE persistence 30 d | 0.0665 | 0.0665 | MATCH |
| Section 5.4 | improvement vs MA 30 d (%) | 4.3 | 4.2715 | MATCH |
| Table 5.3 | fixed_order: risk reduction | 0.317 | 0.317 | MATCH |
| Table 5.3 | fixed_order: score gain (points) | 2.64 | 2.6418 | MATCH |
| Table 5.3 | random: risk reduction | 0.3739 | 0.3739 | MATCH |
| Table 5.3 | random: score gain (points) | 3.12 | 3.1156 | MATCH |
| Table 5.3 | highest_risk: risk reduction | 0.6199 | 0.6199 | MATCH |
| Table 5.3 | highest_risk: score gain (points) | 5.17 | 5.1659 | MATCH |
| Table 5.3 | agent: risk reduction | 0.6645 | 0.6645 | MATCH |
| Table 5.3 | agent: score gain (points) | 5.54 | 5.5375 | MATCH |
| Table 5.3 | oracle: risk reduction | 0.6646 | 0.6646 | MATCH |
| Table 5.3 | oracle: score gain (points) | 5.54 | 5.5382 | MATCH |
| Table 5.1; Section 5.4 | agent vs fixed order % | 109.6 | 109.6084 | MATCH |
| Section 5.4 | agent vs random % | 77.7 | 77.734 | MATCH |
| Table 5.1; Section 5.4 | agent vs highest-risk % | 7.2 | 7.1922 | MATCH |
| Section 5.4 | learned effectiveness correlation | 0.9998 | 0.9998 | MATCH |
| Table 5.1; Section 3.3.1.1 | controls extracted | 52 | 52 | MATCH |
| Table 5.1; Section 3.3.1.1 | control recall % | 45.6 | 45.614 | MATCH |
| Table 5.1; Section 3.3.1.1 | sub-controls extracted | 96 | 96 | MATCH |
| Table 5.7; Section 3.4.2.1 | labeled tweets before removing no-majority | 36080 | 36080 | MATCH |
| Table 5.7; Section 3.4.2.1 | after cleaning and de-duplication | 31434 | 31434 | MATCH |
| Table 5.7; Section 3.4.2.1 | not news | 27642 | 27642 | MATCH |
| Table 5.7; Section 3.4.2.1 | normal news | 3151 | 3151 | MATCH |
| Table 5.7; Section 3.4.2.1 | high-risk news | 641 | 641 | MATCH |
| Table 5.7; Section 3.4.2.1 | Fleiss kappa | 0.916 | 0.9161 | MATCH |
| Table 5.7; Section 3.4.2.1 | train | 22003 | 22003 | MATCH |
| Table 5.7; Section 3.4.2.1 | validation | 4715 | 4715 | MATCH |
| Table 5.7; Section 3.4.2.1 | test | 4716 | 4716 | MATCH |
| Table 5.7; Section 3.4.2.1 | majority baseline F1 | 0.312 | 0.3119 | MATCH |
| Table 5.7; Section 3.4.2.1 | XGBoost macro F1 | 0.852 | 0.8524 | MATCH |
| Table 5.7; Section 3.4.2.1 | XGBoost AUC | 0.987 | 0.9867 | MATCH |
| Table 5.7; Section 3.4.2.1 | LogReg macro F1 | 0.865 | 0.8653 | MATCH |
| Table 5.7; Section 3.4.2.1 | LogReg AUC | 0.988 | 0.9883 | MATCH |
| Table 5.7; Section 3.4.2.1 | XGBoost F1 high-risk | 0.759 | 0.759 | MATCH |
| Table 5.7; Section 3.4.2.1 | XGBoost F1 normal | 0.816 | 0.8158 | MATCH |
| Table 5.7; Section 3.4.2.1 | XGBoost F1 not news | 0.982 | 0.9822 | MATCH |
| Table 5.7; Section 3.4.2.1 | CV mean | 0.845 | 0.8449 | MATCH |
| Table 5.7; Section 3.4.2.1 | CV SD | 0.014 | 0.0137 | MATCH |
| Table 5.7; Section 3.4.2.1 | high-risk recall | 0.656 | 0.6562 | MATCH |
| Section 3.4.2.1 | tweets without majority (removed) | 9 | 9 | MATCH |
| Sections 5.3, 5.4 | linking: word top-1 | 0.397 | 0.3969 | MATCH |
| Sections 5.3, 5.4 | linking: word top-3 | 0.54 | 0.5399 | MATCH |
| Sections 5.3, 5.4 | linking: char top-1 | 0.522 | 0.5216 | MATCH |
| Sections 5.3, 5.4 | linking: char top-3 | 0.645 | 0.6452 | MATCH |
| Sections 5.3, 5.4 | linking: word top-1 with domain name | 0.501 | 0.5006 | MATCH |
| Sections 5.3, 5.4 | linking: char top-1 with domain name | 0.636 | 0.6358 | MATCH |
| Sections 5.3, 5.4 | linking: word top-1 without domain name | 0.156 | 0.1556 | MATCH |
| Sections 5.3, 5.4 | linking: char top-1 without domain name | 0.256 | 0.2557 | MATCH |
| Sections 5.3, 5.4 | linking: English test posts | 3658 | 3658 | MATCH |
| Table 5.2 | domain 1: controls in knowledge base | 6 | 6 | MATCH |
| Table 5.2 | domain 2: controls in knowledge base | 6 | 6 | MATCH |
| Table 5.2 | domain 3: controls in knowledge base | 1 | 1 | MATCH |
| Table 5.2 | domain 4: controls in knowledge base | 6 | 6 | MATCH |
| Table 5.2 | domain 5: controls in knowledge base | 6 | 6 | MATCH |
| Table 5.2 | domain 6: controls in knowledge base | 10 | 10 | MATCH |
| Table 5.2 | domain 7: controls in knowledge base | 6 | 6 | MATCH |
| Table 5.2 | domain 8: controls in knowledge base | 6 | 6 | MATCH |
| Table 5.2 | domain 9: controls in knowledge base | 6 | 6 | MATCH |
| Table 5.2 | domain 10: controls in knowledge base | 5 | 5 | MATCH |
| Table 5.2 | domain 11: controls in knowledge base | 6 | 6 | MATCH |
| Table 5.2 | domain 12: controls in knowledge base | 10 | 10 | MATCH |
| Section 5.4 | records in controls.csv | 148 | 148 | MATCH |
| Section 5.4 | merged-control records | 41 | 41 | MATCH |
| Section 5.4 | page-header domain records | 101 | 101 | MATCH |
| Section 5.3 | sub-control recall % | 91.4 | 91.4286 | MATCH |
| Section 5.6 | standard split replica XGBoost | 0.8268 | 0.8268 | MATCH |
| Section 5.6 | standard split replica LogReg | 0.8343 | 0.8343 | MATCH |
| Section 5.6 | overlap: exact text in train | 0.235 | 0.2354 | MATCH |
| Section 5.6 | overlap: same generating signature | 0.998 | 0.9978 | MATCH |
| Section 5.6 | overlap: same template family | 1.0 | 1.0 | MATCH |
| Section 5.6 | template families | 24 | 24 | MATCH |
| Abstract; Sections 5.6, 6.5 | template-family holdout XGBoost mean | 0.357 | 0.3572 | MATCH |
| Abstract; Sections 5.6, 6.5 | template-family holdout XGBoost sd | 0.149 | 0.1487 | MATCH |
| Abstract; Sections 5.6, 6.5 | template-family holdout LogReg mean | 0.287 | 0.2874 | MATCH |
| Abstract; Sections 5.6, 6.5 | template-family holdout LogReg sd | 0.03 | 0.0297 | MATCH |
| Section 5.6 | template-family holdout XGBoost fold 1 | 0.232 | 0.2318 | MATCH |
| Section 5.6 | template-family holdout XGBoost fold 2 | 0.299 | 0.2994 | MATCH |
| Section 5.6 | template-family holdout XGBoost fold 3 | 0.287 | 0.2866 | MATCH |
| Section 5.6 | template-family holdout XGBoost fold 4 | 0.611 | 0.6109 | MATCH |
| Section 5.6 | template-family holdout LogReg fold 1 | 0.317 | 0.3174 | MATCH |
| Section 5.6 | template-family holdout LogReg fold 2 | 0.269 | 0.2694 | MATCH |
| Section 5.6 | template-family holdout LogReg fold 3 | 0.248 | 0.248 | MATCH |
| Section 5.6 | template-family holdout LogReg fold 4 | 0.315 | 0.3148 | MATCH |
| Section 5.6 | domain holdout xgboost mean | 0.827 | 0.8267 | MATCH |
| Section 5.6 | domain holdout xgboost sd | 0.002 | 0.0022 | MATCH |
| Section 5.6 | domain holdout logreg mean | 0.828 | 0.8281 | MATCH |
| Section 5.6 | domain holdout logreg sd | 0.004 | 0.0039 | MATCH |
| Section 5.6 | paraphrase posts | 360 | 360 | MATCH |
| Abstract; Section 5.6 | paraphrase XGBoost | 0.602 | 0.6017 | MATCH |
| Abstract; Section 5.6 | paraphrase LogReg | 0.719 | 0.7191 | MATCH |
| Section 5.6 | paraphrase xgboost en | 0.661 | 0.6611 | MATCH |
| Section 5.6 | paraphrase xgboost ar | 0.547 | 0.5472 | MATCH |
| Section 5.6 | paraphrase logreg en | 0.727 | 0.7267 | MATCH |
| Section 5.6 | paraphrase logreg ar | 0.709 | 0.7093 | MATCH |
| Section 5.6 | bootstrap xgboost_ci95.0 | 0.818 | 0.818 | MATCH |
| Section 5.6 | bootstrap xgboost_ci95.1 | 0.835 | 0.8354 | MATCH |
| Section 5.6 | bootstrap logreg_ci95.0 | 0.826 | 0.8256 | MATCH |
| Section 5.6 | bootstrap logreg_ci95.1 | 0.843 | 0.8434 | MATCH |
| Sections 5.3, 5.6 | bootstrap diff LR-XGB low | -0.0003 | -0.0003 | MATCH |
| Sections 5.3, 5.6 | bootstrap diff LR-XGB high | 0.0146 | 0.0146 | MATCH |
| Section 5.6 | forecaster h7 MAE SD over organizations | 0.0015 | 0.0015 | MATCH |
| Section 5.6 | forecaster h7 gain CI low | 12.9 | 12.8778 | MATCH |
| Section 5.6 | forecaster h7 gain CI high | 14.7 | 14.7444 | MATCH |
| Section 5.6 | forecaster h14 MAE SD over organizations | 0.0033 | 0.0033 | MATCH |
| Section 5.6 | forecaster h14 gain CI low | 9.2 | 9.1729 | MATCH |
| Section 5.6 | forecaster h14 gain CI high | 11.5 | 11.4642 | MATCH |
| Section 5.6 | forecaster h30 MAE SD over organizations | 0.007 | 0.007 | MATCH |
| Section 5.6 | forecaster h30 gain CI low | 2.5 | 2.4678 | MATCH |
| Section 5.6 | forecaster h30 gain CI high | 6.0 | 6.0354 | MATCH |
| Section 5.6 | share of organizations beating MA at 30 d (23 of 30) | 0.767 | 0.7667 | MATCH |
| Section 5.6 | share of organizations beating MA at 7 d | 1.0 | 1.0 | MATCH |
| Sections 5.6, 6.5 | remediation linear: gain vs highest-risk % | 7.2 | 7.1922 | MATCH |
| Section 5.6 | remediation linear: CI low | 6.9 | 6.9464 | MATCH |
| Section 5.6 | remediation linear: CI high | 7.4 | 7.4368 | MATCH |
| Sections 5.6, 6.5 | remediation concave: gain vs highest-risk % | 15.7 | 15.6903 | MATCH |
| Section 5.6 | remediation concave: CI low | 15.3 | 15.3 | MATCH |
| Section 5.6 | remediation concave: CI high | 16.1 | 16.0646 | MATCH |
| Sections 5.6, 6.5 | remediation threshold: gain vs highest-risk % | -0.1 | -0.1097 | MATCH |
| Section 5.6 | remediation threshold: CI low | -0.3 | -0.3324 | MATCH |
| Section 5.6 | remediation threshold: CI high | 0.1 | 0.1395 | MATCH |
| Section 5.6 | agent share of oracle % | 99.99 | 99.9873 | MATCH |
| Section 4.3 | traced record: alarm day | 324 | 324 | MATCH |
| Section 4.3 | traced record: onset day | 316 | 316 | MATCH |
| Section 4.3 | traced record: link similarity | 0.215 | 0.2147 | MATCH |
| Section 4.3 | traced record: P(non-compliant) | 0.993 | 0.9933 | MATCH |
| Section 4.3 | traced record: observed risk | 0.357 | 0.3571 | MATCH |
| Section 4.3 | traced record: forecast 7 d | 0.438 | 0.438 | MATCH |
| Section 4.3 | traced record: forecast 30 d | 0.364 | 0.3645 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | controls TP | 52 | 52 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | controls FP | 0 | 0 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | controls FN | 62 | 62 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | controls identifier precision | 1.0 | 1.0 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | controls identifier recall | 0.456 | 0.4561 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | controls mean token F1 | 0.62 | 0.6161 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | controls exact text matches | 11 | 11 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | sub-controls TP | 96 | 96 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | sub-controls FP | 0 | 0 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | sub-controls FN | 9 | 9 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | sub-controls identifier precision | 1.0 | 1.0 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | sub-controls identifier recall | 0.914 | 0.9143 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | sub-controls mean token F1 | 0.9 | 0.8999 | MATCH |
| Sections 3.3.1.1, 5.6; Appendix D | sub-controls exact text matches | 64 | 64 | MATCH |
| Section 3.3.1.1; Appendix D | sub-controls with token F1 >= 0.90 | 76 | 76 | MATCH |
| Section 5.3; Appendix D | coordinate KB records | 219 | 219 | MATCH |
| Section 5.3; Appendix D | coordinate KB word top-1 | 0.406 | 0.4062 | MATCH |
| Section 5.3; Appendix D | coordinate KB char top-1 | 0.493 | 0.4934 | MATCH |
| Section 5.3; Appendix D | coordinate KB char top-1 without name | 0.222 | 0.222 | MATCH |
| Section 5.3; Appendix D | baseline KB char top-1 | 0.522 | 0.5216 | MATCH |

## Key numbers printed in the thesis text
| String | Found |
|---|---|
| 0.36 | yes |
| 0.29 | yes |
| 0.60 | yes |
| 0.72 | yes |
| 5.9% | yes |
| 7.2% | yes |
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
| Section 3.3.1.1; Appendix D | manual spot-check of 12 records of the Layer 1 reference set against the PDF | manual check; the reference set itself is produced by layer1_extract_coord_*.py and evaluated by layer1_evaluate.py |