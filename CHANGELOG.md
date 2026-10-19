# Changelog

## v1.1 (October 2026) — release cited in the final thesis

No experiment was re-run with different settings and no reported number changed. Changes:

- Added `code/layer1_evaluate.py`, which regenerates `layer1_ecc/layer1_text_eval.json` (identifier precision/recall and
  token-level text fidelity against the PDF reference set) and `layer1_ecc/linking_comparison.json` (linking with the
  baseline and the coordinate-based knowledge base). In v1.0 these two files were included without the script that
  produced them. The script reproduces both files exactly (to floating-point precision).
- `verify_thesis.py` now also checks the robustness tests (`extra_results.json`), the CybAttT results and the Layer 1
  evaluation: 279 numbers in total, all MATCH (`results/main_results/reconciliation.md`). Table and section labels were
  updated to the numbering of the final thesis, and keys that contain dots are now read correctly.
- `run_extra.sh` runs `layer1_evaluate.py` and the thesis-vs-code check after the robustness analyses.
- Documentation: README files state the Python versions actually used (3.12.3 for the main run, 3.13.16 for the
  robustness analyses), map every Chapter 5 result to its script and output file, and state the limitations
  (synthetic data, template-family holdout, researcher-defined mapping, AraBERT/AraBART design only).
- `results/cybattt/CYBATTT_RESULTS.md`: the "Thesis" column now shows the values printed in the final thesis.
- Table labels in code comments and in `results_tables.md` headings updated to the final thesis numbering.
- Two outdated note strings (in `layer1_link.py`, `extra_analysis.py` and the corresponding `note` fields of
  `results.json` and `extra_results.json`) now point to `layer1_evaluate.py`; no numeric field was changed.

Check: `run_experiment.py` and `extra_analysis.py` were re-run in a clean environment (Python 3.13.16 with the pinned
library versions); `results.json`, `extra_results.json`, `tweets_used.csv` and `audit_events.csv` were identical to the
published files (no numeric difference).

## v1.0 (commit 7052cdd)

Initial release of the thesis code and results.
