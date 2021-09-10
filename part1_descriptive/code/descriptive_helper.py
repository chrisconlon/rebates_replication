import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

t_date= pd.to_datetime('2008-01-01')


def weighted(x, cols, w="product_vends"):
             return pd.Series(np.average(x[cols], weights=x[w], axis=0), cols)

###
# These are for the summaries
###
def summary_one(x,stub='tot'):
    x=x[x.keep].copy()
    total=x[x.cat.isin(['Chocolate','NonChocolate'])]['vended'].sum()
    x2=x[x.manuf_id.isin(['Hershey','Nestle','Mars'])].groupby(['new_pro_id'],observed=True)[['vended']].sum()
    x2['share']=(100*x2['vended']/total).round(1)
    x2=x2.sort_values('share',ascending=False)
    x2.columns=[stub+'_vend', stub+'_share']
    return x2

def threshold_calc(df):
    tmp=df.groupby(['quarter_end'])[['vended','mars_confections']].sum()
    tmp.iloc[-1,:]=13/7.5*tmp.iloc[-1,:]
    tmp[['mars_confections','vended']]=tmp[['mars_confections','vended']].astype(int)
    tmp[['mars_index','vended_index']]=tmp[['mars_confections','vended']]/tmp[['mars_confections','vended']].iloc[0]
    tmp['mars_index']=tmp['mars_index']*19.80
    tmp['vended_index']=tmp['vended_index']*100
    tmp[['mars_conf_share']]=100.0*tmp[['mars_confections']].div(tmp['vended'],axis=0)
    tmp['lagged']=tmp['mars_confections'].shift(4)
    tmp['yoy'] = tmp['mars_confections']/tmp['lagged']
    return tmp

def summary_tex(merged_df,dfn,prod):
    summs=pd.merge(pd.merge(dfn,prod[['new_pro_id','manuf_id']],on='new_pro_id'),
    pd.concat([ summary_one(merged_df[(merged_df.exclusion)],'Pre'),
                 summary_one(merged_df[~(merged_df.exclusion)],'Post')]
              ,axis=1).fillna(0),
    on='new_pro_id'
    )
    summs['Product']=summs['productname'].astype(str) + ' (' + summs['manuf_id'].astype(str) +')'

    y1=summs[['Product','Rank','Avail','Share','Pre_share','Post_share']]
    latex_list=y1.to_latex(index=False,column_format='l c c c | c c',header=['Product','Rank','Availability %','Share','Pre 2008','Post 2008']).splitlines()

    extra_line=' & \multicolumn{3}{c|}{National Sample} & \multicolumn{2}{c}{MarkVend Share}\\\\'
    latex_list[2:2] = [extra_line]
    return '\n'.join(latex_list)

def threshold_tex(dft2):
    dft2.index.name=''
    dft2.columns=['Overall Sales','Mars Sales','Mars Share','Mars YoY','Vends Per Visit','Days Per Visit']
    latex_list=dft2.to_latex(na_rep='',column_format='l c c c c | c c', header=['Sales','Sales','Share','YoY Sales','Vends/Visit','Days/Visit']).splitlines()
    del latex_list[3:4]
    extra_line=' & Overall &  \multicolumn{3}{c|}{Mars} &\multicolumn{2}{c}{Retailer Effort} \\\\'
    latex_list[2:2] = [extra_line]
    return '\n'.join(latex_list)


def threshold_reg_tex(res1,res2):
    ols_string='''
    \\begin{tabular}{l|cc} 
    \\toprule
    & Elapsed Days Per Visit & Vends Per Visit \\\\
    \\midrule
    Lower Threshold & [b1]*** & [b2]*** \\\\
     & ([b1se]) & ([b2se]) \\\\
    \\midrule
    Observations & [n] & [n] \\\\
    R-squared & [rsq1] & [rsq2] \\\\
    Machine FE &  \checkmark &  \checkmark \\\\
     Week of Year FE &  \checkmark &  \checkmark \\\\
    \\bottomrule
    \multicolumn{3}{c}{ Standard errors in parentheses:  *** p$<$0.01 } \\\\
    \end{tabular}
    '''

    n=int(res1.nobs)
    out_str=ols_string.replace('[b1]',str(res1.params['exclusion'].round(3))).replace('[b2]',str(res2.params['exclusion'].round(3))).\
        replace('[b1se]',str(res1.bse['exclusion'].round(4))).replace('[b2se]',str(res2.bse['exclusion'].round(4))).\
        replace('[rsq1]',str(res1.rsquared.round(4))).replace('[rsq2]',str(res2.rsquared.round(4))).replace('[n]',str(n))
    
    print(out_str)
    return out_str

# First argument is e^R second is e^Visit
def plot_statevars(df,a,b):
    print("Restock After " + str(np.mean(df['product_vends'])) +' Consumers\n' )
    fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(20,10))
    axes[0].hist(df['average_daily_sales'],bins=50,density=True,color='gray')
    axes[0].set_xlabel('Daily Arrival Rate')
    axes[1].hist(df['product_vends'],bins=50,density=True,color='gray')
    axes[1].set_xlabel('Cumulative Sales at Restocking')
    
    axes[1].axvline(x=a,color='black',linestyle='--')
    plt.text(a-35,.0068,'$e^{VI}$', size=24)
    
    axes[1].axvline(x=b,color='black',linestyle='-.')
    plt.text(b+1,.0065,'$e^{R}$', size=24)
    return


###
# These are for the facings
###


def merge_df(df1,facings):
    big_df=pd.merge(df1,facings,on=['vvs_id'])
    big_df['Hershey']=big_df[['Chocolate|Hershey','NonChocolate|Hershey']].sum(axis=1)
    big_df['Mars']=big_df[['Chocolate|Mars','NonChocolate|Mars']].sum(axis=1)
    big_df['Nestle']=big_df[['Chocolate|Nestle','NonChocolate|Nestle']].sum(axis=1)
    big_df['Skittles/Starburst']=big_df[['Skittles','Starburst']].sum(axis=1)
    return big_df

def compute_facings(df2,prod,sales_cutoff=4e4):
    x=pd.merge(df2[['vvs_id','new_pro_id','vended','dex_vended','par','capacity']],prod,on=['new_pro_id'])
    x['manuf_cat']=x['cat'].astype(str)+'|'+x['manuf_id'].astype(str)
    x1=x.groupby(['vvs_id','cat']).count()['vended'].unstack().fillna(0)
    x1.columns = x1.columns.tolist()
    x2=x.groupby(['vvs_id','manuf_cat']).count()['vended'].unstack().fillna(0)

    top_list=x[x.manuf_id.isin(['Hershey','Nestle','Mars'])].groupby(['productname','new_pro_id','manuf_id'],observed=True)['vended'].sum().sort_values(ascending=False).reset_index()
    print(top_list[top_list.vended> sales_cutoff])
    x3=x[x.new_pro_id.isin(top_list[top_list.vended> sales_cutoff].new_pro_id)].groupby(['vvs_id','productname']).count()['vended'].unstack().fillna(0)

    return pd.merge(pd.merge(x1,x2,on='vvs_id'),x3,on='vvs_id',how='left').fillna(0)


## And the plots
def plot_categories(df,use_weights=False):
    prod_list=['Chocolate|Mars','Chocolate|Hershey','Chocolate|Nestle','NonChocolate|Mars','NonChocolate|Hershey']

    if use_weights:
        x=df.groupby(['month_end']).apply(weighted, prod_list)
    else:
        x=df.groupby(['month_end'])[prod_list].mean()

    ax=x.plot(figsize=(15,10),color=['navy','maroon','green'],style=['-','-','-','-.','-.'])
    ax.axvline(x=t_date, ymin=0, ymax=4, color='gray',ls=':')
    plt.ylim(0,5.25)

    plt.xlabel('')
    plt.ylabel('Product Facings')

    #plt.annotate('Threshold Change', xy=(t_date, 3), xycoords='data',
    #             xytext=('2007-10-01', 2.5), textcoords='data',
    #             arrowprops=dict(facecolor='black', shrink=0.05),
    #             horizontalalignment='right', verticalalignment='center',
    #             )
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncol=2)
    
def plot_overall(df):
    ax=df[df.balanced].groupby(['month_end'])[['Chocolate','NonChocolate']].mean()[['Chocolate','NonChocolate']].plot(figsize=(20,10),color=['navy', 'maroon'],style=['-'])
    df[df.ExpMachine>0].groupby(['month_end'])[['Chocolate','NonChocolate']].mean()[['Chocolate','NonChocolate']].plot(ax=ax,color=['navy', 'maroon'],style=['-.','-.'])
    plt.xlabel('')
    plt.ylabel('Product Facings')

    ax.axvline(x=t_date, ymin=0, ymax=4, color='gray',ls=':')
    #plt.annotate('Threshold Change', xy=(t_date, 5), xycoords='data',
    #             xytext=('2007-10-01', 3.5), textcoords='data',
    #             arrowprops=dict(facecolor='black', shrink=0.05),
    #             horizontalalignment='right', verticalalignment='center',
    #             )
    plt.legend(['Chocolate (Balanced Panel)','Non-Chocolate (Balanced Panel)','Chocolate (Experimental Sample)','Non-Chocolate (Experimental Sample)'],loc='upper center', bbox_to_anchor=(0.5, -0.1),ncol=2)

def plot_facings(df,use_weights=False):
    prod_list=['M&M','Milky Way','3-Musketeers','Reeses PB Cup','Payday','Raisinets','Butterfinger']
    color_list=['navy', 'navy','navy','maroon','maroon','green','green']
    style_list=['-','-.','--','-','-.','-','-.']
    
    if use_weights:
        x=df.groupby(['month_end']).apply(weighted, prod_list)
    else:
        x=df.groupby(['month_end']).mean()[prod_list]
    
    ax=x.plot(figsize=(20,10),color=color_list,style=style_list)
    plt.xlabel('')
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),ncol=3)
    ax.axvline(x=t_date, ymin=0, ymax=1, color='gray',ls=':')
    plt.annotate('Exclusionary Period (M,M)', xy=('2007-6-01', 0.95), xycoords='data',
                 horizontalalignment='center', verticalalignment='center',
                 )

    plt.annotate('Non-Exclusionary Period (H,M)', xy=('2008-06-01', 0.95), xycoords='data',
                 horizontalalignment='center', verticalalignment='center',
             )

    t=pd.date_range('06-30-2006', t_date+pd.tseries.offsets.DateOffset(months=1), freq='M').to_pydatetime()
    plt.fill_between(t, 0, 1, facecolor='yellow', alpha=0.15, interpolate=True)

    t=pd.date_range(t_date, '02-28-2009', freq='M').to_pydatetime()
    plt.fill_between(t, 0, 1, facecolor='orange', alpha=0.15, interpolate=True)

