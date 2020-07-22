# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np
import json

#Graphs
#######################################################
#######################################################
#######################################################
cnf, dth, rec, act = '#393e46', '#ff2e63', '#21bf73', '#fe9801' 

#Read Data
grouped_daily=pd.read_csv('Data/grouped_daily.csv', engine='python')
grouped_daily_cities=pd.read_csv('Data/grouped_daily_cities.csv', engine='python')
grouped_daily_regions=pd.read_csv('Data/grouped_daily_regions.csv', engine='python')
grouped_cumulative=pd.read_csv('Data/grouped_cumulative.csv', engine='python')
grouped_cumulative_cities=pd.read_csv('Data/grouped_cumulative_cities.csv', engine='python')
grouped_cumulative_regions=pd.read_csv('Data/grouped_cumulative_regions.csv', engine='python')
grouped_daily_melt=pd.read_csv('Data/grouped_daily_melt.csv', engine='python')
grouped_daily_melt_cities=pd.read_csv('Data/grouped_daily_melt_cities.csv', engine='python')
grouped_daily_melt_regions=pd.read_csv('Data/grouped_daily_melt_regions.csv', engine='python')
grouped_cumulative_melt=pd.read_csv('Data/grouped_cumulative_melt.csv', engine='python')
grouped_cumulative_melt_cities=pd.read_csv('Data/grouped_cumulative_melt_cities.csv', engine='python')
grouped_cumulative_melt_regions=pd.read_csv('Data/grouped_cumulative_melt_regions.csv', engine='python')
grouped_daily_weekly=pd.read_csv('Data/grouped_daily_weekly.csv', engine='python')
grouped_daily_cities_weekly=pd.read_csv('Data/grouped_daily_cities_weekly.csv', engine='python')
grouped_daily_regions_weekly=pd.read_csv('Data/grouped_daily_regions_weekly.csv', engine='python')
grouped_cumulative_weekly=pd.read_csv('Data/grouped_cumulative_weekly.csv', engine='python')
df=pd.read_csv('Data/df.csv', engine='python')

count_cities=len(grouped_cumulative_cities.City.unique())
#FIGURES
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################

#Name Convention: [Data type like Active, Mortalities, etc. if Daily:New, special:All]_[Graph Type ex Line or Bar or Scatter]_[Grouped By]_[Region: E if Eastren, else nothing]
#Name Example: Active Cases represented in Bar Chart Grouped by City in the Eastern Region (Active_Bar_City_E)
Active_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Active cases'), 
x="Active cases", y="City", title="Current Active Cases", orientation='h')

Active_Bar_E = px.bar(grouped_cumulative, x="Date", y="Active cases", 
title="Eastern Region Active Cases Over Time")
Active_Bar_E.update_xaxes(rangeslider_visible=True)


NewCases_Bar_E = px.bar(grouped_daily_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases'), x="Cases", y="City", title="New Cases", orientation='h')

Cases_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases'), x="Cases", y="City", 
title="Aggregated Confirmed Cases", orientation='h')


NewCases_Bar_E = px.bar(grouped_daily, x="Date", y="Cases", 
title="Eastern Region Daily Confirmed Cases Over Time")
NewCases_Bar_E.update_xaxes(rangeslider_visible=True)


NewCases_LineLog_E = px.line(grouped_daily, x="Date", y="Cases", 
title="Eastern Region Daily Confirmed Cases Over Time (Logarithmic Scale)", log_y=True)
NewCases_LineLog_E.update_xaxes(rangeslider_visible=True)


NewMortalities_Bar_City_E = px.bar(grouped_daily_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Mortalities'), x="Mortalities", y="City", 
title="New Deaths", orientation='h')


Mortalities_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Mortalities'), x="Mortalities", y="City", 
title="All Deaths", orientation='h')


NewMortalities_Bar_E = px.bar(grouped_daily, x="Date", y="Mortalities", 
title="Eastern Region Daily Deaths Over Time", color_discrete_sequence=['#333333'])
NewMortalities_Bar_E.update_xaxes(rangeslider_visible=True)


Count_Bar_Cases_E = px.bar(grouped_daily_melt, x="Date", y="Count", 
title="Eastern Region Daily Changes", color="Case", color_discrete_sequence = [act, dth, rec])
Count_Bar_Cases_E.update_xaxes(rangeslider_visible=True)


Count_Line_Cases_E = px.line(grouped_cumulative_melt, x="Date", y="Count", 
title="Eastern Region Aggregated Cases - Line Plot", color="Case", color_discrete_sequence = [act, dth, rec])
Count_Line_Cases_E.update_xaxes(rangeslider_visible=True)


Count_BarArea_Cases_E = px.area(grouped_cumulative_melt, x="Date", y="Count", 
title="Eastern Region Aggregated Cases - Area Plot", color="Case", color_discrete_sequence = [act, dth, rec])
Count_BarArea_Cases_E.update_xaxes(rangeslider_visible=True)


Mortalities_Scatter_City_E = px.scatter(grouped_cumulative_cities.sort_values('Date', 
                ascending=True).tail(count_cities).sort_values(['Cases', 'Mortalities']), 
                 x='Cases', y='Mortalities', color='City', size='Cases', height=700,
                 text='City', log_x=True, log_y=True, title='Deaths vs Confirmed (Scale is in log10)')
Mortalities_Scatter_City_E.update_traces(textposition='top center')
Mortalities_Scatter_City_E.update_layout(showlegend=False)
Mortalities_Scatter_City_E.update_layout(xaxis_rangeslider_visible=True)


RecoveryRate_Line_E = px.line(grouped_cumulative, x="Date", y="Recovary Percent", 
title="Recovary Ratio of Eastern Region Cases")
RecoveryRate_Line_E.update_xaxes(rangeslider_visible=True)


CFR_Line_E = px.line(grouped_cumulative[grouped_cumulative.Cases >= 100], x="Date", y="CFR Percent", 
title="Cases Fetalitiy Ratio (CFR) of Eastern Region When Cases > 100")
CFR_Line_E.update_xaxes(rangeslider_visible=True)


CFR_Line_City_E = px.line(grouped_cumulative_cities[grouped_cumulative_cities.Cases >= 10], 
x="Date", y="CFR Percent", 
title="Cases Fetalitiy Ratio (CFR) when cases >10", color='City')
CFR_Line_City_E.update_xaxes(rangeslider_visible=True)


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
size='Cumulative Cases', animation_frame='Date', log_x=True, range_x=[x_min,x_max], 
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
log_x=True, size='Cumulative Cases', color='City', animation_frame='Date', 
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
size='Cumulative Cases', log_x=True, color='region', animation_frame='Date', 
range_x=[x_min,x_max], range_y=[y_min,y_max])


#END OF FIGURES
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################
###########################################################################


#######################################################
#######################################################
#######################################################


#App settings
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server # the Flask app

#Tables
table = dbc.Table.from_dataframe(grouped_daily_weekly, striped=True, bordered=True, hover=True)

#Cards
first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P("This card has some text content, but not much else"),
        ]
    ),
    className="ml-3 mb-3",
    style={
 #       'margin': 20, 
    },
)
second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Second Card title", className="card-title"),
            html.P(
                "Second Card"
            ),
        ]
    ),
    className="mb-3",
    style={
 #       'margin': 20, 
    },
)
third_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Third Card title", className="card-title"),
            html.P(
                "tEST"
            ),
        ]
    ),
    className="mb-3",
    style={
 #       'margin': 20, 
    },
)
cards = dbc.Row([dbc.Col(first_card, width=4), dbc.Col(second_card, width=4), dbc.Col(third_card, width=4)])
cards2 = dbc.Row([dbc.Col(first_card, width=4), dbc.Col(second_card, width=4), dbc.Col(third_card, width=4)])

#Graphs
Graph1=html.Div(
        dcc.Graph(
        id='example-graph',
        figure=NewCases_Bar_E
        )
    )
Graph2=html.Div(
        dcc.Graph(
        id='example-graph2',
        figure=Active_Map_Region
        )
    )

#Rows
row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph1),
                dbc.Col(Graph2),
            ]
        ),
    ]
)

#Layout of DOC
def serve_layout():
    return html.Div(children=[
    html.Img(
        src=app.get_asset_url('1200px-King_Fahd_University_of_Petroleum_&_Minerals_Logo.svg.png'),
        style={
            'width': 150, 
            'height': 150,
            'margin-left': 'auto',
            'margin-right': 'auto',
            'margin-top': 30,
            "display": "block"
        },
        
    ),
    dbc.Container(
    dbc.Alert("This is a Dashboard that is used to analyze MOH data of COVID19 in Saudi Arabia. It is maintained by KFUPM, COE Department.", color="success"),
    className="p-5",
    ),
    cards,
    cards2,
    row,
    html.Div(
        table
    ),
    html.Footer(
    dbc.Alert("This is a Footer", color="success")
    )
]

)

#DOC initialization
app.layout = serve_layout

#Running server
if __name__ == '__main__':
    app.run_server(debug=True)