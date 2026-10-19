#!/usr/bin/env bash
# Robustness analyses and Layer 1 extraction (same seed/data as run_all.sh). Run after: pip install -r requirements.txt pdfplumber
set -e
python extra_analysis.py --seed 42 --out results_extra            # ~10 min: template/domain/paraphrase splits, overlap, bootstrap CIs, MAE variability, remediation regimes, traced record
python layer1_extract.py --doc ecc-en.pdf --out layer1_out --expected_controls 114                       # baseline regex extractor (52 controls, 96 sub-controls)
python layer1_extract_coord_controls.py && python layer1_extract_coord_subcontrols.py                    # coordinate-based reader -> coord_records_all.json (114 + 105; saved copy: ../layer1_ecc/layer1_reference_from_pdf.json)
python layer1_evaluate.py --controls controls.csv --reference ../layer1_ecc/layer1_reference_from_pdf.json --tweets results/tweets_used.csv --out ../layer1_ecc   # identifier precision/recall, text fidelity, linking comparison (needs results/ from run_all.sh)
python verify_thesis.py results/results.json --full                                    # thesis-vs-code check using the freshly generated files
