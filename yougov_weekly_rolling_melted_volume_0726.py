
# coding: utf-8

# In[65]:


import pandas as pd
import numpy as np

def brandEquity_weekly(file_name, output_filename):
    
    #Output dataframe
    df_score = pd.DataFrame()
    df_score_pivot = pd.DataFrame()
    
    #Metrics label
    xls = pd.ExcelFile(file_name, on_demand = True)
    equity_metrics = xls.sheet_names[1:]
    
    #looping through each tab
    for i, n in enumerate(equity_metrics):
        df = pd.read_excel(file_name, sheet_name=i+1, header=None)
        
        #drop non-neccessary rows
        df = df.drop([2,3,4], axis=0)

        #replace zero to nan
        df.iloc[0:4,:].replace(0, np.nan, inplace=True)

        #fill nan with proper headers
        df.iloc[0:4,:].ffill(axis=1, inplace=True)
        
        #filter 'Score', 'Volume' and 'Attention' columns
        col = [0]
        for e, k in enumerate(df.iloc[3,:]):
            if k == 'Score':
                col.append(e)
            elif k == 'Attention':
                col.append(e)
            elif k == 'Volume':
                col.append(e)       
        df_col = df[col]


        #collecting labels
        reg = []
        for a in df_col.iloc[0]:
            reg.append(a)

        sec = []
        for b in df_col.iloc[1]:
            sec.append(b)

        brand = []
        for c in df_col.iloc[2]:
            brand.append(c)

        met = []
        for d in df_col.iloc[3]:
            met.append(d)

        label = []
        for e, f, g, h in zip(reg, sec, brand, met):
            label.append(str(e)+"_"+str(f)+"_"+str(g)+"_"+str(h))

        df_col_values = df_col.iloc[4:,]
        df_col_values.columns = label
    

        #filter Sunday records
        df_col_values_index = df_col_values.set_index(['Region_Sector_Brand_nan'])
        df_col_values_index = df_col_values_index[df_col_values_index.index.dayofweek == 6]
        df_col_values_index_reset = df_col_values_index.reset_index()
        df_col_values_index_reset.rename(columns={'Region_Sector_Brand_nan':'date'},inplace=True)

        #print(df_col_values_index_reset.head())

        #melting columns
        df_col_values_melt = pd.melt(df_col_values_index_reset, id_vars = ['date'], 
                                                 value_vars=label, var_name='label', value_name='value')
        
        df_col_values_melt['region'] = df_col_values_melt['label'].apply(lambda x: x.split('_')[0])
        df_col_values_melt['sector'] = df_col_values_melt['label'].apply(lambda x: x.split('_')[1])
        df_col_values_melt['brand'] = df_col_values_melt['label'].apply(lambda x: x.split('_')[2])
        df_col_values_melt['metric'] = df_col_values_melt['label'].apply(lambda x: x.split('_')[3])
        df_col_values_melt = df_col_values_melt[df_col_values_melt['label'] != 'Region_Sector_Brand_nan']
        df_col_values_melt = df_col_values_melt.drop(['label'], axis=1)
        df_col_values_melt['metric'].replace('Attention', 'Score', inplace=True)
        
        #pulling tab names to a new column, yougov_metric
        df_col_values_melt['yougov_metric'] = xls.sheet_names[i+1]
         
        df_score = df_score.append(df_col_values_melt)
        
		#having score and volume metric in separate columns
#     df_score_pivot = pd.pivot_table(df_score, 
#                                     index=['date','region','sector','brand','yougov_metric'],
#                                     values='value',
#                                     columns='metric',
#                                     aggfunc=np.sum)    
#
#    df_score_pivot.to_csv(pivot_output_filename, encoding='utf-8')


    df_score.to_csv(output_filename, encoding='utf-8', index = False)
