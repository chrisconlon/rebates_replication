import setup_descriptives
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

from setup_descriptives import raw_dir, proc_dir, tab_dir, fig_dir, setup_figures
from descriptive_helper import merge_df, compute_facings, plot_categories, plot_facings, plot_overall

# get figure style
setup_figures()

f_vvs = raw_dir / 'vv_snacks.parquet'
f_vvi = raw_dir / 'vvi_all.parquet'
f_prod = raw_dir / 'product_data.parquet'

keep_cols=['vvs_id','pos_id','cus_id','ExpMachine','product_vends','Elapsed','mydate','month_end','quarter_end','balanced','exclusion','n_visits']
export_cols=['vvs_id','pos_id','Elapsed','product_vends','week_of_year','ExpMachine','balanced','mydate','exclusion']

## Set the threshold date
tab_facings = tab_dir / 'facings_table.tex'

# output (figures)
fig_catmanuf_bal = fig_dir / 'fig2_facings_category_manuf_bal.pdf'
fig_prod_bal = fig_dir / 'fig2_facings_prod_bal.pdf'

# Appendix figures
fig_category = fig_dir / 'fig_A1_facings_category.pdf'
fig_catmanuf_exp = fig_dir / 'fig_A2_facings_category_manuf_exp.pdf'
fig_base_exp = fig_dir / 'fig_A3_facings_prod_base_exp.pdf'
fig_base_bal = fig_dir / 'fig_A3_facings_prod_base_bal.pdf'
fig_prod_exp = fig_dir / 'fig_A4_facings_prod_exp.pdf'


# read in the data
prod=pd.read_parquet(f_prod)
df1=pd.read_parquet(f_vvs)
df2=pd.read_parquet(f_vvi)

# Filter for vvs_id in our sample
df2a=df2[df2.vvs_id.isin(df1.vvs_id.unique())]
facings=compute_facings(df2a,prod,sales_cutoff = 3e4)
facing_cols=facings.columns


# Filter df1 for our drops and balanced sample only -- otherwise we lose facings overtime as machines get smaller
big_df=merge_df(df1[(df1.keep)&(df1.balanced)&(df1['n_visits']>=10)][keep_cols],facings)

# Display 2006 or not?
big_df_plot=big_df[big_df.mydate> pd.to_datetime('2006-12-31')].copy()

def compute_facings_table(big_df):
    x=big_df.groupby(['quarter_end'])[['Mars','Hershey','Nestle']].mean()
    y=pd.concat([x,x.sum(axis=1).rename('Total')],axis=1).round(1)
    y.index=[str(x) for x in y.index]
    return y

y1= compute_facings_table(big_df[big_df.balanced])
y2= compute_facings_table(big_df[big_df.ExpMachine>0])
pd.concat([y1,y2],axis=1)#.to_latex(tab_facings,column_format='l rrrr | rrrr')

# ## Overall facings
# - Total by firm
# - weighting by sales doesn't matter

plot_overall(big_df_plot)
plt.savefig(fig_category,bbox_inches="tight")

# by firm x category papers
plot_categories(big_df_plot[big_df_plot.balanced])
plt.savefig(fig_catmanuf_bal,bbox_inches='tight')
plot_categories(big_df_plot[big_df_plot.ExpMachine>0])
plt.savefig(fig_catmanuf_exp,bbox_inches='tight')


# ## Product Level Facings
# - Key products for our analysis
# - Mars: MilkyWay and M&M Plain and 3 Musketeers
# - Nestle: Raisinets
# - Hershey: Butterfinger
# - Skip weighting schemes -- imperceptible difference
plot_facings(big_df_plot[big_df_plot.balanced],use_weights=False)
plt.savefig(fig_prod_bal,bbox_inches='tight')

plot_facings(big_df_plot[big_df_plot.ExpMachine>0],use_weights=False)
plt.savefig(fig_prod_exp,bbox_inches='tight')


# ### Base Mars Product Assortment
# - These are high and stable (not affected)
big_df_plot[big_df_plot.ExpMachine>0].groupby(['month_end']).mean()[['M&M Peanut','Twix','Snickers','Skittles/Starburst']].plot(figsize=(20,10),color=['navy', 'navy','navy','navy'],style=['-','-.','--',':','-','-.'])
plt.xlabel('')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncol=2)
plt.ylim(0, 1.2) 
plt.savefig(fig_base_exp,bbox_inches='tight')

big_df_plot[big_df_plot.balanced].groupby(['month_end']).mean()[['M&M Peanut','Twix','Snickers','Skittles/Starburst']].plot(figsize=(20,10),color=['navy', 'navy','navy','navy'],style=['-','-.','--',':','-','-.'])
plt.xlabel('')
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncol=2)
plt.ylim(0, 1.2) 
plt.savefig(fig_base_bal,bbox_inches='tight')

