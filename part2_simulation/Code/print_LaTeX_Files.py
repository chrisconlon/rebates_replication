import pandas as pd
import numpy as np
import pathlib

# Directory names
table_dir = pathlib.Path.cwd().parent / 'Tables and Figures'
input_dir = pathlib.Path.cwd().parent / 'Table Output'
state_dir = pathlib.Path.cwd().parent / 'Output'


import table_helpers
from table_helpers import process_main, compress_table,compress_table2, main_table, main_table2, eff_table,table9_both,\
 effort_table, net_effects, net_effects2, merger_table, ref_table, write_tex_table

#inputs
fn_main=input_dir / 'mc15-tables.mat'
fn_cs= input_dir / 'mc15-cs-tables.mat'
fn_fc15=input_dir / 'mc15-fc15-tables.mat'
fn_fc5=input_dir / 'mc15-fc5-tables.mat'
fn_iqr=input_dir / 'mc15-iqr-tables.mat'
fn_mc0=input_dir / 'mc0-tables.mat'
fn_fig2 = input_dir / 'threshold_figure.mat'
fn_payoffs = input_dir / 'payoffs-mc15.mat'


## Main Text Tables for main specification

# Table 9: FC = 10;MC = 0.15
df=process_main(fn_main)
b = main_table2(compress_table2(df))
write_tex_table(table_dir / 'table_9.tex', b)

# Table 10: Threshold (other file)

#Table 11
a=effort_table(fn_main)
write_tex_table(table_dir / 'table_11.tex', a)

#Table 12
b=ref_table(fn_main)
write_tex_table(table_dir / 'table_12.tex', b)
    
#Table 13
c=net_effects(fn_main)
write_tex_table(table_dir / 'table_13.tex', c)

#Table 14
d=merger_table(fn_main)
write_tex_table(table_dir / 'table_14.tex', d)


## Net Effects for alternative specifications
#Table A1
e=net_effects2(fn_iqr,include_se=False)
write_tex_table(table_dir / 'table_A1.tex', e)

#Table A2
#e=net_effects2(fn_mc0, include_se=False)
#write_tex_table(table_dir / 'table_A2.tex', e)

#Table A3
e=net_effects2(fn_fc5, include_se=False)
write_tex_table(table_dir / 'table_A3.tex', e)

#Table A4
e=net_effects2(fn_fc15, include_se=False)
write_tex_table(table_dir / 'table_A4.tex', e)


## Effort and Net Effects for CS model
#Table A5
b=effort_table(fn_cs)
print(b)
write_tex_table(table_dir / 'table_A5.tex',b)

#Table A6
e=net_effects2(fn_cs, include_se=False)
write_tex_table(table_dir / 'table_A6.tex', e)

## Long-run profits for alternative specifications
# Table A7: FC = 10;MC = 0.15
df=process_main(fn_main)
b = main_table(compress_table(df))
write_tex_table(table_dir / 'table_A7.tex',b)

# Table A8: FC = 10;MC = 0
df=process_main(fn_mc0)
b = main_table(compress_table(df))
write_tex_table(table_dir / 'table_A8.tex',b)
    
# Table A9: FC = 10;MC = 0.15 IQR arrival
#df=process_main(fn_iqr)
#b = main_table(compress_table(df))
#write_tex_table(table_dir / 'table_A9.tex',b)
    
# Table A10: FC = 5;MC = 0:15
#df=process_main(fn_fc5)
#a=main_table(compress_table(df))
#write_tex_table(table_dir / 'table_A10.tex',a)
    
# Table A11: FC = 15;MC = 0.15
#df=process_main(fn_fc15)
#b = main_table(compress_table(df))
#write_tex_table(table_dir / 'table_A11.tex',b)

# Table A12: FC = 10;MC = 0:15
#df=process_main(fn_cs)
#a=main_table(compress_table(df))
write_tex_table(table_dir / 'table_A12.tex',a)

