import pandas as pd
import numpy as np
from datetime import timedelta
import json

###########################################################################
###########################################################################
###########################################################################
###########################################################################
#DATA

#Read Data
df = pd.read_csv("SA_data.csv", sep=None, engine='python')


#Clean Daily Data
df = df.dropna(subset=["region"])
df_Daily = df.rename(columns = {"Daily / Cumulative":"Daily"})
df_Total = df_Daily.loc[(df_Daily['region'] == 'Total')]
df_Daily = df_Daily.loc[(df_Daily['Daily'] == 'Daily') & (df_Daily['region'] != 'Total')]
df_Daily['Date'] = pd.to_datetime(df_Daily['Date'])
df_Daily_regions = df_Daily.copy()
df_Daily = df_Daily.loc[df_Daily['region'] == 'Eastern Region']
df_Daily

#Clean Cumulative Data
df_Cumulative = df.rename(columns = {"Daily / Cumulative":"Cumulative"})
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

#Dump Data for Fast Access
grouped_daily.to_csv('Data/grouped_daily.csv', index=False )
grouped_daily_cities.to_csv('Data/grouped_daily_cities.csv', index=False)
grouped_daily_regions.to_csv('Data/grouped_daily_regions.csv', index=False)
grouped_cumulative.to_csv('Data/grouped_cumulative.csv', index=False)
grouped_cumulative_cities.to_csv('Data/grouped_cumulative_cities.csv', index=False)
grouped_cumulative_regions.to_csv('Data/grouped_cumulative_regions.csv', index=False)
grouped_daily_melt.to_csv('Data/grouped_daily_melt.csv', index=False)
grouped_daily_melt_cities.to_csv('Data/grouped_daily_melt_cities.csv', index=False)
grouped_daily_melt_regions.to_csv('Data/grouped_daily_melt_regions.csv', index=False)
grouped_cumulative_melt.to_csv('Data/grouped_cumulative_melt.csv', index=False)
grouped_cumulative_melt_cities.to_csv('Data/grouped_cumulative_melt_cities.csv', index=False)
grouped_cumulative_melt_regions.to_csv('Data/grouped_cumulative_melt_regions.csv', index=False)
grouped_daily_weekly.to_csv('Data/grouped_daily_weekly.csv', index=False)
grouped_daily_cities_weekly.to_csv('Data/grouped_daily_cities_weekly.csv', index=False)
grouped_daily_regions_weekly.to_csv('Data/grouped_daily_regions_weekly.csv', index=False)
grouped_cumulative_weekly.to_csv('Data/grouped_cumulative_weekly.csv', index=False)
df.to_csv('Data/df.csv', index=False)
df_Total.to_csv('Data/Total.csv', index=False)


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