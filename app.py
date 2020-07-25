# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
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

#Total Summary of Last Reported Data
###########################################################################
###########################################################################
Daily_Recoveries = df_Total.loc[(df_Total['Indicator'] == 'Recoveries') & (df_Total['Daily'] == 'Daily')].Cases.iloc[0]
Daily_Mortalities = df_Total.loc[(df_Total['Indicator'] == 'Mortalities') & (df_Total['Daily'] == 'Daily')].Cases.iloc[0]
Daily_Cases = df_Total.loc[(df_Total['Indicator'] == 'Cases') & (df_Total['Daily'] == 'Daily')].Cases.iloc[0]
Cumulative_Active = df_Total.loc[(df_Total['Indicator'] == 'Active cases') & (df_Total['Daily'] == 'Cumulative')].Cases.iloc[0]
Cumulative_Critical = df_Total.loc[(df_Total['Indicator'] == 'Critical cases') & (df_Total['Daily'] == 'Cumulative')].Cases.iloc[0]
Cumulative_Cases = df_Total.loc[(df_Total['Indicator'] == 'Cases') & (df_Total['Daily'] == 'Cumulative')].Cases.iloc[0]

#Changing variable of Eastern Regions cities since the data is not fixed.
###########################################################################
###########################################################################
count_cities=len(grouped_cumulative_cities.City.unique())


#FIGURES SECTION
###########################################################################
###########################################################################
###########################################################################

#Name Convention: [Data type like Active, Mortalities, etc. if Daily:New, special:All]_[Graph Type ex Line or Bar or Scatter]_[Grouped By]_[Region: E if Eastren, else nothing]
#Name Example: Active Cases represented in Bar Chart Grouped by City in the Eastern Region (Active_Bar_City_E)
#Codes here are copied from Graphs python folder.

NewCases_Bar_E = px.bar(grouped_daily_cities.sort_values('Date', 
ascending=True).tail(count_cities).sort_values('Cases'), x="Cases", y="City", title="New Cases", orientation='h')

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


#App settings
###########################################################################
###########################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server # the Flask app

#Tables
###########################################################################
###########################################################################
table = dbc.Table.from_dataframe(grouped_daily_weekly, striped=True, bordered=True, hover=True, id='Tables')

#Cards of Summary
###########################################################################
###########################################################################
first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Last Recoveries", className="card-title"),
            html.P("%5d"%Daily_Recoveries),
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
            html.H5("Last Mortalities", className="card-title"),
            html.P("%5d"%Daily_Mortalities),
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
            html.H5("Last Cases", className="card-title"),
            html.P("%5d"%Daily_Cases),
        ]
    ),
    className="mb-3",
    style={
 #       'margin': 20, 
    },
)
#End of Row 1 in Summary
###########################################################################
###########################################################################
Fourth_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Total Active", className="card-title"),
            html.P("%6d"%Cumulative_Active),        ]
    ),
    className="ml-3 mb-3",
    style={
 #       'margin': 20, 
    },
)
Fifth_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Critical Cases", className="card-title"),
            html.P("%5d"%Cumulative_Critical),
        ]
    ),
    className="mb-3",
    style={
 #       'margin': 20, 
    },
)
Sixth_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("All Cases", className="card-title"),
            html.P("%7d"%Cumulative_Cases),
        ]
    ),
    className="mb-3",
    style={
 #       'margin': 20, 
    },
)
cards = dbc.Row([dbc.Col(first_card, width=4), dbc.Col(second_card, width=4), dbc.Col(third_card, width=4)], id='Summary')
cards2 = dbc.Row([dbc.Col(Fourth_card, width=4), dbc.Col(Fifth_card, width=4), dbc.Col(Sixth_card, width=4)])

#End of Summary Cards
###########################################################################
###########################################################################

#Graphs to use in App. Copied from Graphs.py
###########################################################################
###########################################################################
Graph1=html.Div(
        dcc.Graph(
        figure=NewCases_Bar_E #grouped_daily_cities
        )
    )
Graph2=html.Div(
        dcc.Graph(
        figure=Cases_Bar_City_E #Cases_Bar_City_E
        )
    )
Graph3=html.Div(
        dcc.Graph(
        figure=Active_Map_Region #df
        )
    )

#Layout of Graphs
###########################################################################
###########################################################################
row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph1),
                dbc.Col(Graph2),
            ],
            id='Graphs',
        ),
    ]
)
row2 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph3),
            ],
            id='Maps',
        ),
    ]
)

#NavBar
###########################################################################
###########################################################################
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Summary", href="#Summary", external_link=True)),
        dbc.NavItem(dbc.NavLink("Charts", href="#Graphs", external_link=True)),
        dbc.NavItem(dbc.NavLink("Maps", href="#Maps", external_link=True)),
        dbc.NavItem(dbc.NavLink("Tables", href="#Tables", external_link=True)),
        dbc.NavItem(dbc.NavLink("Simulation", href="#Simulation", external_link=True)),
    ],
    brand="KFUPM COVID19 Dashboard",
    brand_href="#",
    color="dark",
    dark=True,
   # sticky='top',
)

#Layout of HTML DOC
###########################################################################
###########################################################################
def serve_layout():
    return html.Div(children=[
    navbar,
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
    row2,
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