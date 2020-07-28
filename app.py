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
import AppAutomater as g
from dash.dependencies import Input, Output
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import plotly.express as px
scheduler = BackgroundScheduler()

#Scheduler to update data
###########################################################################
###########################################################################
def Update_Import():
    import AppAutomater as g

scheduler = BackgroundScheduler()
scheduler.add_job(func=Update_Import, trigger="interval", days=1)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

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
        figure=g.NewCases_Bar_E #grouped_daily_cities
        )
    )
Graph2=html.Div(
        dcc.Graph(
        figure=g.Cases_Bar_City_E #Cases_Bar_City_E
        )
    )
Graph3=html.Div(
        dcc.Graph(
        figure=g.Count_BarArea_Cases_E #df
        )
    )
Graph4=html.Div(
        dcc.Graph(
        figure=g.Count_Line_Cases_E #df
        )
    )
Graph5=html.Div(
        dcc.Graph(
        figure=g.Active_Bar_City_E #df
        )
    )
Graph6=html.Div(
        dcc.Graph(
        figure=g.Active_Bar_E #df
        )
    )
Graph7=html.Div(
        dcc.Graph(
        figure=g.Mortalities_Bar_City_E
        )
    )
Graph8=html.Div(
        dcc.Graph(
        figure=g.NewMortalities_Bar_City_E
        )
    )
Graph9=html.Div(
        dcc.Graph(
        figure=g.NewMortalities_Bar_E
        )
    )
Graph10=html.Div(
        dcc.Graph(
        figure=g.Mortalities_Scatter_City_E
        )
    )
Graph11=html.Div(
        dcc.Graph(
        figure=g.Count_Bar_Cases_E
        )
    )
Graph12=html.Div(
        dcc.Graph(
        figure=g.RecoveryRate_Line_E
        )
    )
Graph13=html.Div(
        dcc.Graph(
        figure=g.CFR_Line_E
        )
    )
Graph14=html.Div(
        dcc.Graph(
        figure=g.CFR_Line_City_E
        )
    )
Graph15=html.Div(
        dcc.Graph(
        figure=g.Intervention_Scatter_E
        )
    )
Graph16=html.Div(
        dcc.Graph(
        figure=g.Intervention_Scatter_City_E
        )
    )
Graph17=html.Div(
        dcc.Graph(
        figure=g.Intervention_Scatter_Region
        )
    )
Graph18=html.Div(
        dcc.Graph(
        figure=g.Active_Map_Region #df
        )
    )
Graph_DropDown=html.Div(
        dcc.Graph(
        figure=g.NewCases_LineLog_E, #
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
    html.Div(
        table
    ),
    html.Footer(
    dbc.Alert(
        [   "All Rights Reserved for Original Author, Alnasser Abdullah, and KFUPM. Follow our ", 
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
    return graph

#DOC initialization
app.layout = serve_layout

#Running server
if __name__ == '__main__':
    app.run_server(debug=True)