import pandas as pd
import numpy as np
from datetime import timedelta
import json
from pymongo import MongoClient
import requests
import os
import shutil
import json


url = "https://datasource.kapsarc.org/explore/dataset/saudi-arabia-coronavirus-disease-covid-19-situation/download/?format=csv&timezone=Asia/Baghdad&lang=en&use_labels_for_header=true&csv_separator=%3B"
req = requests.get(url)
url_content = req.content
csv_file = open('SA_data.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
data = pd.read_csv("SA_data.csv", sep=None, engine='python') # loading csv file

# Connect to MongoDB
client = MongoClient("mongodb+srv://Alnasser0:test@covid19-kfupm.8orak.azure.mongodb.net/COVID19-KFUPM?retryWrites=true&w=majority")

db = client['COVID19-KFUPM']
collection = db['COVID19']
collection.delete_many({})
#data_dict = data.to_dict("records")

# Insert collection
#collection.delete_one({"index":"SA_data"})
#collection.insert_one({"index":"SA_data","data":data_dict})
#collection.insert_many(data_dict)


###########################################################################
#CONNECT TO DB
client = MongoClient("mongodb+srv://Alnasser0:test@covid19-kfupm.8orak.azure.mongodb.net/COVID19-KFUPM?retryWrites=true&w=majority")
db = client['COVID19-KFUPM']
collection = db['COVID19']
#data_from_db=collection.find_one({"index":"SA_data"})


###########################################################################
###########################################################################
###########################################################################
###########################################################################
#DATA
#df = pd.DataFrame(data_from_db["data"])
#data_dict = df.to_dict("records")


#Clean Daily Data
df = data.dropna(subset=["Region"])
df_Daily = df.rename(columns = {"Region":"region"})
df_Daily = df_Daily.rename(columns = {"Cases (person)":"Cases"})
df_Daily = df_Daily.rename(columns = {"Daily / Cumulative":"Daily"})
df_Total = df_Daily.loc[(df_Daily['region'] == 'Total')]
df_Daily = df_Daily.loc[(df_Daily['Daily'] == 'Daily') & (df_Daily['region'] != 'Total')]
df_Daily['Date'] = pd.to_datetime(df_Daily['Date'])
df_Daily_regions = df_Daily.copy()
df_Daily = df_Daily.loc[df_Daily['region'] == 'Eastern Region']
df_Daily

#Clean Cumulative Data
df_Cumulative = df.rename(columns = {"Region":"region"})
df_Cumulative = df_Cumulative.replace({'Indicator': 'Active'}, 'Active cases')
df_Cumulative = df_Cumulative.rename(columns = {"Cases (person)":"Cases"})
df_Cumulative = df_Cumulative.rename(columns = {"Daily / Cumulative":"Cumulative"})
df_Cumulative = df_Cumulative.loc[(df_Cumulative['Cumulative'] == 'Cumulative') & (df_Cumulative['region'] != 'Total')]
df_Cumulative['Date'] = pd.to_datetime(df_Cumulative['Date'])
df_Cumulative_regions = df_Cumulative.copy()
df_Cumulative = df_Cumulative.loc[df_Cumulative['region'] == 'Eastern Region']

#Pivot Cumulative Data
df_Daily_regions_pivoted = df_Daily_regions.pivot_table('Cases', ['Date',	'region'], 'Indicator', fill_value=0, dropna=False, aggfunc='sum')
df_Daily_pivoted = df_Daily.pivot_table('Cases', ['Date',	'City'], 'Indicator', fill_value=0, dropna=False, aggfunc='sum')
df_Cumulative_regions_pivoted = df_Cumulative_regions.pivot_table('Cases', ['Date',	'region'], 'Indicator', fill_value=0, dropna=False, aggfunc='sum')
df_Cumulative_pivoted = df_Cumulative.pivot_table('Cases', ['Date',	'City'], 'Indicator', fill_value=0, dropna=False, aggfunc='sum')

#All Data
grouped_daily = df_Daily_pivoted.groupby('Date')['Cases', 'Mortalities', 'Recoveries'].sum().reset_index()
grouped_daily_cities = df_Daily_pivoted.groupby(['Date', 'City'])['Cases', 'Mortalities', 'Recoveries'].sum().reset_index()
grouped_daily_regions = df_Daily_regions_pivoted.groupby(['Date', 'region'])['Cases', 'Mortalities', 'Recoveries'].sum().reset_index()
grouped_cumulative = df_Cumulative_pivoted.groupby('Date')['Active cases', 'Cases', 'Mortalities', 'Recoveries'].sum().reset_index()
grouped_cumulative_cities = df_Cumulative_pivoted.groupby(['Date', 'City'])['Active cases', 'Cases', 'Mortalities', 'Recoveries'].sum().reset_index()
grouped_cumulative_regions = df_Cumulative_regions_pivoted.groupby(['Date', 'region'])['Active cases', 'Cases', 'Mortalities', 'Recoveries'].sum().reset_index()
grouped_daily_melt = grouped_daily.melt(id_vars="Date", value_vars=['Cases', 'Mortalities', 'Recoveries'], var_name='Case', value_name='Count')
grouped_daily_melt_cities = grouped_daily_cities.melt(id_vars=["Date", "City"], value_vars=['Cases', 'Mortalities', 'Recoveries'], var_name='Case', value_name='Count')
grouped_daily_melt_regions = grouped_daily_regions.melt(id_vars=["Date", "region"], value_vars=['Cases', 'Mortalities', 'Recoveries'], var_name='Case', value_name='Count')
grouped_cumulative_melt = grouped_cumulative.melt(id_vars="Date", value_vars=['Active cases', 'Mortalities', 'Recoveries'], var_name='Case', value_name='Count')
grouped_cumulative_melt_cities = grouped_cumulative_cities.melt(id_vars=["Date", "City"], value_vars=['Active cases', 'Mortalities', 'Recoveries'], var_name='Case', value_name='Count')
grouped_cumulative_melt_regions = grouped_cumulative_regions.melt(id_vars=["Date", "region"], value_vars=['Active cases', 'Mortalities', 'Recoveries'], var_name='Case', value_name='Count')
grouped_daily_weekly = grouped_daily.set_index('Date').resample('W').sum().reset_index()
grouped_daily_cities_weekly = grouped_daily_cities.set_index('Date').groupby(['City'])['Cases'].resample('W').sum().reset_index()
grouped_daily_regions_weekly = grouped_daily_regions.set_index('Date').groupby(['region'])['Cases'].resample('W').sum().reset_index()
grouped_cumulative_weekly = grouped_cumulative.set_index('Date').resample('W').sum().reset_index()

#Check and Process Cumulative Data
grouped_cumulative['CFR Percent'] = (100*grouped_cumulative.Mortalities)/grouped_cumulative.Cases
grouped_cumulative['Recovary Percent'] = (100*grouped_cumulative.Recoveries)/grouped_cumulative.Cases


grouped_cumulative_cities['CFR Percent'] = (100*grouped_cumulative_cities.Mortalities)/grouped_cumulative_cities.Cases
grouped_cumulative_cities['Recovary Percent'] = (100*grouped_cumulative_cities.Recoveries)/grouped_cumulative_cities.Cases
grouped_cumulative_cities = grouped_cumulative_cities.fillna(0)


grouped_cumulative_regions['CFR Percent'] = (100*grouped_cumulative_regions.Mortalities)/grouped_cumulative_regions.Cases
grouped_cumulative_regions['Recovary Percent'] = (100*grouped_cumulative_regions.Recoveries)/grouped_cumulative_regions.Cases
grouped_cumulative_regions = grouped_cumulative_regions.fillna(0)

#Check and Process Cumulative Data
grouped_daily_weekly['Cumulative Cases'] = grouped_daily_weekly['Cases'].cumsum()
grouped_daily_cities_weekly['Cumulative Cases'] = (grouped_daily_cities_weekly['Cases']).groupby(grouped_daily_cities_weekly['City']).cumsum()
grouped_daily_regions_weekly['Cumulative Cases'] = (grouped_daily_regions_weekly['Cases']).groupby(grouped_daily_regions_weekly['region']).cumsum()

#JSON Data Processing
list = []
f = open('SAU-geo.json') 
file = json.load(f)

for k in range(len(file['features'])):
    tuble = (file['features'][k]['properties']['NAME_1'], file['features'][k]['properties']['id'])
    list.append(tuble)

df = grouped_cumulative_regions.sort_values('Date', 
ascending=True).tail(np.count_nonzero(grouped_cumulative_regions.region.unique())
).sort_values('Active cases').reset_index()
for i in range(len(df.index)):
  for k in range(len(list)):
    if(df.region.iloc[i] == list[k][0]):
      df.loc[i, 'index'] = str(list[k][1])

#Total Data Process
df_Total['Date'] = pd.to_datetime(df_Total['Date'])
df_Total=df_Total.loc[(df_Total['Date'] == df_Total['Date'].max())]

# #Dump Data for Fast Access
# grouped_daily.to_csv('Data/grouped_daily.csv', index=False )
# grouped_daily_cities.to_csv('Data/grouped_daily_cities.csv', index=False)
# grouped_daily_regions.to_csv('Data/grouped_daily_regions.csv', index=False)
# grouped_cumulative.to_csv('Data/grouped_cumulative.csv', index=False)
# grouped_cumulative_cities.to_csv('Data/grouped_cumulative_cities.csv', index=False)
# grouped_cumulative_regions.to_csv('Data/grouped_cumulative_regions.csv', index=False)
# grouped_daily_melt.to_csv('Data/grouped_daily_melt.csv', index=False)
# grouped_daily_melt_cities.to_csv('Data/grouped_daily_melt_cities.csv', index=False)
# grouped_daily_melt_regions.to_csv('Data/grouped_daily_melt_regions.csv', index=False)
# grouped_cumulative_melt.to_csv('Data/grouped_cumulative_melt.csv', index=False)
# grouped_cumulative_melt_cities.to_csv('Data/grouped_cumulative_melt_cities.csv', index=False)
# grouped_cumulative_melt_regions.to_csv('Data/grouped_cumulative_melt_regions.csv', index=False)
# grouped_daily_weekly.to_csv('Data/grouped_daily_weekly.csv', index=False)
# grouped_daily_cities_weekly.to_csv('Data/grouped_daily_cities_weekly.csv', index=False)
# grouped_daily_regions_weekly.to_csv('Data/grouped_daily_regions_weekly.csv', index=False)
# grouped_cumulative_weekly.to_csv('Data/grouped_cumulative_weekly.csv', index=False)
# df.to_csv('Data/df.csv', index=False)
# df_Total.to_csv('Data/Total.csv', index=False)

#Dump Data Online

grouped_daily=grouped_daily.to_dict("records")
grouped_daily_cities=grouped_daily_cities.to_dict("records")
grouped_daily_regions=grouped_daily_regions.to_dict("records")
grouped_cumulative=grouped_cumulative.to_dict("records")
grouped_cumulative_cities=grouped_cumulative_cities.to_dict("records")
grouped_cumulative_regions=grouped_cumulative_regions.to_dict("records")
grouped_daily_melt=grouped_daily_melt.to_dict("records")
grouped_daily_melt_cities=grouped_daily_melt_cities.to_dict("records")
grouped_daily_melt_regions=grouped_daily_melt_regions.to_dict("records")
grouped_cumulative_melt=grouped_cumulative_melt.to_dict("records")
grouped_cumulative_melt_cities=grouped_cumulative_melt_cities.to_dict("records")
grouped_cumulative_melt_regions=grouped_cumulative_melt_regions.to_dict("records")
grouped_daily_weekly=grouped_daily_weekly.to_dict("records")
grouped_daily_cities_weekly=grouped_daily_cities_weekly.to_dict("records")
grouped_daily_regions_weekly=grouped_daily_regions_weekly.to_dict("records")
grouped_cumulative_weekly=grouped_cumulative_weekly.to_dict("records")
df=df.to_dict("records")
df_Total=df_Total.to_dict("records")

# Insert collection
#collection.insert_one({"index":"SA_data","data":data_dict})
collection.insert_one({"index":"grouped_daily","data":grouped_daily})
collection.insert_one({"index":"grouped_daily_cities","data":grouped_daily_cities})
collection.insert_one({"index":"grouped_daily_regions","data":grouped_daily_regions})
collection.insert_one({"index":"grouped_cumulative","data":grouped_cumulative})
collection.insert_one({"index":"grouped_cumulative_cities","data":grouped_cumulative_cities})
collection.insert_one({"index":"grouped_cumulative_regions","data":grouped_cumulative_regions})
collection.insert_one({"index":"grouped_daily_melt","data":grouped_daily_melt})
collection.insert_one({"index":"grouped_daily_melt_cities","data":grouped_daily_melt_cities})
collection.insert_one({"index":"grouped_daily_melt_regions","data":grouped_daily_melt_regions})
collection.insert_one({"index":"grouped_cumulative_melt","data":grouped_cumulative_melt})
collection.insert_one({"index":"grouped_cumulative_melt_cities","data":grouped_cumulative_melt_cities})
collection.insert_one({"index":"grouped_cumulative_melt_regions","data":grouped_cumulative_melt_regions})
collection.insert_one({"index":"grouped_daily_weekly","data":grouped_daily_weekly})
collection.insert_one({"index":"grouped_daily_cities_weekly","data":grouped_daily_cities_weekly})
collection.insert_one({"index":"grouped_daily_regions_weekly","data":grouped_daily_regions_weekly})
collection.insert_one({"index":"grouped_cumulative_weekly","data":grouped_cumulative_weekly})
collection.insert_one({"index":"df","data":df})
collection.insert_one({"index":"df_Total","data":df_Total})

#END OF DATA PROCESS
###########################################################################
###########################################################################
###########################################################################
###########################################################################


###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################