import setup_descriptives
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from setup_descriptives import raw_dir, proc_dir

f_vvs = raw_dir / 'vv_snacks.parquet'
f_vvi = raw_dir / 'vvi_all.parquet'
f_prod = raw_dir / 'product_data.parquet'

read_cols = ['vvs_id','new_pro_id','vended','dex_vended','par','capacity']
export_cols_matlab=['vvs_id','Elapsed','percent_depleted','product_vends','average_daily_sales','ExpMachine','rank_ads']

### Data out
f_merged = proc_dir / 'merged_data.parquet'
f_csv_out = proc_dir / 'statetransitions.csv'
f_csv_out2 = proc_dir / 'statetransitions-iqr.csv'

# read in data
prod = pd.read_parquet(f_prod)
df1 = pd.read_parquet(f_vvs)
df2 = pd.read_parquet(f_vvi, columns = read_cols)

# combine the product and sales info
def merge_datasets(df1, df2, prod):
    keep_cols=['vvs_id','pos_id','Elapsed','ExpMachine','week_of_year','keep','balanced',
                'exclusion','product_vends','mydate','month_end','quarter_end']
    merged_df=pd.merge(pd.merge(df2, prod, on=['new_pro_id']), df1[keep_cols], on='vvs_id')

    # Vends for manufacturers
    merged_df['mars_vends'] = (merged_df.manuf_id=='Mars') * merged_df['vended']
    merged_df['mars_confections'] = (merged_df.manuf_id=='Mars') * (merged_df.cat.isin(['Chocolate','NonChocolate']))*merged_df['vended']
    merged_df['hershey_vends'] = (merged_df.manuf_id=='Hershey') * merged_df['vended']
    merged_df['nestle_vends'] = (merged_df.manuf_id=='Nestle') * merged_df['vended']
    return merged_df

# combine the product and sales info and save
merged_df  = merge_datasets(df1, df2, prod)
merged_df.to_parquet(f_merged, compression='brotli')

### Export Datasets
#- Write the Vends Per Visit data to csv for matlab
#- write the vends per visit and elapsed days to stata for regressions (Should redo in Python later)

## This is statetransions.csv for dynamic part
effort_df = df1[(df1.rank_vends > 0.75) & (df1.keep)].copy()
effort_iqr = df1[(df1.rank_vends > 0.5) & (df1.rank_vends <= 0.75) & (df1.keep)].copy()

effort_df[export_cols_matlab].to_csv(f_csv_out)
effort_iqr[export_cols_matlab].to_csv(f_csv_out2)

