# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import Graphs as g

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server # the Flask app



app.layout = html.Div(children=[
    html.Img(
        src=app.get_asset_url('1200px-King_Fahd_University_of_Petroleum_&_Minerals_Logo.svg.png'),
        style={
            'width': 200, 
            'height': 200,
            'margin-left': 'auto',
            'margin-right': 'auto',
            "display": "block"
        },
        
    ),
    dbc.Container(
    dbc.Alert("This is a Dashboard that is used to analyze MOH data of COVID19 in Saudi Arabia. It is maintained by KFUPM, COE Department.", color="success"),
    className="p-5",
    ),
    html.Div(
        dcc.Graph(
        id='example-graph',
        figure=g.NewCases_Bar_E
        )
    ),
    html.Div(
        dcc.Graph(
        id='example-graph2',
        figure=g.Active_Map_Region
        )
    )
]

)

if __name__ == '__main__':
    app.run_server(debug=True)