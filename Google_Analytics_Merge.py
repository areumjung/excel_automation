
# coding: utf-8

# In[1]:


import pandas as pd
import os, glob
from datetime import datetime


# In[2]:


def ga_merge(input_directory, output_filename):

    os.chdir(input_directory)
    
    file_list = []
    df = pd.DataFrame()
    for file in glob.glob('Analytics ' + '*.csv'):
        file_list.append(file)
        for i in file_list:
            df = df.append(pd.read_csv(i, skiprows=5))

    date_cov = []
    for i in df['Date']:
        date_cov.append(datetime.strptime(str(i), '%Y%m%d').strftime('%Y-%m-%d'))
    df['date_cov'] = date_cov

    df = df[[ 'date_cov', 'City', 'Region', 'Page', 'Users']]
    df.rename(columns={'date_cov':'Date'}, inplace=True)
    df = df.set_index(['Date'])
    df.to_csv(output_filename)

