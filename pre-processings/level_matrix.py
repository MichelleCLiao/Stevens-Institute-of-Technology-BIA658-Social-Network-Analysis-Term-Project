# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 21:44:15 2018

@author: lethe
"""

import pandas as pd
import numpy as np
import os

data = pd.read_csv("../type_level_crime_sum.csv")
data = data.iloc[:,1:5]
data.columns = ['precinct','type','level','sum']
#assign scores first: attempted = 1, completed = 2
for j in data.index:
    if data.iloc[j,1] == 'ATTEMPTED':
        data.iloc[j,1] = 1
    else:
        data.iloc[j,1] = 2

#type * sum
for i in data.index:
    data.iloc[i,3] = data.iloc[i,1] * data.iloc[i,3]

  #seperate levels      
felony = data.loc[data.loc[:,'level'] == 'FELONY']
misdemeanor = data.loc[data.loc[:,'level'] == 'MISDEMEANOR']
violation = data.loc[data.loc[:,'level'] == 'VIOLATION']
geo = pd.read_csv("../locations.csv")
geo = geo.set_index('precinct')
#build a function
def op(level):
    level.drop(columns = ['level'],inplace = True)
    level = level.groupby('precinct')['sum'].sum()
    level = pd.DataFrame(level)
    level = pd.merge(level,geo,left_index = True,right_index = True)
    return level

felony = op(felony)
misdemeanor = op(misdemeanor)
violation = op(violation)

#standardize
def stan(level):
    s_max = level['sum'].max()
    s_min = level['sum'].min()
    lng_max = level['Longitude'].max()
    lng_min = level['Longitude'].min()
    lat_max = level['Latitude'].max()
    lat_min = level['Latitude'].min()
    for i in level.index:
        level.loc[i,'sum'] = (level.loc[i,'sum'] - s_min)/(s_max - s_min)
        level.loc[i,'Longitude'] = (level.loc[i,'Longitude'] - lng_min)/(lng_max - lng_min)
        level.loc[i,'Latitude'] = (level.loc[i,'Latitude'] - lat_min)/(lat_max - lat_min)
        
    return level

felony = stan(felony)
misdemeanor = stan(misdemeanor)
violation = stan(violation)


#calculate the euclidean distance 
def ed(level):  
        #create a df to store the results
    dist = list(felony.index)
    dist = pd.DataFrame(dist)
    for i in felony.index:
        dist[i] = 0
    dist.set_index([0],inplace = True)    
    for i in dist.index:
        for j in dist.index:
            vec1 = np.array(level.loc[i,])
            vec2 = np.array(level.loc[j,])
            val = np.linalg.norm(vec1 - vec2)
            dist.loc[i,j] = val
    return dist

felony_dist = ed(felony)
misdemeanor_dist = ed(misdemeanor)
violation_dist = ed(violation)

#filt the edge
def filt(level):
    for i in range(0,77):
            # np.argsort returns the actual index start from 0
        sort_list = np.argsort(level.iloc[:,i])
        sort_list = pd.DataFrame(sort_list)
        flag = 0
        for j in level.index:
            if flag > 5:
                level.iloc[sort_list.iloc[flag,0],i] = 0
            flag += 1
    return level

felony_dist = filt(felony_dist)
misdemeanor_dist = filt(misdemeanor_dist)      
violation_dist = filt(violation_dist)

felony_dist.to_csv("felony_eudist.csv")
misdemeanor_dist.to_csv("misdemeanor_eudist.csv")
violation_dist.to_csv("violation_eudist.csv")

#compute the similarity
def simi(level):
    for i in level.index:
        for j in level.index:
            if level.loc[i,j] != 0:
                level.loc[i,j] = 1 - level.loc[i,j]
                
    return level

felony_simi= simi(felony_dist)
misdemeanor_simi = simi(misdemeanor_dist)      
violation_simi = simi(violation_dist)

felony_simi.to_csv("felony_similarity.csv")
misdemeanor_simi.to_csv("misdemeanor_similarity.csv")
violation_simi.to_csv("violation_similarity.csv")

#unweighted edge
def edge(level):
    for i in level.index:
        for j in level.index:
            if level.loc[i,j] != 0:
                level.loc[i,j] = 1
    return level
felony_unweighted = edge(felony_simi)
misdemeanor_unweighted = edge(misdemeanor_simi)
violation_unweighted = edge(violation_simi)

felony_unweighted.to_csv("felony_unweighted.csv")
misdemeanor_unweighted.to_csv("misdemeanor_unweighted.csv")
violation_unweighted.to_csv("violation_unweighted.csv")


