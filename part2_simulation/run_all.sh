#!/usr/bin/env bash
set -e

cd Code

#Matlab Block
matlab profits_mc0_sim.m
matlab compute_profits.m
matlab run_threshold_figure.m
matlab create_figures.m
matlab calculate_all_tables.m

# Python block
python print_latex_tables.py
python print_thresholds.py