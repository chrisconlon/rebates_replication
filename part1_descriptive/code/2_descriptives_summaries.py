import setup_descriptives
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.formula.api as smf


from setup_descriptives import raw_dir, proc_dir, tab_dir, fig_dir, setup_figures
from descriptive_helper import summary_tex, threshold_calc, threshold_tex, threshold_reg_tex, plot_statevars

setup_figures()

f_vvs = raw_dir / 'vv_snacks.parquet'
f_vvi = raw_dir / 'vvi_all.parquet'
f_prod = raw_dir / 'product_data.parquet'
f_national=raw_dir /'national_prods.xlsx'
f_merged = proc_dir / 'merged_data.parquet'

read_cols = ['vvs_id','new_pro_id','vended','dex_vended','par','capacity']

# tables
f_summary = tab_dir /'table1_summary.tex'
f_tab_thrshold = tab_dir /'table2_threshold.tex'
f_ols = tab_dir /'table3_ols.tex'

# figures
fig_statesvars = fig_dir / 'statevars_mc15.pdf'
fig_statesvars_iqr = fig_dir / 'statevars_mc15_iqr.pdf'

# read in data
prod=pd.read_parquet(f_prod)
df1=pd.read_parquet(f_vvs)
df2=pd.read_parquet(f_vvi,columns = read_cols)
dfn=pd.read_excel(f_national)
merged_df=pd.read_parquet(f_merged)

### Product Summaries: Table 1
out_tex=summary_tex(merged_df, dfn, prod)
with open(f_summary, "w") as text_file:
    print(out_tex, file=text_file)

## Arrival rate figures: Figure 4
effort_df=df1[(df1.rank_vends>0.75)&(df1.keep)].copy()
effort_iqr=df1[(df1.rank_vends>0.5)&(df1.rank_vends<=0.75)&(df1.keep)].copy()

# For our top 25%
plot_statevars(effort_df,195,209)
plt.savefig(fig_statesvars,bbox_inches='tight')

# For middle 50%
plot_statevars(effort_iqr, 214 , 228 )
plt.savefig(fig_statesvars_iqr,bbox_inches='tight')

## Threshold Calculations
#1. Recover observed policy functions at different quantiles
#2. Compute YoY change in quarterly Mars sales
#3. Compute Mars and Overall Sales and Share

# top quarter of machines and average days between visits
vends=df1[(df1.rank_vends>0.75)&(df1.keep)].groupby(['quarter_end'])[['product_vends']].mean().round(2)
elapsed=df1[(df1.keep)].groupby(['quarter_end'])[['Elapsed']].mean().round(2)

# Overall sales calculations for: (a) all data (b) balanced panel (c) our experimental machines
a=threshold_calc(merged_df)
b=threshold_calc(merged_df[merged_df.balanced])
c=threshold_calc(merged_df[merged_df.ExpMachine>0])

dft=a[['vended_index','mars_index','mars_conf_share','yoy']].round(2)
dft2=pd.concat([dft, pd.DataFrame(vends['product_vends']),elapsed],axis=1)
totals=pd.concat([dft2[dft2.index<='2007Q4'].mean(),dft2[dft2.index>'2007Q4'].mean()],axis=1).transpose()
totals.index=['Pre 2008 Avg','Post 2008 Avg']
dft3 =pd.concat([dft2, totals],axis=0).round(2)
print(dft3)

# Table 2
out_tex2=threshold_tex(dft3)
with open(f_tab_thrshold, "w") as text_file:
    print(out_tex2, file=text_file)

# Some stats used in paper
print("Low Threshold\n")
print(dft2[(dft2.index>'2007Q4')&(dft2.index<'2009Q1')].mean())
print("\nHigh Threshold \n")
print(dft2[(dft2.index<='2007Q4')].mean())
print("\n")


# Tag the "exclusion" period (pre- 2008)
tmp=df1[~df1.Elapsed.isnull()][['Elapsed','product_vends','exclusion','pos_id','week_of_year']].copy()
tmp['exclusion']=(~tmp['exclusion']).values*1

# Use Elapsed and Vends as LHS
mod1 = smf.ols(formula='Elapsed ~ exclusion + C(pos_id)+C(week_of_year)', data=tmp)
mod2 = smf.ols(formula='product_vends ~ exclusion + C(pos_id)+C(week_of_year)', data=tmp)

res1=mod1.fit()
res2=mod2.fit()
out_str=threshold_reg_tex(res1,res2)

# Table 3
with open(f_ols, "w") as text_file:
    print(out_str, file=text_file)
