#!/usr/bin/env python
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

get_ipython().run_line_magic('run', 'setup_descriptives.py')

f_vvs = raw_dir / 'vv_snacks.parquet'
f_vvi = raw_dir / 'vvi_all.parquet'
f_prod = raw_dir / 'product_data.parquet'

keep_cols=['vvs_id','pos_id','cus_id','ExpMachine','product_vends','Elapsed','mydate','month_end','quarter_end','balanced','exclusion','n_visits']
export_cols=['vvs_id','pos_id','Elapsed','product_vends','week_of_year','ExpMachine','balanced','mydate','exclusion']

from descriptive_helper import merge_df, compute_facings, plot_categories, plot_facings, plot_overall
## Set the threshold date


tab_facings = tab_dir / 'facings_table.tex'
# output (figures)
fig_category = fig_dir / 'facings_category.pdf'
fig_catmanuf_exp = fig_dir / 'facings_category_manuf_exp.pdf'
fig_catmanuf_bal = fig_dir / 'facings_category_manuf_bal.pdf'

fig_prod_exp = fig_dir / 'facings_prod_exp.pdf'
fig_prod_bal = fig_dir / 'facings_prod_bal.pdf'
fig_base_exp = fig_dir / 'facings_prod_base_exp.pdf'
fig_base_bal = fig_dir / 'facings_prod_base_bal.pdf'

### Don't bother with weighted (basically identical)
#fig_prod_exp_w = fig_dir / 'facings_prod_exp_w.pdf'
#fig_prod_bal_w = fig_dir / 'facings_prod_bal_w.pdf'
#fig_base_exp_w = fig_dir / 'facings_prod_base_exp_w.pdf'
#fig_base_bal_w = fig_dir / 'facings_prod_base_bal_w.pdf'


# In[2]:


get_ipython().run_cell_magic('time', '', 'prod=pd.read_parquet(f_prod)\ndf1=pd.read_parquet(f_vvs)\ndf2=pd.read_parquet(f_vvi)\n\n\n# Filter for vvs_id in our sample\ndf2a=df2[df2.vvs_id.isin(df1.vvs_id.unique())]\n\nfacings=compute_facings(df2a,prod,sales_cutoff = 3e4)\nfacing_cols=facings.columns')


# In[3]:


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
pd.concat([y1,y2],axis=1).to_latex(tab_facings,column_format='l rrrr | rrrr')


# ## Overall facings
# - Total by firm
# - By firm x category pairs
# - weighting by sales almost never matters

# In[4]:


plot_overall(big_df_plot)
plt.savefig(fig_category,bbox_inches="tight")


# In[5]:


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

