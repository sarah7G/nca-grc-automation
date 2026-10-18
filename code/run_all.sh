#!/usr/bin/env bash
# Reproduces every table of Chapter 5 from scratch and compares it with the thesis (Python 3.12.3, see requirements.txt).
set -e
python run_experiment.py --seed 42 --out results                                              # ~14 min on one CPU core
[ -f data/CybAttT_df_m.csv ] && python cybattt_pipeline.py --input data/CybAttT_df_m.csv --out results_cybattt                # ~25 min; needs data/CybAttT_df_m.csv (see README)
python verify_thesis.py results/results.json --full                                           # writes results/reconciliation.md
