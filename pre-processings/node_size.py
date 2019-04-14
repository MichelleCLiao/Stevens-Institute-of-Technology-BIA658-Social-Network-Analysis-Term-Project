# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 17:59:25 2018

@author: lethe
"""

import pandas as pd
import numpy as np
import os

os.chdir("D:\\BIA-658 Social Network Analysis\\project\\new")
data = pd.read_csv("type_level_crime_sum.csv")
sum_ = data.groupby('precinct')['sum'].sum()
sum_ = pd.DataFrame(sum_)
boro = pd.read_csv("boro_precinct.csv")
boro.set_index(['precinct'],inplace = True)

merge = pd.merge(boro,sum_,left_index = True, right_index = True)
merge['crime/thousand_people'] = 0
for i in merge.index:
    merge.loc[i,'crime/thousand_people'] = merge.loc[i,'sum'] / merge.loc[i,'population']
merge.to_csv('crime_per_thousand_people.csv')  
#-------------------levels----------------------------
os.chdir("D:\\BIA-658 Social Network Analysis\\project\\new\\level_network")
data = pd.read_csv("../type_level_crime_sum.csv")
data = data.iloc[:,1:5]
felony = data.loc[data.loc[:,'level'] == 'FELONY']
misdemeanor = data.loc[data.loc[:,'level'] == 'MISDEMEANOR']
violation = data.loc[data.loc[:,'level'] == 'VIOLATION']
boro2 = pd.read_csv("../boro_precinct.csv")
boro2.set_index(['precinct'],inplace = True)
def sumup(level):
    sum_2 = level.groupby('precinct')['sum'].sum()
    sum_2 = pd.DataFrame(sum_2)
    merge2 = pd.merge(boro2,sum_2,left_index = True, right_index = True)
    merge2['crime/thousand_people'] = 0
    for i in merge2.index:
        merge2.loc[i,'crime/thousand_people'] = merge2.loc[i,'sum'] / merge2.loc[i,'population']
    return merge2 

felony_rate = sumup(felony)
misdemeanor_rate = sumup(misdemeanor)
violation_rate = sumup(violation)
felony_rate.to_csv('felony_rate.csv')
misdemeanor_rate.to_csv('misdemeanor_rate.csv')
violation_rate.to_csv('violation_rate.csv')