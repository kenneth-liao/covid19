# core component library (dcc)
from dash import dcc

# bootstrap components for custom layouts
import dash_bootstrap_components as dbc

# html component library (html)
from dash import html

# Input and Output objects for callback decorator
from dash.dependencies import Input, Output

# connect app.py file
from app import app

import pandas as pd
from plotly import graph_objects as go
import plotly.io as pio

# set the default theme for plotly
pio.templates.default = "presentation"

# style definitions for sidebar and main content
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "display": "inline-block"
}

# load data
data = pd.read_csv('data/owid-covid-data.csv')

sidebar = html.Div(
    dcc.Checklist(id='location',
                  value=['United States', 'United Kingdom', 'Germany', 'Canada', 'Italy'],
                  options=[{'label': c, 'value': c} for c in data.location.unique()]
                  ), style=SIDEBAR_STYLE
)

plotting_options = dbc.Row([
    dbc.Col(
        html.Div([
            html.H6('Metric'),
            dcc.Dropdown(id='metric', value='Confirmed cases', clearable=False,
                         options=[{'label': 'Confirmed cases', 'value': 'cases'}])
        ], style={'width': 250})
    ),
    dbc.Col(
        html.Div([
            html.H6('Interval'),
            dcc.Dropdown(id='interval', value='Cumulative', clearable=False,
                         options=[{'label': 'Cumulative', 'value': 'total'}])
        ], style={'width': 250})
    ),
    dbc.Col(
        html.Div([
            dcc.Checklist(id='relative', value='Cumulative',
                          options=[{'label': ' Relative to Population', 'value': 'relative'}])
        ]), align='end'
    ),
    dbc.Col(

    ),
])

app.layout = html.Div([
    html.H1('COVID-19 Global Data Tracking'),
    # the Location component stores the url in the address bar
    dcc.Location(id='url', refresh=False),


    dbc.Row([
        dbc.Col(sidebar, width=2),

        dbc.Col([
            plotting_options,

            # graph object which will display the data view
            html.Div(dcc.Graph(id='visualization', figure={})),

            # bottom navigation menu
            html.Div([

            ])
        ])
    ])
])


@app.callback(Output('visualization', 'figure'),
              [Input('location', 'value'),
               Input('metric', 'value')])
def update_figure(location, metric):
    traces = []
    for country in location:
        traces.append(
            go.Scatter(name=country, mode='markers+lines',
                       x=data[data['location'] == country]['date'],
                       y=data[data['location'] == country].total_cases)
        )

    fig = go.Figure(data=traces)
    fig.update_traces(marker={'size': 3}, line={'width': 1})
    fig.update_layout(hovermode='x', showlegend=True)

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
