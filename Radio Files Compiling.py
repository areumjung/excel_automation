
# coding: utf-8

# ## Radio Files - from Radio Team

# In[48]:


import glob, os
import pandas as pd

def file_compile(directory, radio_mapping, output):
    
    os.chdir(directory)
    radio_df = pd.DataFrame()
    
    radio_mapping = pd.read_csv(radio_mapping)
    
    
    for file in glob.glob("*.xlsx"):
        base = os.path.basename(file)
        filename = os.path.splitext(base)
        
        radio_s = pd.ExcelFile(file, on_demand = True)
        radio_sheet = radio_s.sheet_names[:]
        
        for i, j in enumerate(radio_sheet):
            radio = pd.read_excel(base, sheet_name=i, header=0)
            radio['campaign'] = filename[0]
            radio['date'] = radio_sheet[i].split(' ')[0]
            radio['date'] = radio['date'] + '.18'
            radio['date'] = pd.to_datetime(radio['date'])
            #radio['date'] = radio['date'] + '/2018'
            radio['status'] = radio_sheet[i].split(' ')[1]
            radio_df = radio_df.append(radio)
        
    radio_df['Market'] = radio_df['Market'].apply(lambda x: x.split('[')[0])
    radio_df = radio_df.merge(radio_mapping, how='left')
    radio_df['status'].replace('Deliverd', 'Delivered', inplace=True)
    radio_df['status'].replace('Orderd', 'Ordered', inplace=True)
    radio_df = radio_df[['date','Market','DMA ID', 'campaign', 'status','GRPs']]
    radio_df.to_csv("radio_output.csv")


# ## Occurence File - from iHeart Radio

# In[44]:


import pandas as pd
import numpy as np

def iHeart_occurence(iHeart_file, iHeart_mapping, output):
    
    occ = pd.read_excel(iHeart_file, skiprows=2, header=0)
    occ.columns = ['date_col', 'A18+', 'A25-54', 'A65+']
    
    occ['dma_col'] = occ['date_col']
    occ['dma_one'] = occ.dma_col.apply(lambda x: x.split('-')[0])
    occ['dma_two'] = occ.dma_col.apply(lambda x: x.split('/')[0])
    
    occ.dma_two.replace(['1','2','3'], np.nan, inplace=True)
    occ.dma_two.ffill(axis=0, inplace=True)
    
    occ.drop(['dma_col', 'dma_one'], axis=1, inplace=True)
    occ.rename(columns={'dma_two':'Market'}, inplace=True)
    
    #occ.date_col.unique()
    dma_list = ['Atlanta', 'Austin', 'Baltimore', 'Boston', 'Charlotte', 'Chicago', 'Cincinnati', 'Cleveland', 
                'Columbus, OH', 'Dallas-Ft.Worth', 'Denver', 'Detroit', 'Greensboro', 'Hartford', 'Houston', 
                'Indianapolis', 'Jacksonville', 'Kansas City', 'Las Vegas', 'Los Angeles', 'Memphis', 'Miami',
                'Middlesex', 'Milwaukee', 'Minneapolis', 'Nashville', 'Nassau-Suffolk', 'New York', 'Norfolk', 
                'Orlando', 'Philadelphia', 'Phoenix', 'Pittsburgh', 'Portland, OR', 'Providence', 'Raleigh-Durham', 
                'Riverside-San Bernardino', 'Sacramento', 'Salt Lake City', 'San Antonio', 'San Diego', 
                'San Francisco', 'San Jose', 'Seattle', 'St. Louis', 'Tampa-St. Petersburg', 'Washington, DC', 
                'West Palm Beach']
    
    for i in occ.date_col:
        if i in dma_list:
            occ = occ[occ['date_col'] != i]
    
    occ['date'] = occ['date_col'].apply(lambda x: x.split('-')[0])
    occ = occ[occ['date'] != 'Grand Total']
    occ['date'] = pd.to_datetime(occ['date'])
    
    occ['Total GRP'] = occ['A18+'] + occ['A25-54'] + occ['A65+']
    
    occurence_mapping = pd.read_csv(iHeart_mapping)
    occ = occ.merge(occurence_mapping, how='left')
    
    #occ.columns
    occ = occ[[ 'date','Market','DMA ID','Total GRP','A18+','A25-54', 'A65+']]
    
    occ.to_csv(output)