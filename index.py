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

# define metrics
metric_options = [
    {'label': 'Confirmed Cases', 'value': 'cases'},
    {'label': 'Confirmed Deaths', 'value': 'deaths'},
    {'label': 'Tests', 'value': 'tests'}
]

# define intervals
interval_options = [
    {'label': 'Cumulative', 'value': 'total'},
    {'label': 'New per day', 'value': 'new'},
    {'label': 'Weekly', 'value': 'weekly'}
]

# load the latest data
data = pd.read_csv('data/owid-covid-data.csv')
# filter data down to only columns we need
data = data[['location', 'date', 'total_cases', 'new_cases', 'total_cases_per_million', 'new_cases_per_million',
             'total_deaths', 'new_deaths', 'total_deaths_per_million', 'new_deaths_per_million',
             'total_tests', 'new_tests',
             'total_vaccinations', 'new_vaccinations']]


# location check list component
def location_checklist():
    return dcc.Checklist(
        id='location', value=['United States', 'United Kingdom', 'Germany', 'Canada', 'Italy'],
        options=[{'label': c, 'value': c} for c in data.location.unique()]
    )


# metric dropdown component
def metric_dropdown():
    return dcc.Dropdown(
        id='metric',
        options=metric_options,
        value='cases',
        clearable=False
    )


# interval dropdown component
def interval_dropdown():
    return dcc.Dropdown(
        id='interval',
        options=interval_options,
        value='total',
        clearable=False
    )


# relative to population option
def relative_checklist():
    return dcc.Checklist(
        id='relative',
        options=[
            {'label': ' Relative to population', 'value': 'relative'}
        ]
    )


# visualization component
def visualization():
    return dcc.Graph(
        id='visualization',
        figure={},
        className='h-100',
        config={'displayModeBar': False}
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
                ), className='mb-2', style={'height': '10vh'}
            ), width={'size': 2, 'offset': margin}
        ),
        dbc.Col([  # plotting options
            dbc.CardGroup([
                dbc.Card(
                    dbc.CardBody([
                        html.H6('Metric'),
                        metric_dropdown()
                    ]), style={'height': '10vh'}
                ),
                dbc.Card(
                    dbc.CardBody([
                        html.H6('Interval'),
                        interval_dropdown()
                    ]), style={'height': '10vh'}
                ),
                dbc.Card(
                    dbc.CardBody(
                        relative_checklist()
                    ), style={'height': '10vh'}
                ),
                dbc.Card(
                    dbc.CardBody(
                        # empty placeholder
                    ), style={'height': '10vh'}
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
                )
            ), width={'size': 2, 'offset': margin}
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    visualization(), style={'height': '60vh'}
                )
            ), width={'size': 10-2*margin}
        )
    ])

])


# callbacks to connect components
@app.callback(Output('visualization', 'figure'),
              [Input('location', 'value'),
               Input('metric', 'value'),
               Input('interval', 'value')])
def update_figure(location, metric, interval):
    # resample data to weekly
    if interval == 'weekly':
        resampled = data[['location', 'date', 'new_'+metric]].groupby('location').rolling(7, on='date').sum()

        traces = []
        for country in location:
            traces.append(
                go.Scatter(name=country, mode='markers+lines',
                           x=resampled.loc[country, :]['date'],
                           y=resampled.loc[country, :]['new_'+metric])
            )

    else:
        traces = []
        for country in location:
            traces.append(
                go.Scatter(name=country, mode='markers+lines',
                           x=data[data['location'] == country]['date'],
                           y=data[data['location'] == country][interval+'_'+metric])
            )

    fig = go.Figure(data=traces)
    fig.update_traces(marker={'size': 3}, line={'width': 1})
    fig.update_layout(hovermode='x', showlegend=True)

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
