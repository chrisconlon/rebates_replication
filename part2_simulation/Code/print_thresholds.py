import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib

# Directory names
table_dir = pathlib.Path.cwd().parent / 'Tables and Figures'
input_dir = pathlib.Path.cwd().parent / 'Table Output'
state_dir = pathlib.Path.cwd().parent / 'Output'

import table_helpers
from table_helpers import read_one, flow_profit_plot, print_thresholds, give_thresholds, threshold_check, write_tex_table

# Plot Configuration
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('seaborn-whitegrid')
matplotlib.rcParams.update({'font.size': 24})
plt.rc('font', size=24)          # controls default text sizes
plt.rc('axes', titlesize=24)     # fontsize of the axes title
plt.rc('axes', labelsize=24)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=24)    # fontsize of the tick labels
plt.rc('ytick', labelsize=24)    # fontsize of the tick labels
plt.rc('legend', fontsize=24)    # legend fontsize
plt.rc('figure', titlesize=24)
plt.rc('lines', linewidth=6)  # line width default


#inputs
fn_main=input_dir / 'mc15-tables.mat'
fn_cs= input_dir / 'mc15-cs-tables.mat'
fn_fc15=input_dir / 'mc15-fc15-tables.mat'
fn_fc5=input_dir / 'mc15-fc5-tables.mat'
fn_iqr=input_dir / 'mc15-iqr-tables.mat'
fn_mc0=input_dir / 'mc0-tables.mat'
fn_fig2 = input_dir / 'threshold_figure.mat'
fn_payoffs = input_dir / 'payoffs-mc15.mat'


### Flow Profits (Figure 2)
flow_profit_plot(fn_payoffs)
plt.savefig(table_dir / 'perunitprofit_mc15.pdf',bbox_inches='tight')


# ### Critical Thresholds
(marsHH,retailHH,retailHH_r)=read_one(fn_fig2,'profitsHH')
(marsHM,retailHM,retailHM_r)=read_one(fn_fig2,'profitsHM')
(marsMM,retailMM,retailMM_r)=read_one(fn_fig2,'profitsMM')

x_min = min(marsHM)
x_max = max(marsMM)

plt.figure(figsize=(20,10))
plt.plot(marsHM, retailHM_r,'k-.',marsMM, retailMM_r,'k-')
plt.xlabel('Mars Profits')
plt.ylabel('Retailer (Post-Rebate) Profits')

MM_max=max(retailMM_r)
Mars_cutoff=max(marsHM[retailHM_r > max(retailMM_r)])

plt.axhline(y=MM_max,linestyle=':',color='gray')
plt.axvline(x=Mars_cutoff,linestyle=':',color='gray')
#plt.axvline(x=35813,linestyle=':',color='gray')


plt.legend([r'$(H,M): \pi^R + \lambda \pi^M$',r'$(M,M): \pi^R + \lambda \pi^M$','Foreclosure Threshold'])

#for i, txt in enumerate(n):

# mc=0
#idx=np.array([191,169,189,168])-120
#mc=15
idx=np.array([196,172,195,171])-120

x=np.concatenate((marsHM[idx[0:2]],marsMM[idx[2:]]))
y=np.concatenate((retailHM_r[idx[0:2]],retailMM_r[idx[2:]]))

plt.scatter(x, y,color='black',marker='o',s=256)
plt.annotate(r'$e^{VI}$', (x[0]+100, y[0]),size='24')
plt.annotate(r'$e^{SOC}$', (x[1]+100, y[1]),size='24')
plt.annotate(r'$e^{VI}$', (x[2]+100, y[2]),size='24')
plt.annotate(r'$e^{SOC}$', (x[3]+100, y[3]),size='24')

## this block for empirical policy
#plt.scatter(marsHM[31], retailHM_r[31],color='black',marker='^',s=256)
plt.scatter(marsMM[31], retailMM_r[31],color='black',marker='^',s=256)
#plt.annotate(r'$e^{MV}$', (marsHM[31]+100, retailHM_r[31]),size='24')
plt.annotate(r'$e^{OBS}$', (marsMM[31]+100, retailMM_r[31]),size='24')

plt.savefig(table_dir / 'threshold_figure.pdf',bbox_inches='tight')
plt.show()


print_thresholds(fn_fig2)
#Create the initial dataframe for Table 10
table10strt = give_thresholds(fn_fig2)
table10strt.insert(0,0)
table10strt.insert(7,0)
table10assortment = ['(H,H)','(H,H)', '(H,M)','(H,M)','(M,M)','(M,M)','(H,H)']
table10effort = ['$e^{R}(H, H)$', '$e\\left(\\bar{\\pi}_{M}(H, H)\\right)$','$e^{R}(H, M)$','$e\\left(\\bar{\\pi}_{M}(H, M)\\right)$','$e^{R}(M, M)$','$e\\left(\\bar{\pi}_{M}(M, M)\\right)$','$e^{N R}(H, H)$']
table10 =  pd.DataFrame(list(zip(table10strt[0:7], table10strt[1:8], table10assortment, table10effort)))


#Replace 0 in the bottom of the second column with \infty in table_10.tex

#Table 10
e=threshold_check(table10)
write_tex_table(table_dir / "table_10.tex",e )
