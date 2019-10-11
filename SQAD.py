#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


sq_headers = pd.read_excel("McCormick SQAD ALL Regions- 2020.xlsx", sheet_name=0, header=0)
sq_headers = sq_headers.columns


# In[3]:


sq = pd.read_excel("McCormick SQAD ALL Regions- 2020.xlsx", sheet_name=0, header=1)
sq_first_headers = sq.reset_index().columns
sq_first_headers = sq_first_headers[4:]
sq_first_headers


# In[4]:


headers_final = sq_headers[:,] + "_" + sq_first_headers


# In[5]:


sq.columns = ['Demo', 'Market', 'Quarter', 'Morning Drive_:60s CPP', 'Morning Drive.1_:30s CPP',
       'Morning Drive.2_:15s CPP', 'Daytime_:60s CPP.1',
       'Daytime.1_:30s CPP.1', 'Daytime.2_:15s CPP.1',
       'Afternoon Drive_:60s CPP.2', 'Afternoon Drive.1_:30s CPP.2',
       'Afternoon Drive.2_:15s CPP.2', 'Evening_:60s CPP.3',
       'Evening.1_:30s CPP.3', 'Evening.2_:15s CPP.3', 'Weekend_:60s CPP.4',
       'Weekend.1_:30s CPP.4', 'Weekend.2_:15s CPP.4']


# In[6]:


sq.head()


# In[7]:


sq_melt = sq.melt(id_vars=['Demo', 'Market', 'Quarter'], value_vars=['Morning Drive_:60s CPP', 'Morning Drive.1_:30s CPP',
       'Morning Drive.2_:15s CPP', 'Daytime_:60s CPP.1',
       'Daytime.1_:30s CPP.1', 'Daytime.2_:15s CPP.1',
       'Afternoon Drive_:60s CPP.2', 'Afternoon Drive.1_:30s CPP.2',
       'Afternoon Drive.2_:15s CPP.2', 'Evening_:60s CPP.3',
       'Evening.1_:30s CPP.3', 'Evening.2_:15s CPP.3', 'Weekend_:60s CPP.4',
       'Weekend.1_:30s CPP.4', 'Weekend.2_:15s CPP.4'], var_name='Daytime_Length', value_name='CPP')


# In[8]:


sq_melt.head()


# In[9]:


sq_melt['Dayparts'] = sq_melt['Daytime_Length'].apply(lambda x: x.split('_')[0])
sq_melt['Dayparts'] = sq_melt['Dayparts'].apply(lambda x: x.split('.')[0])
sq_melt['Length'] = sq_melt['Daytime_Length'].apply(lambda x: x.split('_')[1])
sq_melt['Length'] = sq_melt['Length'].apply(lambda x: x.split(' ')[0])


# In[10]:


sq_melt.head()


# In[11]:


sqad_melt = sq_melt[['Demo', 'Market', 'Quarter', 'CPP', 'Dayparts', 'Length']]
sqad_index = 'Demo'


# In[12]:


sqad_melt = sqad_melt.set_index(['Demo'])


# In[13]:


sqad_melt.to_csv('sqad_melt.csv')

