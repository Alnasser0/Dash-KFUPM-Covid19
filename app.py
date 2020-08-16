# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

#AppAutomater.py has App graphs and data
#Graphs.py has all graphs
#Data.py has all data processing stuff
#Downloader.py is used to download files daily
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
#from apscheduler.schedulers.background import BackgroundScheduler
#import atexit
import plotly.express as px
import json
import numpy as np
import pandas as pd
from pymongo import MongoClient

#Scheduler to update data
###########################################################################
###########################################################################
def g():
    client = MongoClient("mongodb+srv://Alnasser0:test@covid19-kfupm.8orak.azure.mongodb.net/COVID19-KFUPM?retryWrites=true&w=majority")
    db = client['COVID19-KFUPM']
    collection = db['COVID19']
    #Read Only Needed Data
    ###########################################################################
    ###########################################################################
    grouped_daily_cities =  collection.find_one({"index":"grouped_daily_cities"})
    grouped_daily_cities = pd.DataFrame(grouped_daily_cities["data"])
    
    grouped_cumulative_cities =  collection.find_one({"index":"grouped_cumulative_cities"})
    grouped_cumulative_cities = pd.DataFrame(grouped_cumulative_cities["data"])
    
    g.grouped_daily_weekly =  collection.find_one({"index":"grouped_daily_weekly"})
    g.grouped_daily_weekly = pd.DataFrame(g.grouped_daily_weekly["data"])
    
    df =  collection.find_one({"index":"df"})
    df = pd.DataFrame(df["data"])
    # df=pd.read_csv('Data/df.csv')
    
    df_Total =  collection.find_one({"index":"df_Total"})
    df_Total = pd.DataFrame(df_Total["data"])
    # df_Total=pd.read_csv('Data/Total.csv')
    
    g.grouped_daily_regions =  collection.find_one({"index":"grouped_daily_regions"})
    g.grouped_daily_regions = pd.DataFrame(g.grouped_daily_regions["data"])
    # g.grouped_daily_regions=pd.read_csv('Data/grouped_daily_regions.csv')
    
    grouped_cumulative_melt =  collection.find_one({"index":"grouped_cumulative_melt"})
    grouped_cumulative_melt = pd.DataFrame(grouped_cumulative_melt["data"])
    # grouped_cumulative_melt=pd.read_csv('Data/grouped_cumulative_melt.csv')
    
    grouped_cumulative =  collection.find_one({"index":"grouped_cumulative"})
    grouped_cumulative = pd.DataFrame(grouped_cumulative["data"])
    # grouped_cumulative=pd.read_csv('Data/grouped_cumulative.csv')
    
    grouped_daily =  collection.find_one({"index":"grouped_daily"})
    grouped_daily = pd.DataFrame(grouped_daily["data"])
    # grouped_daily=pd.read_csv('Data/grouped_daily.csv')
    
    grouped_daily_melt =  collection.find_one({"index":"grouped_daily_melt"})
    grouped_daily_melt = pd.DataFrame(grouped_daily_melt["data"])
    # grouped_daily_melt=pd.read_csv('Data/grouped_daily_melt.csv')
    
    grouped_daily_cities_weekly =  collection.find_one({"index":"grouped_daily_cities_weekly"})
    grouped_daily_cities_weekly = pd.DataFrame(grouped_daily_cities_weekly["data"])
    # grouped_daily_cities_weekly=pd.read_csv('Data/grouped_daily_cities_weekly.csv')
    
    grouped_daily_regions_weekly =  collection.find_one({"index":"grouped_daily_regions_weekly"})
    grouped_daily_regions_weekly = pd.DataFrame(grouped_daily_regions_weekly["data"])
    # grouped_daily_regions_weekly=pd.read_csv('Data/grouped_daily_regions_weekly.csv')
    
    cnf, dth, rec, act = '#393e46', '#ff2e63', '#21bf73', '#fe9801' 


    #Total Summary of Last Reported Data
    ###########################################################################
    ###########################################################################
    g.Daily_Recoveries = df_Total.loc[(df_Total['Indicator'] == 'Recoveries') & (df_Total['Daily'] == 'Daily')].Cases.iloc[0]
    g.Daily_Mortalities = df_Total.loc[(df_Total['Indicator'] == 'Mortalities') & (df_Total['Daily'] == 'Daily')].Cases.iloc[0]
    g.Daily_Cases = df_Total.loc[(df_Total['Indicator'] == 'Cases') & (df_Total['Daily'] == 'Daily')].Cases.iloc[0]
    g.Cumulative_Active = df_Total.loc[(df_Total['Indicator'] == 'Active cases') & (df_Total['Daily'] == 'Cumulative')].Cases.iloc[0]
    g.Cumulative_Critical = df_Total.loc[(df_Total['Indicator'] == 'Critical cases') & (df_Total['Daily'] == 'Cumulative')].Cases.iloc[0]
    g.Cumulative_Cases = df_Total.loc[(df_Total['Indicator'] == 'Cases') & (df_Total['Daily'] == 'Cumulative')].Cases.iloc[0]


    #Parameters to be used
    ###########################################################################
    ###########################################################################
    count_cities=len(grouped_cumulative_cities.City.unique())
    g.available_regions = g.grouped_daily_regions['region'].unique()
    #FIGURES SECTION
    ###########################################################################
    ###########################################################################
    ###########################################################################

    #Name Convention: [Data type like Active, Mortalities, etc. if Daily:New, special:All]_[Graph Type ex Line or Bar or Scatter]_[Grouped By]_[Region: E if Eastren, else nothing]
    #Name Example: Active Cases represented in Bar Chart Grouped by City in the Eastern Region (Active_Bar_City_E)
    #Codes here are copied from Graphs python folder.

    g.NewCases_LineLog_E = px.line(g.grouped_daily_regions[g.grouped_daily_regions['region'] == 'Eastern Region'], x="Date", y="Cases", 
    title="Eastern Region Daily Confirmed Cases Over Time (Logarithmic Scale)", log_y=True, height=600)
    g.NewCases_LineLog_E.update_xaxes(rangeslider_visible=True)

    g.NewCases_Bar_E = px.bar(grouped_daily_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Cases')[grouped_daily_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Cases')['Cases'] >=1], height=600, x="Cases", y="City", title="New Cases", orientation='h')
    g.NewCases_Bar_E.update_layout(
    yaxis = dict(
    tickfont = dict(size=count_cities//3)))

    g.Cases_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Cases')[grouped_cumulative_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Cases').Cases > 50], height=600,x="Cases", y="City", 
    title="Aggregated Confirmed Cases of Eastern Region", orientation='h')
    g.Cases_Bar_City_E.update_layout(
    yaxis = dict(
    tickfont = dict(size=count_cities//3)))

    g.Count_Line_Cases_E = px.line(grouped_cumulative_melt, x="Date", y="Count", 
    title="Eastern Region Aggregated Cases - Line Plot", color="Case", height=600,color_discrete_sequence = [act, dth, rec])
    g.Count_Line_Cases_E.update_xaxes(rangeslider_visible=True)


    g.Count_BarArea_Cases_E = px.area(grouped_cumulative_melt, x="Date", y="Count", 
    title="Eastern Region Aggregated Cases - Area Plot", color="Case", height=600,color_discrete_sequence = [act, dth, rec])
    g.Count_BarArea_Cases_E.update_xaxes(rangeslider_visible=True)

    g.Active_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Active cases')[grouped_cumulative_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Active cases')['Active cases']>=1], 
    x="Active cases", y="City", title="Current Active Cases of Eastern Region", height=600,orientation='h')
    g.Active_Bar_City_E.update_layout(
    yaxis = dict(
    tickfont = dict(size=count_cities//4)))

    g.Active_Bar_E = px.bar(grouped_cumulative, x="Date", height=600,y="Active cases", 
    title="Eastern Region Active Cases Over Time")
    g.Active_Bar_E.update_xaxes(rangeslider_visible=True)

    g.NewMortalities_Bar_City_E = px.bar(grouped_daily_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Mortalities')[grouped_daily_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Mortalities').Mortalities >=1], height=600,x="Mortalities", y="City", 
    title="New Deaths", orientation='h')
    g.NewMortalities_Bar_City_E.update_layout(
    yaxis = dict(
    tickfont = dict(size=count_cities//2)))

    g.Mortalities_Bar_City_E = px.bar(grouped_cumulative_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Mortalities')[grouped_cumulative_cities.sort_values('Date', 
    ascending=True).tail(count_cities).sort_values('Mortalities').Mortalities >=1], height=600,x="Mortalities", y="City", 
    title="All Deaths", orientation='h')
    g.Mortalities_Bar_City_E.update_layout(
    yaxis = dict(
    tickfont = dict(size=count_cities//2)))

    g.NewMortalities_Bar_E = px.bar(grouped_daily, x="Date", y="Mortalities", 
    title="Eastern Region Daily Deaths Over Time", height=700,color_discrete_sequence=['#333333'])
    g.NewMortalities_Bar_E.update_xaxes(rangeslider_visible=True)

    g.Mortalities_Scatter_City_E = px.scatter(grouped_cumulative_cities.sort_values('Date', 
                    ascending=True).tail(count_cities).sort_values(['Cases', 'Mortalities']), 
                    x='Cases', y='Mortalities', color='City', size='Cases', height=700,
                    text='City', log_x=True, log_y=True, title='Deaths vs Confirmed (Scale is in log10)')
    g.Mortalities_Scatter_City_E.update_traces(textposition='top center')
    g.Mortalities_Scatter_City_E.update_layout(showlegend=False)
    g.Mortalities_Scatter_City_E.update_layout(xaxis_rangeslider_visible=True)


    g.RecoveryRate_Line_E = px.line(grouped_cumulative, height=600,x="Date", y="Recovary Percent", 
    title="Recovary Rate of Eastern Region Cases")
    g.RecoveryRate_Line_E.update_xaxes(rangeslider_visible=True)

    g.CFR_Line_E = px.line(grouped_cumulative[grouped_cumulative.Cases >= 100], height=600,x="Date", y="CFR Percent", 
    title="Cases Fetalitiy Ratio (CFR) of Eastern Region")
    g.CFR_Line_E.update_xaxes(rangeslider_visible=True)


    g.CFR_Line_City_E = px.line(grouped_cumulative_cities[grouped_cumulative_cities.Cases >= 10], 
    x="Date", y="CFR Percent", 
    title="Cases Fetalitiy Ratio (CFR) of Eastern Region' Cities", height=600,color='City')
    g.CFR_Line_City_E.update_xaxes(rangeslider_visible=True)

    g.Count_Bar_Cases_E = px.bar(grouped_daily_melt, height=600,x="Date", y="Count", 
    title="Eastern Region Daily Changes", color="Case", color_discrete_sequence = [act, dth, rec])
    g.Count_Bar_Cases_E.update_xaxes(rangeslider_visible=True)

    f = open('SAU-geo.json') 
    file = json.load(f)

    g.Active_Map_Region = px.choropleth(data_frame = df,
                        geojson=file,
                        locations="index",
                        color= "Active cases",  # value that varies
                        hover_name= "region",
                        featureidkey='properties.id',
                        color_continuous_scale="Viridis",  #  color scale
                        scope='asia',
                        title='Saudi Arabia Active Cases'
                        )
    g.Active_Map_Region.update_geos(center ={'lon': 45.0792, 'lat': 23.9959},
                lataxis_range= [15, 32], lonaxis_range=[33, 57])



    df = g.grouped_daily_weekly.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
    x_min=np.min(df['Cumulative Cases'])+1
    x_max=np.max(df['Cumulative Cases'])
    x_max+=x_max*10
    y_min=np.min(df['Cases'])+1
    y_max=np.max(df['Cases'])
    y_max+=y_max/10
    g.Intervention_Scatter_E = px.scatter(df, x='Cumulative Cases', y='Cases', 
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
    g.Intervention_Scatter_City_E = px.scatter(df, x='Cumulative Cases', y='Cases', 
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
    g.Intervention_Scatter_Region = px.scatter(df, x='Cumulative Cases', y='Cases', 
    title="Successful Intervention Rate of Saudi Arabia Regions", 
    size='Cumulative Cases', log_x=True, height=600,color='region', animation_frame='Date', 
    range_x=[x_min,x_max], range_y=[y_min,y_max])





    #END OF FIGURES
    ###########################################################################
    ###########################################################################
    ###########################################################################
#def Download_Data():
#    import Uploader
#def Data_Update():
#    import Data

g()
#scheduler = BackgroundScheduler()

#scheduler.add_job(func=Download_Data, trigger="interval", minutes=1410)
#scheduler.add_job(func=Data_Update, trigger="interval", minutes=1425)
#scheduler.add_job(func=g, trigger="interval", minutes=1440)
#scheduler.start()

# Shut down the scheduler when exiting the app
#atexit.register(lambda: scheduler.shutdown())

def Fixed_Graph(Graph):
    Graph.layout.xaxis.fixedrange = True
    Graph.layout.yaxis.fixedrange = True
    return Graph
#Functions
###########################################################################
###########################################################################

#Used to get values of a table
def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

#App settings
###########################################################################
###########################################################################
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server # the Flask app

#Tables
###########################################################################
###########################################################################
table = dbc.Table.from_dataframe(g.grouped_daily_weekly, striped=True, bordered=True, hover=True, id='Tables')


#Dropdowns
dropdown = html.Div([
            dcc.Dropdown(
                id='RegionSelector',
                options=get_options(g.available_regions),
                value='Eastern Region'
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'})
LogYesNo = html.Div([
            dcc.Dropdown(
                id='LogSelector',
                options=[
                    {'label': 'Turn on Logarithmic Scale', 'value': 'Yes'},
                    {'label': 'Turn off Logarithmic Scale', 'value': 'No'},
                ],
                value='Yes'
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'})

#Cards of Summary
###########################################################################
###########################################################################
first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Last Recoveries", className="card-title"),
            html.P("%5d"%g.Daily_Recoveries),
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
            html.P("%5d"%g.Daily_Mortalities),
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
            html.P("%5d"%g.Daily_Cases),
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
            html.P("%6d"%g.Cumulative_Active),        
        ]
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
            html.P("%5d"%g.Cumulative_Critical),
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
            html.P("%7d"%g.Cumulative_Cases),
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

#Graphs to use in App. Copied from AppAutomater.py
###########################################################################
###########################################################################
Graph1=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.NewCases_Bar_E) #grouped_daily_cities
        )
    )
Graph2=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Cases_Bar_City_E) #Cases_Bar_City_E
        )
    )
Graph3=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Count_BarArea_Cases_E) #df
        )
    )
Graph4=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Count_Line_Cases_E) #df
        )
    )
Graph5=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Active_Bar_City_E) #df
        )
    )
Graph6=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Active_Bar_E) #df
        )
    )
Graph7=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Mortalities_Bar_City_E)
        )
    )
Graph8=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.NewMortalities_Bar_City_E)
        )
    )
Graph9=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.NewMortalities_Bar_E)
        )
    )
Graph10=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Mortalities_Scatter_City_E)
        )
    )
Graph11=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Count_Bar_Cases_E)
        )
    )
Graph12=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.RecoveryRate_Line_E)
        )
    )
Graph13=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.CFR_Line_E)
        )
    )
Graph14=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.CFR_Line_City_E)
        )
    )
Graph15=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Intervention_Scatter_E)
        )
    )
Graph16=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Intervention_Scatter_City_E)
        )
    )
Graph17=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.Intervention_Scatter_Region)
        )
    )
Graph18=html.Div(
        dcc.Graph(
        figure=g.Active_Map_Region #df
        )
    )
Graph_DropDown=html.Div(
        dcc.Graph(
        figure=Fixed_Graph(g.NewCases_LineLog_E), #
        id='indicator-graphic'
        )
    )

#Layout of Graphs
###########################################################################
###########################################################################
row1 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph1),
                dbc.Col(Graph2),
            ],
        ),
    ]
)
row2 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph3),
                dbc.Col(Graph4),
            ],
        ),
    ]
)
row3 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph5),
                dbc.Col(Graph6),
            ],
        ),
    ]
)
row4 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph7),
                dbc.Col(Graph8),
            ],
        ),
    ]
)
row5 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph9),
                dbc.Col(Graph10),
            ],
        ),
    ]
)
row6 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph11),
                dbc.Col(Graph12),
            ],
        ),
    ]
)
row7 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph13),
                dbc.Col(Graph14),
            ],
        ),
    ]
)
row8 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph15),
                dbc.Col(Graph16),
            ],
        ),
    ]
)
row9 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph17),
            ],
        ),
    ]
)
row10 = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(Graph18),
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
        dbc.NavItem(dbc.NavLink("Charts", href="#indicator-graphic", external_link=True)),
        dbc.NavItem(dbc.NavLink("Maps", href="#Maps", external_link=True)),
        dbc.NavItem(dbc.NavLink("Tables", href="#Tables", external_link=True)),
        dbc.NavItem(dbc.NavLink("Simulation", href="#Simulation", external_link=True)),
    ],
    brand="KFUPM COVID19 Dashboard",
    brand_href="#",
    color="dark",
    dark=True,
    sticky='top',
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
    dbc.Alert("This is a dashboard that is used to analyze MOH data of COVID19 in Saudi Arabia. As it is an initial build, we are more focused on Eastern Region data analysis. Note that the dashboard is maintained by KFUPM, COE Department.", color="success"),
    className="p-5",
    ),
    cards,
    cards2,
    dropdown,
    LogYesNo,
    Graph_DropDown,
    row1,
    row2,
    row3,
    row4,
    row5,
    row6,
    row7,
    row8,
    row9,
    row10,
    dbc.Container(
    dbc.Alert("Eastern Region Weekly Data!", color="success"),
    className="text-center",
    ),
    html.Div(
        table
    ),
    html.Footer(
    dbc.Alert(
        [   "All Rights Reserved for Original Author, Alnasser, and KFUPM. Follow our ", 
            html.A("github", href="https://github.com/Alnasser0/Dash-KFUPM-Covid19"),
             " for more information."
        ],
        color="dark",
        className="text-center",
        #style="mb-0",
        )
    )
    #github for more information.
           # dbc.Alert(
           # [
           #     "This is a danger alert with an ",
           #     html.A("example link", href="#", className="alert-link"),
           # ],
           # color="danger",
]

)

#Callbacks

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('RegionSelector', 'value'),
    Input('LogSelector', 'value')])
def update_graph(value, value2):
    if(value2 == 'Yes'):
        graph = px.line(g.grouped_daily_regions[g.grouped_daily_regions['region'] == value], x="Date", y="Cases", 
        title="{} Region Daily Confirmed Cases Over Time".format(value), log_y=True)
        graph.update_xaxes(rangeslider_visible=True)
    else:
        graph = px.line(g.grouped_daily_regions[g.grouped_daily_regions['region'] == value], x="Date", y="Cases", 
        title="{} Region Daily Confirmed Cases Over Time".format(value))
        graph.update_xaxes(rangeslider_visible=True)
    return Fixed_Graph(graph)

#DOC initialization
app.layout = serve_layout

#Running server
if __name__ == '__main__':
    app.run_server(debug=True)