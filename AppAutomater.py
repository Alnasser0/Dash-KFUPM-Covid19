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
grouped_daily_regions=pd.read_csv('Data/grouped_daily_regions.csv')
grouped_cumulative_melt=pd.read_csv('Data/grouped_cumulative_melt.csv')
grouped_cumulative=pd.read_csv('Data/grouped_cumulative.csv')
grouped_daily=pd.read_csv('Data/grouped_daily.csv')
grouped_daily_melt=pd.read_csv('Data/grouped_daily_melt.csv')
grouped_daily_cities_weekly=pd.read_csv('Data/grouped_daily_cities_weekly.csv')
grouped_daily_regions_weekly=pd.read_csv('Data/grouped_daily_regions_weekly.csv')
cnf, dth, rec, act = '#393e46', '#ff2e63', '#21bf73', '#fe9801' 


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
title="Eastern Region Daily Confirmed Cases Over Time (Logarithmic Scale)", log_y=True, height=600)
NewCases_LineLog_E.update_xaxes(rangeslider_visible=True)

NewCases_Bar_E = px.bar(grouped_daily_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases')[grouped_daily_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases')['Cases'] >=1], height=600, x="Cases", y="City", title="New Cases", orientation='h')
NewCases_Bar_E.update_layout(
yaxis = dict(
tickfont = dict(size=count_cities//3)))

Cases_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases')[grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases').Cases > 50], height=600,x="Cases", y="City", 
title="Aggregated Confirmed Cases of Eastern Region", orientation='h')
Cases_Bar_City_E.update_layout(
yaxis = dict(
tickfont = dict(size=count_cities//3)))

Count_Line_Cases_E = px.line(grouped_cumulative_melt, x="Date", y="Count", 
title="Eastern Region Aggregated Cases - Line Plot", color="Case", height=600,color_discrete_sequence = [act, dth, rec])
Count_Line_Cases_E.update_xaxes(rangeslider_visible=True)


Count_BarArea_Cases_E = px.area(grouped_cumulative_melt, x="Date", y="Count", 
title="Eastern Region Aggregated Cases - Area Plot", color="Case", height=600,color_discrete_sequence = [act, dth, rec])
Count_BarArea_Cases_E.update_xaxes(rangeslider_visible=True)

Active_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Active cases')[grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Active cases')['Active cases']>=1], 
x="Active cases", y="City", title="Current Active Cases of Eastern Region", height=600,orientation='h')
Active_Bar_City_E.update_layout(
yaxis = dict(
tickfont = dict(size=count_cities//4)))

Active_Bar_E = px.bar(grouped_cumulative, x="Date", height=600,y="Active cases", 
title="Eastern Region Active Cases Over Time")
Active_Bar_E.update_xaxes(rangeslider_visible=True)

NewMortalities_Bar_City_E = px.bar(grouped_daily_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Mortalities')[grouped_daily_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Mortalities').Mortalities >=1], height=600,x="Mortalities", y="City", 
title="New Deaths", orientation='h')

Mortalities_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Mortalities')[grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Mortalities').Mortalities >=1], height=600,x="Mortalities", y="City", 
title="All Deaths", orientation='h')
Mortalities_Bar_City_E.update_layout(
yaxis = dict(
tickfont = dict(size=count_cities//2)))

NewMortalities_Bar_E = px.bar(grouped_daily, x="Date", y="Mortalities", 
title="Eastern Region Daily Deaths Over Time", height=700,color_discrete_sequence=['#333333'])
NewMortalities_Bar_E.update_xaxes(rangeslider_visible=True)

Mortalities_Scatter_City_E = px.scatter(grouped_cumulative_cities.sort_values('Date', 
                ascending=True).tail(count_cities).sort_values(['Cases', 'Mortalities']), 
                 x='Cases', y='Mortalities', color='City', size='Cases', height=700,
                 text='City', log_x=True, log_y=True, title='Deaths vs Confirmed (Scale is in log10)')
Mortalities_Scatter_City_E.update_traces(textposition='top center')
Mortalities_Scatter_City_E.update_layout(showlegend=False)
Mortalities_Scatter_City_E.update_layout(xaxis_rangeslider_visible=True)


RecoveryRate_Line_E = px.line(grouped_cumulative, height=600,x="Date", y="Recovary Percent", 
title="Recovary Rate of Eastern Region Cases")
RecoveryRate_Line_E.update_xaxes(rangeslider_visible=True)

CFR_Line_E = px.line(grouped_cumulative[grouped_cumulative.Cases >= 100], height=600,x="Date", y="CFR Percent", 
title="Cases Fetalitiy Ratio (CFR) of Eastern Region")
CFR_Line_E.update_xaxes(rangeslider_visible=True)


CFR_Line_City_E = px.line(grouped_cumulative_cities[grouped_cumulative_cities.Cases >= 10], 
x="Date", y="CFR Percent", 
title="Cases Fetalitiy Ratio (CFR) of Eastern Region' Cities", height=600,color='City')
CFR_Line_City_E.update_xaxes(rangeslider_visible=True)

Count_Bar_Cases_E = px.bar(grouped_daily_melt, height=600,x="Date", y="Count", 
title="Eastern Region Daily Changes", color="Case", color_discrete_sequence = [act, dth, rec])
Count_Bar_Cases_E.update_xaxes(rangeslider_visible=True)

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



df = grouped_daily_weekly.copy()
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
x_min=np.min(df['Cumulative Cases'])+1
x_max=np.max(df['Cumulative Cases'])
x_max+=x_max*10
y_min=np.min(df['Cases'])+1
y_max=np.max(df['Cases'])
y_max+=y_max/10
Intervention_Scatter_E = px.scatter(df, x='Cumulative Cases', y='Cases', 
title="Successful Intervention Rate of Eastern Region", 
size='Cumulative Cases', animation_frame='Date', height=600,log_x=True, range_x=[x_min,x_max], 
range_y=[y_min,y_max])


df = grouped_daily_cities_weekly.copy()
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
x_min=np.min(df['Cumulative Cases'])+1
x_max=np.max(df['Cumulative Cases'])
x_max+=x_max*10
y_min=np.min(df['Cases'])+1
y_max=np.max(df['Cases'])
y_max+=y_max/10
Intervention_Scatter_City_E = px.scatter(df, x='Cumulative Cases', y='Cases', 
title="Successful Intervention Rate of Eastern Region cities", 
log_x=True, size='Cumulative Cases', height=600,color='City', animation_frame='Date', 
range_x=[x_min,x_max], range_y=[y_min,y_max])


df = grouped_daily_regions_weekly.copy()
df['Date'] = pd.to_datetime(df['Date'])
df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
x_min=np.min(df['Cumulative Cases'])+1
x_max=np.max(df['Cumulative Cases'])
x_max+=x_max*10
y_min=np.min(df['Cases'])+1
y_max=np.max(df['Cases'])
y_max+=y_max/10
Intervention_Scatter_Region = px.scatter(df, x='Cumulative Cases', y='Cases', 
title="Successful Intervention Rate of Saudi Arabia Regions", 
size='Cumulative Cases', log_x=True, height=600,color='region', animation_frame='Date', 
range_x=[x_min,x_max], range_y=[y_min,y_max])





#END OF FIGURES
###########################################################################
###########################################################################
###########################################################################