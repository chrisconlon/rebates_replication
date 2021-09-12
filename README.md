## Replication of Conlon and Mortimer
## Efficiency and Foreclosure Effects of Vertical Rebates: Empirical Evidence (JPE 2021)

[https://www.journals.uchicago.edu/doi/10.1086/716563](https://www.journals.uchicago.edu/doi/10.1086/716563)

## Organization of files

We organize the files in the replication package into two parts:
1. Part 1 does the descriptive analysis (in Python)
2. Part 2 does the numerical simulation model (in Matlab)

Each part lives in a separate folder. Within each folder we separate files as

PartX
./code : where the code lives and is run from
./raw_data : inputs we provide as part of the replication package / or can provide upon request

Figures and Tables saved in eponymously named folders

## Requirements

The following packages/dependencies are required to run the replication package
1. Python 3.7 or higher (pandas, numpy, matplotlib, statsmodels, pyarrow)
2. MATLAB (tested on R2020a): slmengine (SLM Toolbox)

The python packages (appropriate versions) can be install via pip with 

```
pip install -r requirements.txt
```
