## Replication of Conlon and Mortimer
## Efficiency and Foreclosure Effects of Vertical Rebates: Empirical Evidence (JPE 2021)

[https://www.journals.uchicago.edu/doi/10.1086/716563](https://www.journals.uchicago.edu/doi/10.1086/716563)

## Organization of files

We organize the files in the replication package into two parts:
1. Part 1 does the descriptive analysis (in Python)
- This produces Tables 1-5
2. Part 2 does the numerical simulation model (in Matlab)

Each part lives in a separate folder. Each folder has its own README with the corresponding list of Tables and Figures and where they are created.

Within each folder we separate files as:

PartX/
1. ./code : where the code lives and is run from
2. ./raw_data : inputs we provide as part of the replication package / or can provide upon request
3. Figures and Tables saved in eponymously named folders

Please see the separate README.md in each folder for detailed instructions

## Requirements

The following packages/dependencies are required to run the replication package
1. Python 3.7 or higher (pandas, numpy, matplotlib, statsmodels, pyarrow)
2. MATLAB (tested on R2020a): slmengine (SLM Toolbox)

The python packages (appropriate versions) can be install via pip with 

```
pip install -r requirements.txt
```


### Data availability

We have provided a subset of the full dataset for replication purposes within this package. We've anonymized some of the sensitive client information. The replication files should run and produce all of the tables and figures in the paper (except those drawn by hand, including the presenation slides, etc.).

Certain intermeidate data products are constructed from a combination of raw materials (provided) and proprietary information (not provided) in those cases we provide the suitably anonymized intermediate data products.