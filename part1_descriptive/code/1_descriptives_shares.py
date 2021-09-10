import setup_descriptives
import pandas as pd
from setup_descriptives import raw_dir, proc_dir, tab_dir, fig_dir
from descriptive_helper import summary_one, threshold_calc, summary_tex, threshold_tex, threshold_reg_tex, plot_statevars

f_vvs = raw_dir / 'vv_snacks.parquet'
f_vvi = raw_dir / 'vvi_all.parquet'
f_prod = raw_dir / 'product_data.parquet'
f_national=raw_dir /'national_prods.xlsx'

keep_cols=['vvs_id','pos_id','Elapsed','ExpMachine','week_of_year','keep','balanced','exclusion','product_vends','mydate','month_end','quarter_end']
export_cols_stata=['vvs_id','pos_id','Elapsed','product_vends','week_of_year','ExpMachine','balanced','mydate','exclusion']
export_cols_matlab=['vvs_id','Elapsed','percent_depleted','product_vends','average_daily_sales','ExpMachine','rank_ads']

### Data out
f_csv_out =proc_dir / 'statetransitions.csv'
f_csv_out2 =proc_dir / 'statetransitions-iqr.csv'

# output 
f_tab_thrshold = tab_dir /'table2_threshold.tex'
f_summary = tab_dir /'table1_summary.tex'
f_ols = tab_dir /'table3_ols.tex'

fig_statesvars = fig_dir / 'statevars_mc15.pdf'
fig_statesvars_iqr = fig_dir / 'statevars_mc15_iqr.pdf'


# unused tables
f_tab_topprods = tab_dir /'top_prods.tex'
# figures
f_fig_mars_share = fig_dir / 'mars_share.pdf'


# read in data
prod=pd.read_parquet(f_prod)
df1=pd.read_parquet(f_vvs)
df2=pd.read_parquet(f_vvi,columns = ['vvs_id','new_pro_id','vended','dex_vended','par','capacity'])
dfn=pd.read_excel(f_national)

merged_df=pd.merge(pd.merge(df2, prod, on=['new_pro_id']), df1[keep_cols], on='vvs_id')

# Vends for manufacturers
merged_df['mars_vends'] = (merged_df.manuf_id=='Mars') * merged_df['vended']
merged_df['mars_confections'] = (merged_df.manuf_id=='Mars') * (merged_df.cat.isin(['Chocolate','NonChocolate']))*merged_df['vended']
merged_df['hershey_vends'] = (merged_df.manuf_id=='Hershey') * merged_df['vended']
merged_df['nestle_vends'] = (merged_df.manuf_id=='Nestle') * merged_df['vended']

### Export Datasets
#- Write the Vends Per Visit data to csv for matlab
#- write the vends per visit and elapsed days to stata for regressions (Should redo in Python later)

## This is statetransions.csv for dynamic part
effort_df = df1[(df1.rank_vends > 0.75) & (df1.keep)].copy()
effort_iqr = df1[(df1.rank_vends > 0.5) & (df1.rank_vends <= 0.75) & (df1.keep)].copy()

effort_df[export_cols_matlab].to_csv(f_csv_out)
effort_iqr[export_cols_matlab].to_csv(f_csv_out2)


### Product Summaries
out_tex=summary_tex(merged_df, dfn, prod)
with open(f_summary, "w") as text_file:
    print(out_tex, file=text_file)

summs=pd.merge(dfn,pd.concat([summary_one(merged_df[~(merged_df.exclusion)],'all'),
                 summary_one(merged_df[(merged_df.exclusion)],'all_excl'),
                 summary_one(merged_df[(~merged_df.exclusion)&(merged_df.ExpMachine>0)],'exp'),
                 summary_one(merged_df[(merged_df.exclusion)&(merged_df.ExpMachine>0)],'exp_excl'),
                ],axis=1).fillna(0),on=['new_pro_id'])

y2=summs.drop(list(summs.filter(regex ='vend').columns)+['new_pro_id'],axis=1)
#y2.to_latex(f_summary,index=False,column_format='rlrrrrrr',header=['Rank','Product','National Avail','National Share','Share (NE-All)','Share (E-All)','Share (NE-Exp)','Share (E-Exp)'])
print(y2)


## Threshold Calculations
#1. Recover observed policy functions at different quantiles
#2. Compute YoY change in quarterly Mars sales
#3. Compute Mars and Overall Sales and Share

vends=df1[(df1.rank_vends>0.75)&(df1.keep)].groupby(['quarter_end'])[['product_vends']].mean().round(2)
elapsed=df1[(df1.keep)].groupby(['quarter_end'])[['Elapsed']].mean().round(2)

a=threshold_calc(merged_df)
b=threshold_calc(merged_df[merged_df.balanced])
c=threshold_calc(merged_df[merged_df.ExpMachine>0])


dft=a[['vended_index','mars_index','mars_conf_share','yoy']].round(2)
dft2=pd.concat([dft,pd.DataFrame(vends['product_vends']),elapsed],axis=1)
totals=pd.concat([dft2[dft2.index<='2007Q4'].mean(),dft2[dft2.index>'2007Q4'].mean()],axis=1).transpose()
totals.index=['Pre 2008 Avg','Post 2008 Avg']
dft3=pd.concat([dft2,totals],axis=0).round(2)

out_tex2=threshold_tex(dft3)
with open(f_tab_thrshold, "w") as text_file:
    print(out_tex2, file=text_file)
    
print("Low Threshold\n")
print(dft2[(dft2.index>'2007Q4')&(dft2.index<'2009Q1')].mean())
print("\nHigh Threshold \n")
print(dft2[(dft2.index<='2007Q4')].mean())
print("\n")

dft3



