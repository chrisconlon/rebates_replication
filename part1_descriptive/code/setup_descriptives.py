# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 17:49:41 2016

@author: cconlon
"""

import numpy as np
import pandas as pd
import pathlib

import matplotlib
import matplotlib.pyplot as plt
from cycler import cycler
import seaborn as sns

proj_dir = pathlib.Path.cwd().parent 
raw_dir = proj_dir / 'raw_data'
proc_dir = proj_dir / 'proc_data'
fig_dir = proj_dir / 'figures'
tab_dir = proj_dir / 'tables'
temp_dir = proj_dir / 'temp'
db_dir = proj_dir / 'db'

# Plot Configuration
def setup_figures():
	matplotlib.style.use('seaborn-whitegrid')
	matplotlib.rcParams.update({'font.size': 24})
	plt.rc('font', size=24)          # controls default text sizes
	plt.rc('axes', titlesize=24)     # fontsize of the axes title
	plt.rc('axes', labelsize=24)    # fontsize of the x and y labels
	plt.rc('xtick', labelsize=24)    # fontsize of the tick labels
	plt.rc('ytick', labelsize=24)    # fontsize of the tick labels
	plt.rc('legend', fontsize=24)    # legend fontsize
	plt.rc('figure', titlesize=24)
	#plt.rc('axes', prop_cycle=cycler(color=['008fd5', 'fc4f30', 'e5ae38', '6d904f', '8b8b8b', '810f7c']))
	#plt.rc('axes',prop_cycle=cycler(color=['c', 'm', 'y', 'k'], lw=[1, 2, 3, 4]))
	# bw: ['#252525', '#636363', '#969696', '#bdbdbd', '#d9d9d9']
	#plt.rc('axes',prop_cycle=cycler(color=['#252525', '#636363', '#969696', '#bdbdbd'])*cycler(linestyle=['-',':','--', '-.']))
	plt.rc('axes',prop_cycle=cycler(color=['navy'])*cycler(linestyle=['-', '--', ':', '-.']))

	plt.rc('lines', linewidth=3)
	return