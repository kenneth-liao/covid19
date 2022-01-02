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
    #"position": "fixed",
    #"top": 70,
    #"left": 0,
    "bottom": 70,
    "width": "25rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "scroll"
}

CONTENT_STYLE = {
    #"position": "fixed",
    "top": 70,
    "left": 300,
    "bottom": 70,
    "margin-left": "2rem",
    "padding": "2rem 1rem"
}

# load data
data = pd.read_csv('data/owid-covid-data.csv')

# define the various cards that will be displayed in the app
title = dbc.Card(
    dbc.CardBody(
        html.H1('COVID-19 Global Data Tracking')
    ), color='#4F33FF'
)

location_sidebar = dbc.Card(
    dbc.CardBody(
        dcc.Checklist(id='location',
                      value=['United States', 'United Kingdom', 'Germany', 'Canada', 'Italy'],
                      options=[{'label': c, 'value': c} for c in data.location.unique()]
                      )
    ), style={'width': '20rem'}, color='#FF7A33'
)

plotting_options = dbc.CardGroup([
    dbc.Card(
            dbc.CardBody([
                html.H6('Metric'),
                dcc.Dropdown(id='metric', value='Confirmed cases', clearable=False,
                             options=[{'label': 'Confirmed cases', 'value': 'cases'}])
            ])

    ),
    dbc.Card(
            dbc.CardBody([
                html.H6('Interval'),
                dcc.Dropdown(id='interval', value='Cumulative', clearable=False,
                             options=[{'label': 'Cumulative', 'value': 'total'}])
            ])
    ),
    dbc.Card(
            dbc.CardBody(
                dcc.Checklist(id='relative', value='Cumulative',
                              options=[{'label': ' Relative to Population', 'value': 'relative'}])
            )
    )
], style={'width': '70rem'})





graph = dbc.Card(
    dbc.CardBody(
        html.Div(dcc.Graph(id='visualization', figure={}))
    ), color='#3396FF'
)



app.layout = html.Div([
    # # the Location component stores the url in the address bar
    # dcc.Location(id='url', refresh=False),
    #
    #
    # dbc.Row([
    #     dbc.Col(sidebar, width=2),
    #
    #     dbc.Col(
    #         html.Div([
    #             plotting_options,
    #
    #             # graph object which will display the data view
    #             dbc.Row(
    #                 dbc.Col(
    #                     html.Div(dcc.Graph(id='visualization', figure={})),
    #                 )
    #             ),
    #
    #             # bottom navigation menu
    #             dbc.Row(
    #                 dbc.Col(
    #                     html.Div([
    #
    #                     ])
    #                 )
    #             )
    #         ], style=CONTENT_STYLE)
    #     )
    # ])
    dbc.Row(title),
    dbc.Row([
        dbc.Col(location_sidebar, width='auto'),
        dbc.Col([
            dbc.Row(plotting_options),
            dbc.Row(graph)], width=8)
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
    fig.update_layout(hovermode='x', showlegend=True, height=800)

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
