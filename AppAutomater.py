import plotly.express as px
import pandas as pd
import numpy as np
import json

#Read Only Needed Data
###########################################################################
###########################################################################
grouped_daily_cities=pd.read_csv('Data/grouped_daily_cities.csv')
grouped_cumulative_cities=pd.read_csv('Data/grouped_cumulative_cities.csv')
grouped_daily_weekly=pd.read_csv('Data/grouped_daily_weekly.csv')
df=pd.read_csv('Data/df.csv')
df_Total=pd.read_csv('Data/Total.csv')
grouped_daily_regions=pd.read_csv('Data/grouped_daily_regions.csv', engine='python')
#Total Summary of Last Reported Data
###########################################################################
###########################################################################
Daily_Recoveries = df_Total.loc[(df_Total['Indicator'] == 'Recoveries') & (df_Total['Daily'] == 'Daily')].Cases.iloc[0]
Daily_Mortalities = df_Total.loc[(df_Total['Indicator'] == 'Mortalities') & (df_Total['Daily'] == 'Daily')].Cases.iloc[0]
Daily_Cases = df_Total.loc[(df_Total['Indicator'] == 'Cases') & (df_Total['Daily'] == 'Daily')].Cases.iloc[0]
Cumulative_Active = df_Total.loc[(df_Total['Indicator'] == 'Active cases') & (df_Total['Daily'] == 'Cumulative')].Cases.iloc[0]
Cumulative_Critical = df_Total.loc[(df_Total['Indicator'] == 'Critical cases') & (df_Total['Daily'] == 'Cumulative')].Cases.iloc[0]
Cumulative_Cases = df_Total.loc[(df_Total['Indicator'] == 'Cases') & (df_Total['Daily'] == 'Cumulative')].Cases.iloc[0]


#Parameters to be used
###########################################################################
###########################################################################
count_cities=len(grouped_cumulative_cities.City.unique())
available_regions = grouped_daily_regions['region'].unique()

#FIGURES SECTION
###########################################################################
###########################################################################
###########################################################################

#Name Convention: [Data type like Active, Mortalities, etc. if Daily:New, special:All]_[Graph Type ex Line or Bar or Scatter]_[Grouped By]_[Region: E if Eastren, else nothing]
#Name Example: Active Cases represented in Bar Chart Grouped by City in the Eastern Region (Active_Bar_City_E)
#Codes here are copied from Graphs python folder.

NewCases_LineLog_E = px.line(grouped_daily_regions[grouped_daily_regions['region'] == 'Eastern Region'], x="Date", y="Cases", 
title="Eastern Region Daily Confirmed Cases Over Time (Logarithmic Scale)", log_y=True)
NewCases_LineLog_E.update_xaxes(rangeslider_visible=True)

NewCases_Bar_E = px.bar(grouped_daily_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases'), x="Cases", y="City", title="New Cases", orientation='h')
NewCases_Bar_E.update_layout(
yaxis = dict(
tickfont = dict(size=7)))

Cases_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases')[grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases').Cases > 50], x="Cases", y="City", 
title="Aggregated Confirmed Cases", orientation='h')
Cases_Bar_City_E.update_layout(
yaxis = dict(
tickfont = dict(size=7)))

f = open('SAU-geo.json') 
file = json.load(f)

Active_Map_Region = px.choropleth(data_frame = df,
                    geojson=file,
                    locations="index",
                    color= "Active cases",  # value that varies
                    hover_name= "region",
                    featureidkey='properties.id',
                    color_continuous_scale="Viridis",  #  color scale
                    scope='asia',
                    title='Saudi Arabia Active Cases'
                    )
Active_Map_Region.update_geos(center ={'lon': 45.0792, 'lat': 23.9959},
               lataxis_range= [15, 32], lonaxis_range=[33, 57])


#END OF FIGURES
###########################################################################
###########################################################################
###########################################################################