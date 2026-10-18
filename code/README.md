# Code

All experiments use seed 42. Every number in Chapter 5 of the thesis is produced by the scripts below.

## Environment

Python 3.12.3 with the versions pinned in `requirements.txt`
(scikit-learn 1.8.0, xgboost 3.4.1, numpy 2.4.4, pandas 3.0.2, matplotlib 3.10.8), plus `pdfplumber` for Layer 1.
Other library versions may change XGBoost and cross-validation results in the third decimal place.

```bash
python -m pip install -r requirements.txt pdfplumber
./run_all.sh     # main experiments -> results/
./run_extra.sh   # robustness analyses -> results_extra/, Layer 1 extraction -> layer1_out/
```

## Files

| File | Purpose |
|---|---|
| `common.py` | Synthetic post generator, simulated audit series, drift detectors (CUSUM, EWMA, fixed threshold), ECC structure |
| `run_experiment.py` | Main experiments: compliance-status classifier with 5-fold CV, drift detection and MTTD, risk forecaster, remediation agent |
| `baselines_sensitivity.py` | Equal-frequency detector baselines (Table 5.3b) and CUSUM sensitivity grid (Table 5.3c) |
| `extra_analysis.py` | Robustness analyses (Section 5.6): template-family and domain held-out splits, paraphrase test, bootstrap intervals, forecaster variability, reward regimes |
| `layer1_extract.py` | Rule-based extraction of controls and sub-controls from ECC-1:2018 (output: `controls.csv`) |
| `layer1_extract_coord_controls.py`, `layer1_extract_coord_subcontrols.py` | Coordinate-based PDF reader used to build the Layer 1 reference set |
| `layer1_link.py` | Uses `controls.csv` as knowledge base: extraction report, domain-to-ECC mapping, TF-IDF linking of posts to controls |
| `cybattt_pipeline.py` | Auxiliary experiment on CybAttT: cleaning, inter-annotator agreement of the published labels, classification |
| `verify_thesis.py`, `thesis_claims.json` | Compares the 170 numbers reported in the thesis with the code output (`results/reconciliation.md`) |
| `label_tweets_llm.py`, `agreement.py` | Optional annotation helpers; not used for the reported results |
| `controls.csv` | Layer 1 output: 52 controls and 96 sub-controls |

## Known limitations

- The EWMA baseline could not meet the 0.05 false-alarm budget within its parameter grid (false-alarm rate 0.117; flagged in `results.json`).
- Post-to-control linking is evaluated on English posts only.
- Layer 1 scripts require the ECC-1:2018 PDF (see the main README).
