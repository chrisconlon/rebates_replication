# Efficiency and Foreclosure Effects of Vertical Rebates: Empirical Evidence- Conlon and Mortimer

## How to run code
Change to the directory containing this file and run "./run_all.sh" on the terminal. The code should take approximately 4 hours to run. Tables and figures will be produced as described below in the file titled "Tables and Figures".

# (Provision of Data and Where to get it)

## File of origin for tables and figures

| Table/Figure Number | Generating File (Data)      | Generating File (Table)      |
| ------------------------ | -----------------------------|------------------------------ |  
| Table 6                      | (By Hand)                                          |                                          
| Table 7                      | (By Hand)                                           |                                          
| Table 8                      | calculate_all_tables       | Print Latex Tables.py 
| Table 9                      | calculate_all_tables.m     | Print Latex Tables.py         |
| Table 10                     | run_threshold_figure.m     | Print Latex Tables.py          |
| Table 11                     | calculate_all_tables.m     | Print Latex Tables.py          |
| Table 12                     | calculate_all_tables.m     | Print Latex Tables.py          |
| Table 13                     | calculate_all_tables.m     | Print Latex Tables.py          | 
| Table 14                     | calculate_all_tables.m     | Print Latex Tables.py          |
| Table A1                     | calculate_all_tables.m     | Print Latex Tables.py          |
| Table A2                     | calculate_all_tables.m     | Print Latex Tables.py          |
| Table A3                     | calculate_all_tables.m     | Print Latex Tables.py          |
| Table A4                     | calculate_all_tables.m     | Print Latex Tables.py          |
| Table A5                     | calculate_all_tables.m     | Print Latex Tables.py          |
| Table A6                     | calculate_all_tables.m    | Print Latex Tables.py           |
| Table A7                     | calculate_all_tables.m   | Print Latex Tables.py            |
| Table A8                     | calculate_all_tables.m    | Print Latex Tables.py           |
| Table A9                     | calculate_all_tables.m     | Print Latex Tables.py          |
| Table A10                   | calculate_all_tables.m     | Print Latex Tables.py          |
| Table A11                   | calculate_all_tables.m    | Print Latex Tables.py          |
| Table A12                   | calculate_all_tables.m     | Print Latex Tables.py          |
|                                    |                                         |                                             |
| Figure 1                      | (By Hand)                        | (By Hand)                            |
| Figure 2                      |  run_threshold_figure.m  | Print Latex Tables.py          |
| Figure 3                      | N/A                                  | Print Latex Tables.py          | 
| Figure 4                      | run_threshold_figure.m   | Print Latex Tables.py          |
| Figure A2                    |  N/A                                 | Print Latex Tables.py          |
| Figure A3                    | compute_profits.m          | create_figures.m                 |
| Figure A4                    | compute_profits.m          |   run_linear.m                      |


## Python and Matlab dependencies (General Functions that are used throughout code)
Python: pandas, table_helpers, numpy, os, sys, interleave, loadmat, matplotlib, matplotlib.pyplot

Matlab
: squeeze, std, round, mean, latexmat,  disp, save, fullfile, addpath, load, cumsum, size, mrdivide, augmentF, textscan, fopen, meshgrid, max, heatmap, find, scatter, unique, histc, full, flipud, length, helpers, SLMtools


## Files Provided

Data

~\Raw Data
:inventory.mat,

:posterior_theta.mat

:main-short.mat,

:mle-estimates.mat

:statetransitions.csv

:statetransitions-iqr.csv 

~\Output Data

:statevars.mat & statevars_iqr.mat (State Variables with the top quartile and IQR) 

:SalesHM-mle.mat, SalesHH-mle.mat, SalesMM-mle.mat & SalesNN-mle.mat (Sales levels of various vending machine assortments)

:Profits_mc15.mat (Matrices containing optimal effort policies and corresponding profits with a marginal cost of 0.15)

:Profits_mc0.mat (Matrices containing optimal effort policies and corresponding profits with a marginal cost of 0)

:Profits_mc15-cs.mat (Matrices containing optimal effort policies and corresponding profits with consumer surplus)

:Profits_mc15-fc5.mat (Matrices containing optimal effort policies and corresponding profits with a fixed cost of 5)

:Profits_mc15-fc15.mat (Matrices containing optimal effort policies and corresponding profits with a fixed cost of 15)

~\ Table Output Data

:payoffs-mc15.mat (Smoothed Profits for HM Sales Assortment with a Marginal Cost of 0.15)

:threshold_figure.mat (Profits Data used to create a graph of Manufacturer-Retailer (with rebate) profits with Thresholds)

:mc15-tables.mat (Policy and Profit tables with upper quartile data obtained from simulated profit data)

:mc15-iqr-tables.mat (Policy and Profit with inter-quartile Data obtained from simulated profit data )

:mc0-tables.mat (Computed estimates of policy and profit data of various product assortments with a marginal cost of 0)

:mc15-fc5-tables.mat (Policy and Profit with inter-quartile Data obtained from simulated profit data with a fixed cost of 5)

:mc15-fc15-tables.mat (Policy and Profit with inter-quartile Data obtained from simulated profit data with a fixed cost of 15)

:mc15-cs-tables.mat (Policy and Profit with inter-quartile Data obtained from simulated profit data with consumer surplus)


## Downloading Data (Details on how to download or otherwise obtain the dataset used)

User must provide "Y" to "Z".

Note:

These should live in the file titled "X".

:(Raw Data files obtained from the source with description)
