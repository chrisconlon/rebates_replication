from scipy.io import loadmat, whosmat
import numpy as np
import pandas as pd
from toolz import interleave
import matplotlib.pyplot as plt

# titles
titleHM='(H,M) Assortment: Reeses Peanut Butter Cup and Three Musketeers'
titleHH='(H,H) Assortment: Reeses Peanut Butter Cup and Payday'
titleMM='(M,M) Assortment: Three Musketeers and Milkyway'

# For the main table
short_cols=['policy_str','retail','rebate','Mars','Hershey','Nestle','Integrated','Industry','Consumer2']
short_labels=['Policy','$\pi^R$','$\lambda \pi^M$','$\pi^M$','$\pi^H$','$\pi^N$','$\pi^R+\pi^M$','PS','CS']

efforts = ['NR','R','VI','IND','SOC','SOC1','SOC4']
efforts_exp = ['NR','R','VI','IND','SOC','SOC1','SOC4','Pre 2008','Post 2008',]
col_labels=['(H,H)','(H,M)','(M,M)']

# Read Columns
cols=['policy','retail','rebate','Mars','Hershey','Nestle','Integrated','Industry','Consumer2','Social2']

### Shared Functions
num_format = lambda x: '{:,}'.format(x)

def write_tex_table(f_out,tex):
    with open(f_out, "w") as text_file:
        print(tex, file=text_file)
    return

def build_formatters(df, format):
        return {column:format for (column, dtype) in df.dtypes.iteritems() if dtype in [np.dtype('int64'),np.dtype('int32'), np.dtype('float64')]}

def policy_string(df):
    return '$e^{' + df['which_kind'] +'}('+ df.policy.astype(str) +')$'


def se_format(x,digits=2):
    if isinstance(x, str):
        return '[' + x + ']'
    else:
        return '[' + str(np.round(x,digits)) + ']'

def combine_se(y1,y2,row_labels):
    z=pd.DataFrame(interleave([y1.values,y2.applymap(se_format).values]))
    z.index=sum([[i, ''] for i in row_labels], [])
    return z

### End shared functions

def process_main(fn,t_name='my_table_mle'):
    x=loadmat(fn,squeeze_me=True,struct_as_record=False)[t_name]
    df=pd.DataFrame(np.round(x).astype(int),columns=cols)
    df['which_kind']=efforts_exp*3
    df['policy_str']=policy_string(df)
    n_rows=int(df.shape[0]/3)
    df['assortment']=np.array(['(H,M)'] * n_rows + ['(H,H)'] * n_rows + ['(M,M)'] * n_rows)
    return df

def compress_table(df):
    df2=df.reset_index()
    df2['policy_str']=policy_string(df2)
    if any(['R' in df2.index]):
        df2=df2[df2.which_kind.isin(['NR', 'R', 'VI', 'IND', 'SOC2'])]
    df2=df2.loc[:, short_cols].copy()
    df2.columns=[short_labels]
    return df2

def compress_table2(df):
    df2=df.reset_index()
    df2['policy_str']=policy_string(df2)
    df2=df2[df2.which_kind.isin(['NR', 'R', 'VI', 'IND', 'SOC','Pre 2008','Post 2008'])]
    df2=df2.loc[:, short_cols].copy()
    df2.columns=[short_labels]
    return df2

def main_table(stacked_tables,cut=[4,13,23]):
    formatters = build_formatters(stacked_tables, num_format)
    latex=stacked_tables.to_latex(escape=False,index=False,column_format='l| cc ccc ccc',formatters=formatters)
    latex_list=latex.splitlines()
    ncols=stacked_tables.shape[1]
    
    dividerHM=[' \multicolumn{'+str(ncols)+'}{c}{'+titleHM+'}\\\ ','\midrule']
    dividerHH=['\midrule','  \multicolumn{'+str(ncols)+'}{c}{'+titleHH+'}\\\ ','\midrule']
    dividerMM=['\midrule','  \multicolumn{'+str(ncols)+'}{c}{'+titleMM+'}\\\ ','\midrule']

    latex_list[cut[0]:cut[0]]=dividerHM
    latex_list[cut[1]:cut[1]]=dividerHH
    latex_list[cut[2]:cut[2]]=dividerMM

    latex_new = '\n'.join(latex_list)
    print(latex_new)
    print('\n'*2)
    return latex_new

def main_table2(stacked_tables,cut=[4,13,23]):
    stacked_tables = stacked_tables.drop(['$\lambda \pi^M$','$\pi^M$','$\pi^H$','$\pi^N$'], axis=1)
    print(stacked_tables)
    formatters = build_formatters(stacked_tables, num_format)
    latex=stacked_tables.to_latex(escape=False,index=False,column_format='l| c ccc',formatters=formatters)
    latex_list=latex.splitlines()
    ncols=stacked_tables.shape[1]
    
    dividerHM=[' \multicolumn{'+str(ncols)+'}{c}{'+titleHM+'}\\\ ','\midrule']
    dividerHH=['\midrule','  \multicolumn{'+str(ncols)+'}{c}{'+titleHH+'}\\\ ','\midrule']
    dividerMM=['\midrule','  \multicolumn{'+str(ncols)+'}{c}{'+titleMM+'}\\\ ','\midrule']

    latex_list[cut[0]:cut[0]]=dividerHM
    latex_list[cut[1]:cut[1]]=dividerHH
    latex_list[cut[2]:cut[2]]=dividerMM

    latex_new = '\n'.join(latex_list)
    print(latex_new)
    print('\n'*2)
    return latex_new


def process_table9(fn,is_se=False):
    if is_se:
        table_id='table9'
        y=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['table9'],axis=2),2))
    else:
        table_id='table9_mle'
        y=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)[table_id])).astype(int)
    
    y.index=['retail','Mars','Hershey','Nestle','PS','CS','SS','Observed']
    y.loc['Bilateral']=y.loc['retail'] +y.loc['Mars'] 
    y.loc['Rational']=np.abs(y.loc['retail']).astype(str)+'-'+y.loc['Mars'].astype(str)
    y=y.loc[['retail','Mars','Bilateral','Hershey','PS','CS','SS','Rational','Observed']]
    return y

def effort_table(fn,mylabels=['(M,H)','(H,H)','(M,M)']):
    x=pd.DataFrame(loadmat(fn,squeeze_me=True,struct_as_record=False)['policy_table_mle'],columns=mylabels)
    x=pd.concat([x,(100*((x.loc[0].values-x)/x.loc[0].values)).round(2)],axis=1)
    x['which_kind'] = efforts
    x.index = '$e^{' + x.which_kind +'}$'
    x.index.name=''
    x=x.drop(columns='which_kind')
    latex_out=x.to_latex(header=True,escape=False,column_format='l| ccc| ccc')
    latex_list=latex_out.splitlines()
    latex_list[3:3] = ['& \multicolumn{3}{c}{Effort Policy} & \multicolumn{3}{c}{\% Change from $e^{NR}$} \\\\ \n']
    del latex_list[4:5] 
    return '\n'.join(latex_list)

def table9_part1(df2):
    x=df2[['policy','retail','rebate','Mars','Hershey','Integrated','Industry']].reset_index(drop=True).transpose().sort_values(by='Hershey',axis=1,ascending=False)
    x.index=['$e^R$','$\pi^R$','$\lambda  \pi^M$','$\pi^M$','$ \pi^H$','$ \pi^R +  \pi^M$','$\pi^R +  \pi^M+ \pi^H$']
    x.columns=col_labels
    return x

def table9_part2(fn,include_se=True):
    y1=process_table9(fn,is_se=False)
    if include_se:
        y2=process_table9(fn,is_se=True)
        row_labels=['$\Delta \pi^R$','$\Delta \pi^M$','$\Delta \pi^R+\Delta \pi^M$','$\Delta \pi^H$','$\Delta PS$','$\Delta CS$','$\Delta SS$','Rational','Observed']
        y1=combine_se(y1,y2,row_labels)
    header=pd.DataFrame({'from':['(H,H)','(H,M)','(H,H)'],'to':['(H,M)','(M,M)','(M,M)']}).transpose()
    z=pd.concat([header,y1])
    return z

def table9_both(fn,include_se=True):
    # first part
    df=process_main(fn)
    part1=table9_part1(df[df.which_kind=='R'])
    old_cols=part1.columns
    part1.columns=[0,1,2]

    # add second part and fix columns
    df2=pd.concat([part1,table9_part2(fn,include_se)],axis=0)
    df2.columns=old_cols
    
    latex_y=df2.to_latex(escape=False,header=True,column_format='l ccc')
    dividerR=['\midrule & \multicolumn{3}{c}{Rebates}\\\ ','\midrule']

    if include_se:
        (a,b,c) = (-6,11,14)
    else:
        (a,b,c) = (-4,11,14)
    
    latex_list=latex_y.splitlines()
    latex_list[a:a]=dividerR
    latex_list[b:b]=['\midrule']
    latex_list[c:c]=['\midrule']
    return '\n'.join(latex_list)

def calc_eff_same(policy):
    base=policy[0,]
    target=policy[2,]
    target2=policy[-1,]
    return 100.*np.vstack([(base-target)/base,(base-target2)/base])

def eff_table(fn):
    x=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['efficiency_mle'])).astype(int)
    x.index=['retailer','Mars','Hershey','Nestle','PS','CS','SS','rebate']
    x=x.loc[['retailer','Mars','Hershey','PS','CS','SS']]

    y=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['efficiency'],axis=2),2))
    y.index=['retailer','Mars','Hershey','Nestle','PS','CS','SS','rebate']
    y=y.loc[['retailer','Mars','Hershey','PS','CS','SS']]
    
    row_labels=['$\Delta \pi^R$','$\Delta \pi^M$','$\Delta \pi^H$','$\Delta PS$','$\Delta CS$','$\Delta SS$']

    policy_1=np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['policy_table_mle'])
    policy_2=loadmat(fn,squeeze_me=True,struct_as_record=False)['policy_table']
    
    y1=pd.DataFrame(calc_eff_same(policy_1).reshape([6])).transpose().round(2)
    y2=pd.DataFrame(np.std(calc_eff_same(policy_2),1)).transpose().round(2)
    
    # put together pieces
    top_df=combine_se(y1,y2,['$\% \Delta(e^{NR},e^{Opt})$'])
    out_df=pd.concat([top_df,combine_se(x,y,row_labels)])
    out_df.columns=col_labels*2
    
    # clean the latex
    latex_out=out_df.to_latex(header=True,escape=False,column_format='l| ccc| ccc')
    latex_list=latex_out.splitlines()
    latex_list[2:2]=['& \multicolumn{3}{c}{Vertically Integrated} & \multicolumn{3}{c}{Socially Optimal} \\\  \n ']
    output='\n'.join(latex_list)

    return output

def net_effects(fn,include_se=True):
    # Main Table
    x=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['net_effect_mle'])).astype(int)
    x2=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['net_effect'],2),2))

    # Cutoff price
    y=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['cutoff_price_mle'],2))
    y2=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['cutoff_price'],1),2))

    # Reduced Lambda
    z=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['reduced_lambda_mle'],2))
    z2=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['reduced_lambda'],1),2))

    # stack up the cutoff and reduced lambda
    extra=pd.concat([y.transpose(),z.transpose()])
    extra_se=pd.concat([y2.transpose(),z2.transpose()])
    extra_labels=['$w_h$ to avoid foreclosure','Reduced $\lambda$ (Percent)']
    if include_se:
        extra_df=combine_se(extra,extra_se,extra_labels)
    else:
        extra_df=extra
        extra_df.index=extra_labels

    # label and put together
    net_row_labels=['$\Delta \pi^R$','$\Delta \pi^M$','$\Delta \pi^H$','$\Delta \pi^N$',
            '$\Delta PS$','$\Delta CS(\epsilon=-2)$', '$\Delta SS$','$\lambda  \pi^M$']
    if include_se:
        out_df=pd.concat([combine_se(x,x2,net_row_labels),extra_df])
    else:
        out_df = x.astype(object)
        out_df.index = net_row_labels
        out_df =pd.concat([out_df,extra_df.astype(object)])
    out_df.columns=['$e^{R}$','$e^{VI}$','$e^{SOC}$']*2

    # clean the latex
#    latex=out_df.to_latex(escape=False,column_format='l|ccc| ccc')
    latex=out_df.to_latex(escape=False,column_format='l|ccc| cccc')
    latex_list=latex.splitlines()
    latex_list[2:2]=['from & \multicolumn{3}{c|}{(H,M) and $e^{NR}$} & \multicolumn{3}{c}{(H,H) and $e^{NR}$} \\\  \n ']
    latex_list[-8:-8]=['\midrule']
    output='\n'.join(latex_list)
    return output

def ref_table(fn,include_se=True):
    # main table
    x=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['ref_table_mle'])).astype(int)
    x2=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['ref_table'],2),2))

    # label and put together
    net_row_labels=['$\Delta \pi^R$','$\Delta \pi^M$','$\Delta \pi^H$','$\Delta \pi^N$',
            '$\Delta PS$','$\Delta CS(\epsilon=-2)$', '$\Delta SS$','$\lambda  \pi^M$']
    if include_se:
        out_df=combine_se(x,x2,net_row_labels)
    else:
        out_df = x.astype(object)
    out_df.columns=['No Rebate','Vertical Integration','Industry Optimal','Social Optimum ($\epsilon=-2$)']
    #out_df.columns=['No Rebate','Vertical Integration','Observed','Industry Optimal','Social Optimum ($\epsilon=-2$)']

    # clean the latex
    latex=out_df.to_latex(escape=False,column_format='lccccc')
    latex_list=latex.splitlines()
#    latex_list[3:3]=['Effort & $e^{NR}:212$ & $e^{VI}:195$ & $e^{IND}:197$ & $e^{SOC}:172$ \\\\' ]
#    latex_list[3:3]=['Assortment & (H,H) & (M,M) & (H,M) & (H,M) \\\\' ]
    latex_list[3:3]=['Effort & $e^{NR}:212$ & $e^{VI}:195$  & $e^{IND}:197$ & $e^{SOC}:172$ \\\\' ]
    latex_list[3:3]=['Assortment & (H,H) & (M,M) & (H,M) & (H,M) \\\\' ]
    
    # Drop the Rebate
    latex_list[-4:-2]=['' ]    
    output='\n'.join(latex_list)
    return output

def obs_table(fn,include_se=True):
    x=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['observed_mle'])).astype(int)
    x2=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['observed_table'],2),2))

    # label and put together
    net_row_labels=['$\Delta \pi^R$','$\Delta \pi^M$','$\Delta \pi^H$','$\Delta \pi^N$',
            '$\Delta PS$','$\Delta CS(\epsilon=-2)$', '$\Delta SS$','$\lambda  \pi^M$']
    if include_se:
        out_df=combine_se(x,x2,net_row_labels)
    else:
        out_df = x.astype(object)


    # clean the latex
    latex=out_df.to_latex(escape=False,column_format='l | cc | ccc',header=False)
    latex_list=latex.splitlines()
    latex_list[2:2]=['Assortment & (H,H) & (H,M) & (M,M) & (H,H) & (H,M) \\\\ \\midrule' ]
    latex_list[2:2]=[' & \\multicolumn{2}{c}{Effort $= 137$}&\\multicolumn{3}{c}{Effort $= 144$} \\\\ ']
    
    output='\n'.join(latex_list)
    return output

def merger_table(fn):
    x=np.round(pd.DataFrame(loadmat(fn,squeeze_me=True,struct_as_record=False)['merger_table_mle']),2)
    xA=np.round(x.iloc[0:6],0).astype(int)
    xB=np.round(x.iloc[6:],2)

    x2=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['merger_table'],2),2))
    xA2=np.round(x2.iloc[0:6],2)
    xB2=np.round(x2.iloc[6:],2)

    part1=combine_se(xA,xA2,['$\Delta \pi^R$','$\Delta \pi^M$','$\Delta \pi^{Rival}$','Rebate',
            '$\Delta PS$','$\Delta CS(\epsilon=-2)$'])
    part2=combine_se(xB,xB2,['Price to Avoid Foreclosure','\% Reduction in Rebate $c=0.15$'])

    out_df=pd.concat([part1,part2])

    header1='AUD Assortment &$e^{VI}(M,M)$ & $e^{VI}(H,M)$ & $e^{VI}(M,M)$ & $e^{VI}(M,M)$ \\\\ '
    header2='Alternative &$e^{NR}(H,H)$ & $e^{NR}(N,N)$ & $e^{NR}(H,H)$ & $e^{NR}(H,H)$ \\\\'

    # clean the latex
    latex_out=out_df.to_latex(header=True,escape=False,column_format='l| cccc')
    latex_list=latex_out.splitlines()
    latex_list[2:2]=[header1]
    latex_list[3:3]=[header2]
    latex_list[-6:-6]=['\midrule']
    latex_list[4:5]=['']
    
    output='\n'.join(latex_list)
    return output



def net_effects2(fn,include_se=True):
    # Main Table
    x=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['net_effect_mle'])).astype(int)
    x2=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['net_effect'],2),2))

    # Cutoff price
    y=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['cutoff_price_mle'],2))
    y2=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['cutoff_price'],1),2))

    # Reduced Lambda
    z=pd.DataFrame(np.round(loadmat(fn,squeeze_me=True,struct_as_record=False)['reduced_lambda_mle'],2))
    z2=pd.DataFrame(np.round(np.std(loadmat(fn,squeeze_me=True,struct_as_record=False)['reduced_lambda'],1),2))

    # stack up the cutoff and reduced lambda
    extra=pd.concat([y.transpose(),z.transpose()])
    extra_se=pd.concat([y2.transpose(),z2.transpose()])
    extra_labels=['$w_h$ to avoid foreclosure','Reduced $\lambda$ (Percent)']
    if include_se:
        extra_df=combine_se(extra,extra_se,extra_labels)
    else:
        extra_df=extra
        extra_df.index=extra_labels

    # label and put together
    net_row_labels=['$\Delta \pi^R$','$\Delta \pi^M$','$\Delta \pi^H$','$\Delta \pi^N$',
            '$\Delta PS$','$\Delta CS(\epsilon=-2)$', '$\Delta SS$','$\lambda  \pi^M$']
    if include_se:
        out_df=pd.concat([combine_se(x,x2,net_row_labels),extra_df])
    else:
        out_df = x.astype(object)
        out_df.index = net_row_labels
        out_df =pd.concat([out_df,extra_df.astype(object)])
    #out_df = out_df.iloc[:, :-1]
    out_df.columns = ['$e^{R}$','$e^{VI}$','$e^{SOC}$','$e^{R}$','$e^{VI}$','$e^{SOC}$']
    
    # clean the latex
#    latex=out_df.to_latex(escape=False,column_format='l|ccc| ccc')
    latex=out_df.to_latex(escape=False,column_format='l|ccc| cccc')
    latex_list=latex.splitlines()
    #latex_list[2:2]=['from & \multicolumn{3}{c|}{(H,M) and $e^{NR}$} & \multicolumn{3}{c}{(H,H) and $e^{NR}$} \\\  \n ']
    latex_list[2:2]=['from & \multicolumn{3}{c|}{(H,H) and $e^{NR}$} & \multicolumn{3}{c}{(H,M) and $e^{NR}$} \\\  \n ']
    latex_list[-13:-13]=['\midrule']
    output='\n'.join(latex_list)
    return output

#### For plots and thresholds
# print_thresholds.py

def flow_profit_plot(fn2):
    x=loadmat(fn2,squeeze_me=True,struct_as_record=False)['payoffs']
    tmp=pd.DataFrame({'Mars / 10':x.mars/10,'Hershey':x.hershey,'Nestle':x.nestle,'Retailer':x.retail})
    fig, axes = plt.subplots(nrows=1, ncols=2,figsize=(20,10))
    tmp[['Mars / 10','Hershey','Nestle']].plot(ax=axes[0],color=['black','black','black'],style=['-','-.','--'])
    tmp[['Retailer']].plot(ax=axes[1],color=['black'])
    axes[0].set_ylabel('Profit Per Consumer')
    axes[0].set_xlabel('# of Consumers')
    axes[1].set_xlabel('# of Consumers')
    return fig
    
    

def read_one(fn,assortment,minval=120,maxval=300):
    x=loadmat(fn,squeeze_me=True,struct_as_record=False)[assortment]
    mars=x.Mars[minval:maxval]
    retail=x.Retail[minval:maxval]
    retailR=x.RetailR[minval:maxval]

    return(mars,retail,retailR)


def print_thresholds(fn):
    (marsHH,retailHH,retailHH_r)=read_one(fn,'profitsHH',minval=10)
    (marsHM,retailHM,retailHM_r)=read_one(fn,'profitsHM',minval=10)
    (marsMM,retailMM,retailMM_r)=read_one(fn,'profitsMM',minval=10)

    MM_max=max(retailMM_r)
    HM_max=max(retailHM_r)
    HH_max=max(retailHH_r)
    HH_ub=max(retailHH)

    MM_top=marsMM[np.argmax(retailMM_r)]
    HM_top=marsHM[np.argmax(retailHM_r)]
    HH_top=marsHH[np.argmax(retailHH_r)]

    MM_cutoff=max(marsHM[retailHM_r > max(retailMM_r)])
    HM_cutoff=max(marsHH[retailHH_r > max(retailHM_r)])
    HH_cutoff=max(marsMM[retailMM_r > max(retailHH)])

    print("Top of HH: \t\t", HH_top.round().astype(int))
    print("Threshold for HM:\t", HM_cutoff.round().astype(int))
    print("Top of HM: \t\t", HM_top.round().astype(int))
    print("Threshold for MM:\t", MM_cutoff.round().astype(int))
    print("Top of MM: \t\t", MM_top.round().astype(int))
    print("Threshold Giving Up:\t",HH_cutoff.round().astype(int) )

    return

def give_thresholds(fn):
    (marsHH,retailHH,retailHH_r)=read_one(fn,'profitsHH',minval=10)
    (marsHM,retailHM,retailHM_r)=read_one(fn,'profitsHM',minval=10)
    (marsMM,retailMM,retailMM_r)=read_one(fn,'profitsMM',minval=10)

    MM_max=max(retailMM_r)
    HM_max=max(retailHM_r)
    HH_max=max(retailHH_r)
    HH_ub=max(retailHH)

    MM_top=marsMM[np.argmax(retailMM_r)]
    HM_top=marsHM[np.argmax(retailHM_r)]
    HH_top=marsHH[np.argmax(retailHH_r)]

    MM_cutoff=max(marsHM[retailHM_r > max(retailMM_r)])
    HM_cutoff=max(marsHH[retailHH_r > max(retailHM_r)])
    HH_cutoff=max(marsMM[retailMM_r > max(retailHH)])

    threshold = [HH_top.round().astype(int), HM_cutoff.round().astype(int), HM_top.round().astype(int), MM_cutoff.round().astype(int), MM_top.round().astype(int),HH_cutoff.round().astype(int)]
    return threshold

def threshold_check(out_df,include_se=True):
    out_df.columns=['$\\bar{\\pi_{M}^{MIN}}$','$\\bar{\\pi}_{M}^{MAX}$','$\\text{Assortment}$','$\text{Effort}$']
    formatters = build_formatters(out_df, num_format)
    output=out_df.to_latex(escape=False,column_format='cccc',index = False,formatters=formatters)
    print(output)
    return output

    
