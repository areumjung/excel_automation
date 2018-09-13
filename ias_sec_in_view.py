
# coding: utf-8

# In[15]:


import pandas as pd, os, glob
from datetime import datetime

def ias(directory):

    os.chdir(directory)

    all_output = pd.DataFrame()

    for f in glob.glob('CVS.' + '*.xlsx'):

        print("File(s) being processed: ", f)
        base = os.path.basename(f)
        filename = os.path.splitext(base)

        xls = pd.ExcelFile(f, on_demand = True)
        tab_names = xls.sheet_names[:]
        output = pd.DataFrame()

        if 'exception' not in f:
            for i in tab_names:
                df = pd.read_excel(f, sheet_name=i, skiprows=7)
                if len(df) > 24:

                    df_first = df.iloc[:17,3:]
                    df_first['tab_names'] = i
                    df_first['campaign_name'] = df_first['tab_names'].apply(lambda x: x.split('_')[0])
                    df_first['week'] = df_first['tab_names'].apply(lambda x: x.split('_')[1])
                    df_first['week_start'] = df_first['week'].apply(lambda x: x.split('-')[0])
                    df_first['format'] = df_first.iloc[0,0]
                    df_first['filename'] = f
                    output = output.append(df_first.iloc[4:, :])

                    df_two = df.iloc[18:, 3:]
                    df_two['tab_names'] = i
                    df_two['campaign_name'] = df_two['tab_names'].apply(lambda x: x.split('_')[0])
                    df_two['week'] = df_two['tab_names'].apply(lambda x: x.split('_')[1])
                    df_two['week_start'] = df_two['week'].apply(lambda x: x.split('-')[0])
                    df_two['format'] = df_two.iloc[0,0]
                    df_two['filename'] = f
                    output = output.append(df_two.iloc[4:, :])

                else:
                    df_first = df.iloc[:17,3:]
                    df_first['tab_names'] = i
                    df_first['campaign_name'] = df_first['tab_names'].apply(lambda x: x.split('_')[0])
                    df_first['week'] = df_first['tab_names'].apply(lambda x: x.split('_')[1])
                    df_first['week_start'] = df_first['week'].apply(lambda x: x.split('-')[0])
                    df_first['format'] = df_first.iloc[0,0]
                    df_first['filename'] = f
                    output = output.append(df_first.iloc[4:, :])


        elif 'exception' in f:
            for i in tab_names:
                df = pd.read_excel(f, sheet_name=i, skiprows=7)
                if len(df) > 24:

                    df_first = df.iloc[:17,3:]
                    df_first['tab_names'] = i
                    df_first['campaign_name'] = df_first['tab_names'].apply(lambda x: x.split(' ')[1])
                    df_first['week'] = df_first['tab_names'].apply(lambda x: x.split('_')[0])
                    df_first['week_start'] = df_first['week'].apply(lambda x: x.split('-')[0])
                    df_first['format'] = df_first.iloc[0,0]
                    df_first['filename'] = f
                    output = output.append(df_first.iloc[4:, :])

                    df_two = df.iloc[18:, 3:]
                    df_two['tab_names'] = i
                    df_two['campaign_name'] = df_two['tab_names'].apply(lambda x: x.split(' ')[1])
                    df_two['week'] = df_two['tab_names'].apply(lambda x: x.split('_')[0])
                    df_two['week_start'] = df_two['week'].apply(lambda x: x.split('-')[0])
                    df_two['format'] = df_two.iloc[0,0]
                    df_two['filename'] = f
                    output = output.append(df_two.iloc[4:, :])

                else:
                    df_first = df.iloc[:17,3:]
                    df_first['tab_names'] = i
                    df_first['campaign_name'] = df_first['tab_names'].apply(lambda x: x.split(' ')[1])
                    df_first['week'] = df_first['tab_names'].apply(lambda x: x.split('_')[0])
                    df_first['week_start'] = df_first['week'].apply(lambda x: x.split('-')[0])
                    df_first['format'] = df_first.iloc[0,0]
                    df_first['filename'] = f
                    output = output.append(df_first.iloc[4:, :])

        all_output = all_output.append(output)    

    all_output.columns = ['Exposure Time', '# of consumers', 'Freq_1', 'Freq_2', 'Freq_3', 'Freq_4', 'Freq_5', 
                          'Freq_6', 'Freq_7', 'Freq_8', 'Freq_9', 'Freq_10', 'tab', 'campaign', 'week', 
                          'week_start', 'format', 'filename']

    #Campaign and LOB Mapping
    campaign_mapping = pd.read_csv("campaign_mapping.csv")
    
    lob_mapping = pd.read_csv("lob_mapping.csv")

    campaign_mapped = all_output.merge(campaign_mapping, how='left')
    lob_output_mapped = campaign_mapped.merge(lob_mapping, how='left')

    lob_output_mapped['Exposure Time'] = lob_output_mapped['Exposure Time'].apply(lambda x: x.replace(" ", ""))
    time_mapping = pd.DataFrame({'alpha':['a_<1','b_1-2','c_2-5','d_5-10','e_10-15','f_15-20','g_20-25',
                                          'h_25-30','i_30-35','j_35-40','k_40-45','l_45-50','m_50>'],
                                 'Exposure Time':['<1','1-2','2-5','5-10','10-15','15-20','20-25','25-30','30-35',
                                                  '35-40','40-45','45-50','50>']})
    output_mapped = lob_output_mapped.merge(time_mapping, how='left')

    output_mapped['week_start'] = output_mapped['week_start'].apply(lambda x: x.replace(".", "/"))
    output_mapped['week_start'] = output_mapped['week_start'].apply(lambda x: x + ("/2018"))

    final_output = output_mapped[['week_start', 'LOB', 'campaign_name', 'format', 'Exposure Time', 'alpha', '# of consumers', 'Freq_1', 
                                  'Freq_2', 'Freq_3', 'Freq_4', 'Freq_5', 'Freq_6', 'Freq_7', 'Freq_8', 'Freq_9', 'Freq_10', 
                                  'filename']]
    final_output = final_output.drop('Exposure Time', axis=1)
    final_output.rename(columns={'alpha':'Exposure Time'}, inplace=True)

    #Impression Calculation
    final_output = final_output.fillna(value=0)

    imps_df = pd.DataFrame()

    for i in range(len(final_output['# of consumers'])):
        for k in range(10):
            imps_df.loc[i, k] = (k+1) * final_output['# of consumers'][i] * final_output.iloc[i,k+6]    
   
    imps_total = []
    for k in range(len(imps_df)):
        imps_total.append(sum(imps_df.iloc[k,0:10])/100)
    imps_df['imps'] = imps_total
    imps_df.columns = ['freq_1_imps', 'freq_2_imps', 'freq_3_imps', 'freq_4_imps', 'freq_5_imps', 'freq_6_imps', 'freq_7_imps',
                      'freq_8_imps', 'freq_9_imps', 'freq_10_imps', 'Total imps']

    all_output_final = pd.concat([final_output, imps_df], axis=1)
    all_output_final.set_index('week_start', inplace=True)

    #final_output
    all_output_final.to_csv('Output//' + 'all_output_final_' + datetime.today().strftime('%m.%d') + '.csv')

