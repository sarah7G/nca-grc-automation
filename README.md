# A Machine Learning-Based Framework for Predictive and Continuous Cybersecurity GRC Automation

Code, generated data and results for the MSc thesis of **Sara G. Al-Ruwaili**,
Department of Computer Science, College of Science, Northern Border University (Arar, Saudi Arabia).
Supervisor: Dr. Randa S. S. Allafi.

The repository reproduces every result reported in Chapter 5 of the thesis, including the additional robustness
tests of Section 5.6: a compliance-status text classifier, CUSUM drift detection on simulated audit series,
equal-frequency detector baselines and a sensitivity grid, compliance-risk forecasting, remediation prioritisation,
robustness analyses (template-family holdout, domain holdout, paraphrase test, bootstrap intervals, forecaster
variability, reward regimes), an auxiliary experiment on real tweets (CybAttT), and a rule-based extraction of
NCA ECC-1:2018 (Layer 1) with its evaluation against a reference set built from the PDF.

Release used in the thesis: **v1.1** (see `CHANGELOG.md`).

## Contents

| Folder | Description |
|---|---|
| `code/` | All experiment code, run scripts, pinned requirements and the thesis-vs-code check (see `code/README.md`) |
| `results/main_results/` | Outputs of `run_experiment.py`: `results.json` (configuration, library versions and all main results), tables, figures, generated post corpus (`tweets_used.csv`), simulated audit events (`audit_events.csv`), and `reconciliation.md` (every Chapter 5 number compared with the code output) |
| `results/extra_robustness/` | `extra_results.json` from `extra_analysis.py`: robustness tests of Section 5.6 and the traced record of Section 4.3 |
| `results/cybattt/` | Auxiliary experiment on the public CybAttT tweet dataset (`cybattt_pipeline.py`) |
| `layer1_ecc/` | Layer 1: reference set built from the ECC PDF (`layer1_reference_from_pdf.json`, `controls_coord.csv`), extraction evaluation (`layer1_text_eval.json`) and linking comparison (`linking_comparison.json`), both produced by `layer1_evaluate.py` |
| `figures/` | Architecture figure (Figure 4.1) |

## Where each result of the thesis comes from

| Result (thesis location) | Script (`code/`) | Output file |
|---|---|---|
| Classifier, baselines, per-class scores, confusion matrix, 5-fold CV (Tables 5.1, 5.8; Figure 5.1; Sections 5.3–5.5) | `run_experiment.py` | `results/main_results/results.json` (`classifier`), `fig_confusion.png` |
| CUSUM drift detector and MTTD versus periodic audits (Tables 5.1, 5.6; Figure 5.3) | `run_experiment.py` | `results.json` (`drift_and_mttd`), `fig_mttd.png` |
| Equal-frequency baselines and sensitivity grid (Tables 5.4, 5.5; Appendix E) | `baselines_sensitivity.py` (called by `run_experiment.py`) | `results.json` (`detector_comparison`, `sensitivity_cusum`) |
| Risk forecaster (Table 5.1; Figure 5.2) | `run_experiment.py` | `results.json` (`forecaster`), `fig_forecast.png` |
| Remediation prioritisation (Tables 5.1, 5.3) | `run_experiment.py` | `results.json` (`remediation`) |
| Layer 1 extraction, domain table, post-to-control linking (Tables 5.1, 5.2; Section 5.4) | `layer1_extract.py`, `layer1_link.py` | `code/controls.csv`, `results.json` (`layer1`) |
| Layer 1 identifier precision/recall, text fidelity, coordinate-based linking (Sections 3.3.1.1, 5.6; Appendix D) | `layer1_extract_coord_*.py`, `layer1_evaluate.py` | `layer1_ecc/*.json` |
| Robustness tests (Section 5.6) and traced record (Section 4.3) | `extra_analysis.py` | `results/extra_robustness/extra_results.json` |
| CybAttT auxiliary check (Table 5.7; Figure 5.4) | `cybattt_pipeline.py` | `results/cybattt/cybattt_results.json` |
| Thesis-vs-code comparison of 279 numbers | `verify_thesis.py`, `thesis_claims.json` | `results/main_results/reconciliation.md` |

## Quick start

```bash
cd code
python -m pip install -r requirements.txt pdfplumber
./run_all.sh      # main experiments, seed 42 (~15 min on one CPU core) + thesis-vs-code check
./run_extra.sh    # robustness analyses, Layer 1 extraction and evaluation (~10 min)
```

Environment used for the thesis: main experiments with Python 3.12.3, robustness analyses with Python 3.13.16; both
with scikit-learn 1.8.0, xgboost 3.4.1, numpy 2.4.4, pandas 3.0.2 and matplotlib 3.10.8 (recorded in the
`environment` field of each result file). Other library versions may change XGBoost and cross-validation results in
the third decimal place.

## External data (not included)

- **NCA ECC-1:2018 (English):** download from https://nca.gov.sa and save as `code/ecc-en.pdf` (needed for Layer 1 extraction only; the reference set derived from it is included).
- **CybAttT tweets:** not redistributed because they contain real users' posts. Download `df_m.csv` from
  https://github.com/HudaLughbi/CybAttT (Lughbi et al., 2024, doi:10.3390/data9030039) and save it as
  `code/data/CybAttT_df_m.csv`. The pipeline regenerates the cleaned file.

## Limitations

The main experiments use synthetic posts and simulated audit series; results do not represent performance on
real organisational data, and performance on synthetic data is not evidence of effectiveness on real-world data.
Under template-family holdout the classifier falls to macro F1 0.36 (XGBoost) and 0.29 (logistic regression).
The mapping between posts and NCA controls is researcher-defined and was not validated by experts. The bilingual
AraBERT/AraBART parser is a design only and is not part of this code. The Layer 1 reference set is built
programmatically from the PDF and spot-checked, not expert-adjudicated. The paraphrase test set was written by the
researcher, not by domain experts. See Sections 5.6, 6.4 and 6.5 of the thesis.

## Citation

Al-Ruwaili, S. G. (2026). *A machine learning-based framework for predictive and continuous cybersecurity GRC automation* (MSc thesis).
Northern Border University, Arar, Saudi Arabia.

## License

Code released under the MIT License (see `LICENSE`).
