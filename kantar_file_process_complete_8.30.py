
# coding: utf-8

# ## Setting up your working directory

# In[4]:


import os

os.chdir("C://Users//Areum.Jung//Desktop//Kantar")


# ## Import packages

# In[5]:


import pandas as pd
import numpy as np
from datetime import datetime


# # First Process

# In[ ]:


## Upload the file
kantar = pd.read_excel('CVS_Kantar Competitor Spend_1-1-2018-8-19-2018.xlsx', sheet_name=0, skiprows=7, index_col=None)
kantar = kantar.iloc[:-4,:]


# In[ ]:


## Week Mapping
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


# In[ ]:


## DMA & Media Channel Mapping
dma_map = pd.read_csv('kantar_dma_mapping_8.21.csv')
dma_map.rename(columns={"Kantar DMA":"MARKET"}, inplace=True)
kantar_dma = kantar_week.merge(dma_map, how='left')

channel_map = pd.read_csv('kantar_channel_mapping_8.21.csv')
channel_map.rename(columns={"Media":"MEDIA"}, inplace=True)
kantar_dma_channel = kantar_dma.merge(channel_map, how='left')

kantar_dma_channel['spend'] = kantar_dma_channel['DOLS (000)'] * 1000


# In[ ]:


## Renaming the column headers
kantar_dma_channel.rename(columns={'week':'WEEK', 'spend':'SPEND'}, inplace=True)


# In[ ]:


## Select columns you need
kantar_selected = kantar_dma_channel[['WEEK', 'WEEK_NBR', 'ADVERTISER', 'PRODUCT', 'DMA ID', 'MARKET','MEDIA', 'MEDIA_CAT', 'SPEND']]
kantar_selected = kantar_selected.set_index(['WEEK'])


# In[ ]:


## Export the output
kantar_selected.to_csv('CVS_Kantar Competitor Spend_1-1-2018-8-19-2018_formatted.csv')


# # Second Process

# In[6]:


## Load in your input files
pop = pd.read_excel("US pop by DMA 17.xlsx", sheet_name=0)
pop = pop.iloc[:,:2]

spd = pd.read_excel("CVS_Kantar Competitor Spend_1-1-2018-8-19-2018_formatted_v2.xlsx", sheet_name=0)

cvs = pd.read_excel("cvs_store_list.xlsx", sheet_name=0)


# ## R Code
# 
# ##################   Comp TTL #########################
# POP_ref <- read_excel("US pop by DMA 17.xlsx", sheet = 4, range="A1:B183")
# POP_ref$dma_id <- as.character(POP_ref$dma_id)
# 
# R_Com_SPD18Q2 <- read_excel("CVS_Kantar Competitor Spend_1-1-2018-5-27-2018_Formatted.xlsx",sheet=3)
# 
# ComDMA <- R_Com_SPD18Q2 %>%
#   filter(DMA_ID != "* NATIONAL" & DMA_ID != "ALL OTHER") %>%
#   select("DMA_ID") %>%
#   distinct() %>%
#   inner_join(DMA_MKT,by="DMA_ID") %>%              # DMAs competitor spent on where CVS has store
#   left_join(POP_ref,by=c("DMA_ID"="dma_id"))  %>% #5 DMAs missing population,670,705,755,676,673
#   replace(., is.na(.), 0) %>%
#   select(DMA_ID,pop)

# In[7]:


spd1 = spd[(spd['DMA_ID'] != '*National') & (spd['DMA_ID'] != 'All Other')]
unique_dma = spd1['DMA_ID'].unique()
unique_dma = pd.DataFrame(unique_dma)
unique_dma.columns = ['dma_id']
cvs.columns = ['dma_name', 'dma_id']
cvs_dma = unique_dma.merge(cvs, how='inner')
cvs_dma_pop = cvs_dma.merge(pop, how='left')
cvs_dma_pop = cvs_dma_pop.fillna(value=0)
cvs_dma_pop = cvs_dma_pop[['dma_id', 'pop']]
cvs_dma_pop = cvs_dma_pop.set_index('dma_id')


# In[ ]:


## Export
cvs_dma_pop.to_csv("process_qa//" + "cvs_dma_pop.csv")


# ## By Channel - TOTAL Competitor SPD - under DMAs

# ## R Code
# 
# #by Channel
# #TOTAL Competitor SPD - under DMAs
# Com_SPD18Q2A <- R_Com_SPD18Q2 %>%
#   filter(DMA_ID != "* NATIONAL" & DMA_ID != "ALL OTHER" & ADVERTISER != "CVS") %>%
#   select(-one_of("Week","PRODUCT","DMA_NAME","MEDIA","ADVERTISER")) %>%
#   dcast(WEEK_NBR + DMA_ID ~ MEDIA_CAT, fun = sum, value.var = "Spend")

# In[8]:


spd1_nocvs = spd1[spd1['ADVERTISER'] != 'CVS']
spd_one = spd1_nocvs[['WEEK_NBR', 'DMA_ID', 'MEDIA_CAT', 'SPEND']]
spd_one = pd.crosstab(index=[spd_one['WEEK_NBR'], spd_one['DMA_ID']], values=spd_one['SPEND'], columns=spd_one['MEDIA_CAT'], aggfunc=sum)


# In[ ]:


## Export
spd_one.to_csv("process_qa//" + "spd_one.csv")


# ## TOTAL Competitor SPD - Nation Wide

# ## R Code
# 
# #TOTAL Competitor SPD - Nation Wide
# Com_SPD18Q2B <- R_Com_SPD18Q2 %>%
#   filter((DMA_ID == "* NATIONAL" | DMA_ID == "ALL OTHER") & ADVERTISER != "CVS") %>%
#   select(-one_of("Week","PRODUCT","DMA_ID","DMA_NAME","MEDIA","ADVERTISER")) %>%
#   dcast(WEEK_NBR ~ MEDIA_CAT, fun = sum, value.var = "Spend") %>%
#   right_join(Com_SPD18Q2A,by=c("WEEK_NBR"="WEEK_NBR")) %>%
#   left_join(ComDMA,by=c("DMA_ID"="DMA_ID")) %>%
#   replace(., is.na(.), 0)  %>%
#   group_by(WEEK_NBR)  %>%
#   mutate(POP_PCT = pop/sum(pop))  %>%
#   ungroup()  %>%
#   mutate(Disp.x = POP_PCT * Disp.x, #assign national spd to DMA based on pop
#          NWSPPS.x = POP_PCT * NWSPPS.x,
#          TV.x = POP_PCT * TV.x,
#          comp_Mag_sp = POP_PCT * Mag,
#          comp_Disp_sp = Disp.x + Disp.y, #sum national part and DMA part
#          comp_NWSPPS_sp = NWSPPS.x + NWSPPS.y,
#          comp_TV_sp = TV.x + TV.y,
#          ttl_comp_sp=comp_Mag_sp+comp_Disp_sp+comp_NWSPPS_sp
#          +comp_TV_sp+Loc_Radio) %>%
#   select(WEEK_NBR,DMA_ID,comp_Disp_sp,comp_NWSPPS_sp,comp_TV_sp,comp_Mag_sp,comp_Radio_sp=Loc_Radio,
#          ttl_comp_sp)

# In[9]:


spd2 = spd[(spd['DMA_ID'] == '*National') | (spd['DMA_ID'] == 'All Other')] 
spd2_nocvs = spd2[spd2['ADVERTISER'] != 'CVS']
spd_two = spd2_nocvs[['WEEK_NBR', 'MEDIA_CAT', 'SPEND']]
spd_two = pd.crosstab(index=spd_two['WEEK_NBR'], values=spd_two['SPEND'], columns=spd_two['MEDIA_CAT'], aggfunc=sum)
spd_one = spd_one.reset_index()
spd_two = spd_two.reset_index()


# In[10]:


spd_two_merge = spd_two.merge(spd_one, how='left', left_on='WEEK_NBR', right_on='WEEK_NBR')

cvs_dma_pop = cvs_dma_pop.reset_index()
spd_two_merge_pop = spd_two_merge.merge(cvs_dma_pop, how='left', left_on='DMA_ID', right_on='dma_id')
spd_two_merge_pop.fillna(value=0, inplace=True)


# In[11]:


total_pop = spd_two_merge_pop['pop'].sum()
spd_two_merge_pop['pct'] = spd_two_merge_pop['pop'].apply(lambda x: x / total_pop)


# In[12]:


spd_two_merge_pop['Disp_x'] = spd_two_merge_pop['pct'] * spd_two_merge_pop['Disp_x']
spd_two_merge_pop['NWSPPS_x'] = spd_two_merge_pop['pct'] * spd_two_merge_pop['NWSPPS_x']
spd_two_merge_pop['TV_x'] = spd_two_merge_pop['pct'] * spd_two_merge_pop['TV_x']
spd_two_merge_pop['comp_Mag_sp'] = spd_two_merge_pop['pct'] * spd_two_merge_pop['Mag']

spd_two_merge_pop['comp_Disp_sp'] = spd_two_merge_pop['Disp_x'] + spd_two_merge_pop['Disp_y']
spd_two_merge_pop['comp_NWSPPS_sp'] = spd_two_merge_pop['NWSPPS_x'] + spd_two_merge_pop['NWSPPS_y']
spd_two_merge_pop['comp_TV_sp'] = spd_two_merge_pop['TV_x'] + spd_two_merge_pop['TV_y']
spd_two_merge_pop['ttl_comp_sp'] = spd_two_merge_pop['comp_Mag_sp'] + spd_two_merge_pop['comp_Disp_sp'] + spd_two_merge_pop['comp_NWSPPS_sp'] + spd_two_merge_pop['comp_TV_sp'] + spd_two_merge_pop['Loc_Radio']
spd_two_merge_pop['comp_Radio_sp'] = spd_two_merge_pop['Loc_Radio']

spd_comp_spd = spd_two_merge_pop[['WEEK_NBR','DMA_ID','comp_Disp_sp','comp_NWSPPS_sp','comp_TV_sp','comp_Mag_sp',
                                  'comp_Radio_sp','ttl_comp_sp']]


# In[ ]:


##Export
spd_comp_spd.to_csv("process_qa//" + "spd_comp_spd.csv")


# ## By ADVERTISER

# ## R Code
# 
# #by ADVERTISER
# Com_SPD18Q2AA <- R_Com_SPD18Q2 %>%
#   filter(DMA_ID != "* NATIONAL" & DMA_ID != "ALL OTHER" & ADVERTISER != "CVS") %>%
#   select(-one_of("Week","PRODUCT","DMA_NAME","MEDIA","MEDIA_CAT")) %>%
#   mutate(ADVERTISER = gsub("Ulta Beauty Supply & Salon", "Ulta", ADVERTISER),
#          ADVERTISER = gsub("Ulta.com Store", "Ulta", ADVERTISER),
#          ADVERTISER = gsub("Rite Aid", "Rite_Aid", ADVERTISER)) %>%
#   dcast(WEEK_NBR + DMA_ID ~ ADVERTISER, fun = sum, value.var = "Spend")

# In[13]:


spd3 = spd[(spd['DMA_ID'] != '*National') & (spd['DMA_ID'] != 'All Other') & (spd['ADVERTISER'] != "CVS")]
spd3.columns
spd3 = spd3[['WEEK_NBR', 'ADVERTISER', 'DMA_ID', 'SPEND']]
spd3['ADVERTISER'].replace('Ulta Beauty Supply & Salon', 'Ulta', inplace=True)
spd3['ADVERTISER'].replace('Ulta.com Store', 'Ulta', inplace=True)
spd3['ADVERTISER'].replace('Rite Aid', 'Rite_Aid', inplace=True)

spd3_crosstab = pd.crosstab(index=[spd3['WEEK_NBR'], spd3['DMA_ID']], values=spd3['SPEND'], columns=spd3['ADVERTISER'], aggfunc=sum)


# In[ ]:


spd3_crosstab.to_csv("process_qa//" + "spd3_crosstab.csv")


# ## TOTAL Competitor SPD - Nation Wide

# ## R Code
# 
# #TOTAL Competitor SPD - Nation Wide
# Com_SPD18Q2BB <- R_Com_SPD18Q2 %>%
#   filter((DMA_ID == "* NATIONAL" | DMA_ID == "ALL OTHER") & ADVERTISER != "CVS") %>%
#   select(-one_of("Week","PRODUCT","DMA_ID","DMA_NAME","MEDIA","MEDIA_CAT")) %>%
#   mutate(ADVERTISER = gsub("Ulta Beauty Supply & Salon", "Ulta", ADVERTISER),
#          ADVERTISER = gsub("Ulta.com Store", "Ulta", ADVERTISER),
#          ADVERTISER = gsub("Rite Aid", "Rite_Aid", ADVERTISER)) %>%
#   dcast(WEEK_NBR ~ ADVERTISER, fun = sum, value.var = "Spend") %>%
#   right_join(Com_SPD18Q2AA,by=c("WEEK_NBR"="WEEK_NBR")) %>%
#   left_join(ComDMA,by=c("DMA_ID"="DMA_ID")) %>%
#   replace(., is.na(.), 0)  %>%
#   group_by(WEEK_NBR)  %>%
#   mutate(POP_PCT = pop/sum(pop))  %>%
#   ungroup()  %>%
#   mutate(Walgreens.x = POP_PCT * Walgreens.x, #assign national spd to DMA based on pop
#          Walmart.x = POP_PCT * Walmart.x,
#          Rite_Aid.x = POP_PCT * Rite_Aid.x,
#          Target.x = POP_PCT * Target.x,
#          Sephora.x = POP_PCT * Sephora.x,
#          Ulta.x = POP_PCT * Ulta.x,
#          Walgreens = Walgreens.x + Walgreens.y, #sum national part and DMA part
#          Walmart = Walmart.x + Walmart.y,
#          Rite_Aid = Rite_Aid.x + Rite_Aid.y,
#          Target = Target.x + Target.y,
#          Sephora = Sephora.x + Sephora.y,
#          Ulta = Ulta.x + Ulta.y,
#          RtlComSPDTTL=Walgreens+Walmart+Rite_Aid+Target,
#          BtyComSPDTTL=Sephora+Ulta) %>%
#   select(WEEK_NBR,DMA_ID,Walgreens,Walmart,Rite_Aid,Target,Sephora,Ulta,RtlComSPDTTL,BtyComSPDTTL,POP_PCT)

# In[14]:


spd4 = spd[(spd['DMA_ID'] == '*National') | (spd['DMA_ID'] == 'All Other')] 
spd4_nocvs = spd4[spd4['ADVERTISER'] != 'CVS']
spd4_nocvs = spd4_nocvs[['WEEK_NBR', 'ADVERTISER', 'SPEND']]

spd4_nocvs['ADVERTISER'].replace('Ulta Beauty Supply & Salon', 'Ulta', inplace=True)
spd4_nocvs['ADVERTISER'].replace('Ulta.com Store', 'Ulta', inplace=True)
spd4_nocvs['ADVERTISER'].replace('Rite Aid', 'Rite_Aid', inplace=True)

spd4_crosstab = pd.crosstab(index=spd4_nocvs['WEEK_NBR'], values=spd4_nocvs['SPEND'], columns=spd4_nocvs['ADVERTISER'], 
                            aggfunc=sum)


# In[15]:


spd4_crosstab_reset = spd4_crosstab.reset_index()
spd3_crosstab_reset = spd3_crosstab.reset_index()


# In[16]:


spd4_right = spd4_crosstab_reset.merge(spd3_crosstab_reset, on='WEEK_NBR', how='right')
spd4_left = spd4_right.merge(cvs_dma_pop, left_on='DMA_ID', right_on='dma_id' , how='left')
spd4_left = spd4_left.fillna(0)


# In[17]:


spd4_total_pop = spd4_left['pop'].sum()
spd4_left['pct'] = spd4_left['pop'].apply(lambda x: x / spd4_total_pop)


# In[ ]:


spd4_left.columns


# In[18]:


spd4_left['Rite_Aid_x'] = spd4_left['pct'] * spd4_left['Rite_Aid_x']
spd4_left['Sephora_x'] = spd4_left['pct'] * spd4_left['Sephora_x']
spd4_left['Target_x'] = spd4_left['pct'] * spd4_left['Target_x']
spd4_left['Ulta_x'] = spd4_left['pct'] * spd4_left['Ulta_x']
spd4_left['Walgreens_x'] = spd4_left['pct'] * spd4_left['Walgreens_x']
spd4_left['Walmart_x'] = spd4_left['pct'] * spd4_left['Walmart_x']

spd4_left['Rite_Aid'] = spd4_left['Rite_Aid_x'] + spd4_left['Rite_Aid_y']
spd4_left['Sephora'] = spd4_left['Sephora_x'] + spd4_left['Sephora_y']
spd4_left['Target'] = spd4_left['Target_x'] + spd4_left['Target_y']
spd4_left['Ulta'] = spd4_left['Ulta_x'] + spd4_left['Ulta_y']
spd4_left['Walgreens'] = spd4_left['Walgreens_x'] + spd4_left['Walgreens_y']
spd4_left['Walmart'] = spd4_left['Walmart_x'] + spd4_left['Walmart_y']
spd4_left['RtlComSPDTTL'] = spd4_left['Rite_Aid'] + spd4_left['Sephora'] + spd4_left['Target'] + spd4_left['Walgreens']
spd4_left['BtyComSPDTTL'] = spd4_left['Sephora'] + spd4_left['Ulta']


# In[21]:


final_output = spd4_left[['WEEK_NBR', 'DMA_ID', 'Rite_Aid', 'Sephora', 'Target', 'Ulta', 'Walgreens', 'Walmart',
                          'RtlComSPDTTL', 'BtyComSPDTTL', 'pct']]
final_output.set_index('WEEK_NBR', inplace=True)


# In[22]:


final_output.to_csv("process_qa//" + "final_output.csv")

