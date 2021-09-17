import setup_descriptives
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from collections import defaultdict

from setup_descriptives import raw_dir, proc_dir

# category consolidation
d = defaultdict(lambda: 'Other')
d.update({16:'Mars',17:'Nestle',10:'Hershey'})

f_manuf = raw_dir / 'matched-manuf.csv'
f_total = raw_dir / 'matched-revenues.csv'
f_prod = raw_dir / 'product_data.parquet'

read_cols = ['vvs_id','new_pro_id','vended','dex_vended','par','capacity']
export_cols_matlab=['vvs_id','Elapsed','percent_depleted','product_vends','average_daily_sales','ExpMachine','rank_ads']

def filter_exp(df):
    df.loc[df.exp_id==4,'exp_id']=8
    return df[df.exp_id.isin([1,8,10])]

def diff_fields(df):
    df['diffp'] = df['Revenue1']-df['Revenue0']
    df['diffv']= df['Vends1']-df['Vends0']
    if 'Rebate0' in df.columns:
        df['diffr'] = df['Revenue1']-df['Revenue0'] + df['Rebate1']-df['Rebate0']
    return df

def t_stat(x):
    return (np.mean(x) / np.std(x)) * np.sqrt(len(x)-1)

def margins(df):
    x=df.groupby(['exp_id'])[['Vends0','Revenue0','Rebate0','Vends1','Revenue1','Rebate1']].sum()
    a=(x['Revenue1']/x['Vends1']-x['Revenue0']/x['Vends0'])
    b=(x['Rebate1']/x['Vends1']-x['Rebate0']/x['Vends0'])
    return 100*pd.DataFrame({'margin_wo':a,'margin_reb':a+b})

def consolidate_manuf(df):
    df['manuf_id']=df['manuf_id'].map(d)
    return df

# read in data
df1 = pd.read_csv(f_manuf).pipe(filter_exp).pipe(diff_fields).pipe(consolidate_manuf)

defaultdict = {16:'Mars',17:'Nestle',10:'Hershey'}
# do Table 4
df2 = pd.read_csv(f_total).pipe(filter_exp).pipe(diff_fields)
table4=pd.concat([df2.groupby(['exp_id']).agg(change=('diffv',np.mean),nobs=('diffv',np.size),profit=('diffp',np.mean),
    tstat=('diffp',t_stat),profitr=('diffr',np.mean),tstatr=('diffr',t_stat)),margins(df2)],axis=1)
table4['nobs']=table4.nobs.astype(int)
table4=table4[['change','nobs','margin_wo','profit','tstat','margin_reb','profitr','tstatr']].round(2)
table4.index = ['Snickers','Peanut M\&Ms','Snickers + Peanut M\&Ms']
print(table4)
table4.to_latex(header=False)


df_long=df1.groupby(['exp_id','manuf_id']).agg(change=('diffv',np.mean),nobs=('diffv',np.size),profit=('diffp',np.mean))
