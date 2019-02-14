#!/usr/bin/env python
# coding: utf-8

# In[ ]:


pwd


# In[ ]:


cd "C://Users//areum.jung//Desktop//MCK Local//Sales data"


# In[ ]:


ls


# ## Combining All files

# In[83]:


import pandas as pd
import os, glob

def mkc_sales(input_directory):
    
    os.chdir(input_directory)
    
    all_sales = pd.DataFrame()
    
    file_list = []
    for file in glob.glob('Insights Day_' + '*.xlsx'):
        file_list.append(file)
        
    for f in file_list:
        print(f)
        
        index_df = pd.read_excel(f, sheet_name=0)
        index_df = index_df.iloc[:,1:4]

        campaign = index_df.iloc[:,1][0]
        geo = index_df.iloc[:,2]

        cfv_chr_output = pd.DataFrame()


        for s in range(1,10):
            
            cfv_chr = pd.read_excel(f, sheet_name=s, header=7)
            geo_loc = geo[s-1]

            cfv_chr_var = cfv_chr.columns[0:2]
            cfv_chr_col = cfv_chr.columns[2:]
            cfv_chr_melt = cfv_chr.melt(id_vars=cfv_chr_var, value_vars=cfv_chr_col, var_name='week', value_name='value')
            cfv_chr_melt.rename(columns={'Product':'product', 'Measures':'measures'}, inplace=True)

            cfv_chr_melt['geo'] = geo_loc
            cfv_chr_melt['campaign'] = campaign
            #print(cfv_chr_melt.head())


            cfv_chr_output = cfv_chr_output.append(cfv_chr_melt)
        
        cfv_chr_output['product'] = cfv_chr_output['product'].fillna(method='ffill')
        cfv_chr_output['product'] = cfv_chr_output['product'].astype(str)
        cfv_chr_output['product'] = cfv_chr_output['product'].apply(lambda x: x.strip()) 
        
        cfv_chr_output['week'] = cfv_chr_output['week'].apply(lambda x: x.replace("Week Ending ", ''))
        cfv_chr_output['campaign'] = cfv_chr_output['campaign'].apply(lambda x: x.replace("Insights Day: ", ''))
        cfv_chr_output['campaign'] = cfv_chr_output['campaign'].apply(lambda x: x.replace("Sup", 'Superiority'))
        cfv_chr_output = cfv_chr_output.set_index(['week'])
        
        all_sales = all_sales.append(cfv_chr_output)
        
        all_sales.to_csv("output_two//all_sales.csv")


# In[84]:


mkc_sales("C://Users//areum.jung//Desktop//MCK Local//Sales data//")


# ## Exception - Insights Day_ Frank's PDI & CDI (2)

# In[40]:


franks = pd.read_excel("C://Users//areum.jung//Desktop//MCK Local//Sales data//exception//Insights Day_ Frank's PDI & CDI (2).xlsx", sheet_name=1, header=7)

franks_var = franks.columns[:2]
franks_col = franks.columns[2:]
franks_melt = franks.melt(id_vars=franks_var, value_vars=franks_col, var_name='week', value_name='value')
franks_melt['week'] = franks_melt['week'].apply(lambda x: x.replace("Week Ending ", ''))
franks_melt['campaign'] = 
franks_melt.to_csv("output//Insights Day_ Frank's PDI & CDI (2)_output.csv")

