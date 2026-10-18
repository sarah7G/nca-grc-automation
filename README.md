# A Machine Learning-Based Framework for Predictive and Continuous Cybersecurity GRC Automation

Code, generated data and results for the MSc thesis of **Sara G. Al-Ruwaili**,
Department of Computer Science, College of Science, Northern Border University (Arar, Saudi Arabia).
Supervisor: Dr. Randa S. S. Allafi.

The repository reproduces the experiments reported in Chapter 5 of the thesis: a compliance-status
text classifier, CUSUM drift detection on simulated audit series, compliance-risk forecasting,
remediation prioritisation, robustness analyses, and a rule-based extraction of NCA ECC-1:2018 (Layer 1).

## Contents

| Folder | Description |
|---|---|
| `code/` | All experiment code, run scripts and pinned requirements (see `code/README.md`) |
| `results/main_results/` | Outputs of `run_experiment.py`: `results.json`, tables, figures, generated post corpus (`tweets_used.csv`) and simulated audit events (`audit_events.csv`) |
| `results/extra_robustness/` | `extra_results.json`: template/domain/paraphrase splits, bootstrap intervals, forecaster variability, reward regimes |
| `results/cybattt/` | Auxiliary experiment on the public CybAttT tweet dataset |
| `layer1_ecc/` | Layer 1 outputs: reference set built from the ECC PDF (`layer1_reference_from_pdf.json`), extraction evaluation, linking comparison |
| `figures/` | Architecture figure (Figure 4.1) |

## Quick start

```bash
cd code
python -m pip install -r requirements.txt pdfplumber   # Python 3.12
./run_all.sh      # main experiments, seed 42 (~15 min on one CPU core)
./run_extra.sh    # robustness analyses and Layer 1 extraction
```

## External data (not included)

- **NCA ECC-1:2018 (English):** download from https://nca.gov.sa and save as `code/ecc-en.pdf` (needed for Layer 1 only).
- **CybAttT tweets:** not redistributed because they contain real users' posts. Download `df_m.csv` from
  https://github.com/HudaLughbi/CybAttT (Lughbi et al., 2024, doi:10.3390/data9030039) and save it as
  `code/data/CybAttT_df_m.csv`. The pipeline regenerates the cleaned file.

## Limitations

The main experiments use synthetic posts and simulated audit series; results do not represent performance on
real organisational data. The Layer 1 reference set is built programmatically from the PDF and spot-checked,
not expert-adjudicated. The paraphrase test set was written by the researcher, not by domain experts.
See Sections 5.6 and 6.4 of the thesis.

## Citation

Al-Ruwaili, S. G. (2026). *A machine learning-based framework for predictive and continuous cybersecurity GRC automation* (MSc thesis).
Northern Border University, Arar, Saudi Arabia.

## License

Code released under the MIT License (see `LICENSE`).
