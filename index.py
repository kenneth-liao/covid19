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


# USER DEFINED STYLE SETTINGS #
app_width = 8
##################
margin = (12-app_width)/2


# load data
data = pd.read_csv('data/owid-covid-data.csv')


# define the various cards that will be displayed in the app
def location_checklist():
    return dcc.Checklist(
        id='location', value=['United States', 'United Kingdom', 'Germany', 'Canada', 'Italy'],
        options=[{'label': c, 'value': c} for c in data.location.unique()]
    )


def visualization():
    return dcc.Graph(
        id='visualization', figure={}
    )


app.layout = html.Div([
    # the Location component stores the url in the address bar
    dcc.Location(id='url', refresh=False),

    dbc.Row(  # title
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    html.H1('COVID-19 Global Data Dashboard')
                ), className='mb-4', style={'background-color': '#FF6E33'}
            ), width={'size': app_width, 'offset': margin}
        )
    ),

    dbc.Row([  # logo & plotting options
        dbc.Col(  # logo
            dbc.Card(
                dbc.CardBody(
                    html.H1('Logo')
                ), className='mb-2'
            ), width={'size': 2, 'offset': margin}
        ),
        dbc.Col([  # plotting options
            dbc.CardGroup([
                dbc.Card(
                    dbc.CardBody(
                        html.H4('Metric')
                    )
                ),
                dbc.Card(
                    dbc.CardBody(
                        html.H4('Interval')
                    )
                ),
                dbc.Card(
                    dbc.CardBody(
                        html.H4('Relative to Population')
                    )
                ),
                dbc.Card(
                    dbc.CardBody(
                        # empty placeholder
                    )
                )
            ], className='mb-2', style={'background-color': '#FF6E33'})
        ], width={'size': 10-2*margin})
    ]),

    dbc.Row([  # country check list & visualization
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    # dcc checklist is rendered inside a div so it can be styled
                    location_checklist(), style={'height': '60vh', 'overflow': 'auto'}
                ), className='mb-2'
            ), width={'size': 2, 'offset': margin}
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    visualization(), style={'height': '60vh'}
                ), className='mb-2'
            ), width={'size': 10-2*margin}
        )
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
