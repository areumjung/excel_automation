
# coding: utf-8

# In[1]:


import os, pandas as pd
from datetime import datetime


# In[2]:


os.chdir('C://Users//Areum.Jung//Desktop//Kantar')


# In[3]:


kantar = pd.read_excel('CVS_Kantar Competitor Spend_1-1-2018-8-19-2018.xlsx', sheet_name=0, skiprows=7, index_col=None)


# In[4]:


kantar = kantar.iloc[:-4,:]


# In[5]:


kantar.info()


# In[6]:


kantar.columns


# In[7]:


#Week Mapping


# In[8]:


kantar['week'] = kantar['TIME PERIOD'].apply(lambda x: x.split(' ')[1])
date_cov = []
for i in kantar['week']:
    date_cov.append(datetime.strptime(str(i), "%m/%d/%y").strftime('%Y-%m-%d'))
kantar['week'] = date_cov


week_map = pd.read_csv('kantar_week_mapping_8.21.csv')
week_cov = []
for i in week_map['week']:
    week_cov.append(datetime.strptime(str(i), "%m/%d/%Y").strftime('%Y-%m-%d'))
week_map['week'] = week_cov


kantar_week = kantar.merge(week_map, how='left')


# In[9]:


#DMA & Media Channel Mapping


# In[10]:


dma_map = pd.read_csv('kantar_dma_mapping_8.21.csv')
dma_map.rename(columns={"Kantar DMA":"MARKET"}, inplace=True)
kantar_dma = kantar_week.merge(dma_map, how='left')

channel_map = pd.read_csv('kantar_channel_mapping_8.21.csv')
channel_map.rename(columns={"Media":"MEDIA"}, inplace=True)
kantar_dma_channel = kantar_dma.merge(channel_map, how='left')

kantar_dma_channel['spend'] = kantar_dma_channel['DOLS (000)'] * 1000


# In[11]:


kantar_dma_channel.columns


# In[12]:


#Week	WEEK_NBR	ADVERTISER	PRODUCT	DMA_ID	DMA_NAME	Media	MEDIA_CAT	Spend


# In[13]:


kantar_dma_channel.rename(columns={'week':'WEEK', 'spend':'SPEND'}, inplace=True)
kantar_dma_channel.columns


# In[18]:


kantar_selected = kantar_dma_channel[['WEEK', 'WEEK_NBR', 'ADVERTISER', 'PRODUCT', 'DMA ID', 'MARKET','MEDIA', 'MEDIA_CAT', 'SPEND']]
kantar_selected = kantar_selected.set_index(['WEEK'])
kantar_selected.to_csv('CVS_Kantar Competitor Spend_1-1-2018-8-19-2018_formatted.csv')

