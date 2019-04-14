# -*- coding: utf-8 -*-
"""
Created on Fri Nov  9 20:40:59 2018

@author: lethe
"""

import pandas as pd
import numpy as np

#read the file
df = pd.read_csv("random.csv")

#abstract boro and precinct in case of further use
boro = df.iloc[:,6:8]
boro.columns = ['boro','precinct']
boro.to_csv('boro_precinct.csv', index=False)

#drop unecessary variables
df.drop(columns=["CMPLNT_FR_DT","RPT_DT","OFNS_DESC",
                 "BORO_NM","PREM_TYP_DESC"], inplace = True)
df.drop(columns=["CMPLNT_NUM","CMPLNT_FR_TM","CMPLNT_TO_TM",
                 "PD_CD",'PD_DESC','LOC_OF_OCCUR_DESC','PARKS_NM',
                 'HADEVELOPT','X_COORD_CD','JURIS_DESC',
                 'Y_COORD_CD','Lat_Lon',"CMPLNT_TO_DT","Longitude",'Latitude'], inplace = True)
df = df.dropna()
#rename cols, actually lat and lon is useless here
df.columns = ['key','type','level','precinct']
#save the file in case of further use
df.to_csv("data.csv",index = False)
data = pd.read_csv('data.csv')
#add a column = sum
df['sum'] = 1
"""
add up all cases with the same precinct, type, and level
since the index of cnt is a tuple, so extract it and change it to df
           now it's a df, with normal integer index start with 
change cnt to df and set the index to normal integer
merge two df base on index.
"""
cnt = df['sum'].groupby([df['precinct'],df['type'],df['level']]).sum()
lt = list(cnt.index)
lt = pd.DataFrame(lt)
cnt = pd.DataFrame(cnt)
cnt.set_index(lt.index,inplace = True)
merge = pd.merge(lt,cnt,left_index = True, right_index=True)
merge.to_csv("random_type_level_sum.csv")
"""
assign scores:
    attempted = 1, completed = 2
    felony = 5, violation = 2.5, misdemeanor = 1
    by multiplication, max = 10, min = 1
    then times the count of crimes
"""
#add a col to store the score for each precinct
merge["score"] = 0

#assign the categories as score
for i in merge.index:
    if merge.loc[i,1] == "ATTEMPTED":
        merge.loc[i,1] = 1
    else:
        merge.loc[i,1] = 2
    if merge.loc[i,2] == "FELONY":
        merge.loc[i,2] = 5
    elif merge.loc[i,2] == "VIOLATION":
        merge.loc[i,2] = 2.5
    else:
        merge.loc[i,2] = 1
      
#calculate the score
for i in merge.index:
    merge.loc[i,'score'] = merge.loc[i,1] * merge.loc[i,2] * merge.loc[i,'sum']
merge.columns = ["precinct","type","level","sum","score"]
#groupby to get the final score of each precinct
scores = merge.groupby("precinct")['score'].sum()
scores = pd.DataFrame(scores)

#normalize the geo-info of each precinct
geo = pd.read_csv("preprocessing/locations.csv")
geo.set_index(scores.index, inplace = True)
geo.drop(columns = ['precinct'],inplace = True)
scores_geo = pd.merge(scores,geo,left_index = True, right_index=True)

scores_geo.to_csv("score_geo.csv")
#normalize seperately
s_max = scores_geo['score'].max()
s_min = scores_geo['score'].min()
lng_max = scores_geo['Longitude'].max()
lng_min = scores_geo['Longitude'].min()
lat_max = scores_geo['Latitude'].max()
lat_min = scores_geo['Latitude'].min()
for i in scores_geo.index:
    s_val = (scores_geo.loc[i,'score'] - s_min)/(s_max - s_min)
    lng_val = (scores_geo.loc[i,'Longitude'] - lng_min)/(lng_max - lng_min)
    lat_val = (scores_geo.loc[i,'Latitude'] - lat_min)/(lat_max - lat_min)
    scores_geo.loc[i,'score'] = s_val
    scores_geo.loc[i,'Longitude'] = lng_val
    scores_geo.loc[i,'Latitude'] = lat_val


#create a df to store the results
dist = list(scores_geo.index)
dist = pd.DataFrame(dist)
for i in scores_geo.index:
    dist[i] = 0
dist.set_index([0],inplace = True)

#calculate the euclidean distance  
for i in dist.index:
    for j in dist.index:
        vec1 = np.array(scores_geo.loc[i,])
        vec2 = np.array(scores_geo.loc[j,])
        val = np.linalg.norm(vec1 - vec2)
        dist.loc[i,j] = val
        
#write to file
dist.to_csv("euclidean_dist.csv")

#filt the edge
for i in range(0,77):
    # np.argsort returns the actual index start from 0
    sort_list = np.argsort(dist.iloc[:,i])
    sort_list = pd.DataFrame(sort_list)
    flag = 0
    for j in dist.index:
        if flag > 5:
            dist.iloc[sort_list.iloc[flag,0],i] = 0
        flag += 1
        
dist.to_csv("edge_weighted.csv")

#similarity
for i in dist.index:
    for j in dist.index:
        if dist.loc[i,j] != 0:
            dist.loc[i,j] = 1 - dist.loc[i,j]
            
dist.to_csv("edge_similarity.csv")

#compile unweighted matrix
for i in dist.index:
    for j in dist.index:
        if dist.loc[i,j] != 0:
            dist.loc[i,j] = 1
            
dist.to_csv("edge_unweighted.csv")
           
#----------------
boro = pd.read_csv("boro_precinct.csv")
a = {}
for i in boro['boro'].unique():
    a[i] = []
for i in boro.index:
    b = boro.iloc[i,0]
    for j in a:
        if b == j:
            a[j].append(boro.iloc[i,1])
d = {}
for i in boro['boro'].unique():
    d[i] = []
for i in a:
    for j in a[i]:
        if j not in d[i]:
            d[i].append(j)
                       
bo = pd.DataFrame.from_dict(d,orient='index')

#__________________________
file = ['chrismas_type_level_sum.csv']#,
        #'thanksgiving_type_level_sum.csv',
        #'random_type_level_sum.csv']
for i in file:
    data = pd.read_csv(i)
    felony = data.loc[data.loc[:,'2'] == 'FELONY']
    misdemeanor = data.loc[data.loc[:,'2'] == 'MISDEMEANOR']
    violation = data.loc[data.loc[:,'2'] == 'VIOLATION']
    
    felony_sum = felony.groupby('0')['sum'].sum()
    misdemeanor_sum = misdemeanor.groupby('0')['sum'].sum()
    violation_sum = violation.groupby('0')['sum'].sum()
    
    print(i + ':\n' + 'felony: ' + str(sum(felony_sum)) +
          '\n' + 'misdemeanor: ' + str(sum(misdemeanor_sum)) +
          '\n' + 'violation:' + str(sum(violation_sum)))
      
#---------------------------------------------------
    #change to dummy variables
data = pd.read_csv('data.csv')
#add a column = sum
df['sum'] = 1

type_ = data.groupby([data['precinct'],data['type']])['sum'].sum()
lt = list(type_.index)
lt = pd.DataFrame(lt)
type_ = pd.DataFrame(type_)
type_.set_index(lt.index, inplace = True)
merge = pd.merge(type_,lt,left_index = True, right_index=True)

merge['ATTEMPTED'] = 0
merge['COMPLETED'] = 0

for i in range(0,154):
    if merge.iloc[i,2] == merge.columns[3]:
        merge.iloc[i,3] = merge.iloc[i,0]
    if merge.iloc[i,2] == merge.columns[4] and merge.iloc[i,1] == merge.iloc[i-1,1]:
        merge.iloc[i-1,4] = merge.iloc[i,0]
    else:
        merge.iloc[i,4] = merge.iloc[i,0]


        
cnt = data['sum'].groupby([data['precinct'],data['type'],data['level']]).sum()
lt = list(cnt.index)
lt = pd.DataFrame(lt)
cnt = pd.DataFrame(cnt)
cnt.set_index(lt.index,inplace = True)
merge = pd.merge(lt,cnt,left_index = True, right_index=True)
merge.to_csv("dummy.csv")


    

    










