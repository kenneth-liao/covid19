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
# connect chart file
from apps import chart
from apps import maps
# connect data file
from apps import data
import plotly.io as pio
# ------------------------------------------------------------------------------
# To do
# 1. Add table visualization to table tab
# 3. Style the damn thing







# ------------------------------------------------------------------------------
# User defined styling


# set the default theme for plotly
pio.templates.default = "plotly_white"

# set app width (out of 12 total columns)
app_width = 8
margin = (12-app_width)/2  # don't change this

footer_signature = 'Dashboard design by Kenneth Liao, 2022'


# ------------------------------------------------------------------------------
# Data Options


# define metrics
metric_options = [
    {'label': 'Confirmed Cases', 'value': 'cases'},
    {'label': 'Confirmed Deaths', 'value': 'deaths'},
    {'label': 'Tests', 'value': 'tests'},
    {'label': 'Vaccinations', 'value': 'vaccinations'}
]

# define intervals
interval_options = [
    {'label': 'Cumulative', 'value': 'total'},
    {'label': 'New per day', 'value': 'new'},
    {'label': 'Weekly', 'value': 'weekly'}
]


# ------------------------------------------------------------------------------
# Define main DCC components


# location check list component
def location_checklist():
    return dcc.Checklist(
        id='location', value=['United States', 'United Kingdom', 'Germany', 'Canada', 'Italy'],
        options=[{'label': c, 'value': c} for c in data.data.location.unique()],
        inputStyle={'margin-right': '5px'}  # adds space between checkbox & label
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
        value='new',
        clearable=False
    )


# relative to population option
def relative_checklist():
    return dcc.Checklist(
        id='relative_option',
        options=[
            {'label': ' Relative to population', 'value': 'relative'}
        ]
    )


# ------------------------------------------------------------------------------
# App Layout


app.layout = html.Div([
    # the Location component stores the url in the address bar
    dcc.Location(id='url', refresh=False),

    dbc.Row(  # title
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    html.H1('COVID-19 Global Data Dashboard')
                ), className='mb-4'
            ), width={'size': app_width, 'offset': margin}
        )
    ),

    dbc.Row([  # logo & plotting options
        dbc.Col(  # logo
            dbc.Card(
                dbc.CardBody([
                    html.H5('COVID-19 Data Explorer', style={'font-weight': 'bold'}),
                    dcc.Markdown('''
                    Download the complete *Our World in Data* \
                    [COVID-19 dataset](https://github.com/owid/covid-19-data/tree/master/public/data).
                    ''')
                ]), className='mb-4', style={'height': '10vh'}
            ), width={'size': 2, 'offset': margin}, align='center'
        ),
        dbc.Col([  # plotting options
            dbc.Card([
                dbc.Row([
                    dbc.Col([
                        html.H6('Metric'),
                        metric_dropdown()
                    ], style={'margin-left': '10px'}, align='center'),
                    dbc.Col([
                        html.H6('Interval'),
                        interval_dropdown()
                    ], style={'margin-left': '10px'}, align='center'),
                    dbc.Col([
                        relative_checklist(),
                    ], style={'margin-left': '10px'}, align='center')
                ], style={'height': '10vh'})
            ], className='mb-4')
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
        dbc.Col([
            dbc.CardHeader(
                dcc.Tabs(id='tab-group', value='chart', children=[
                    dcc.Tab(
                        label='Chart',
                        value='chart'
                    ),
                    dcc.Tab(
                        label='Map',
                        value='map'
                    ),
                    dcc.Tab(
                        label='Table',
                        value='table'
                    )
                ]), style={'height': '5vh', 'background-color': 'rgb(245, 245, 245)'}
            ),
            dbc.Row(
                dbc.Col(
                    # this card contains the visualizations
                    dbc.Card(
                        dbc.CardBody(id='visualization-card',
                                     children={},
                                     style={'height': '55vh'}
                                     )
                    )
                )
            )
        ], width={'size': 10-2*margin}
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.Div(
                html.P(footer_signature, className='mt-2')
            ), width={'size': 10-2*margin, 'offset': margin + 2}, style={'text-align': 'right'}
        )
    ])

])


# ------------------------------------------------------------------------------
# Calllbacks to connect DCC components


# connect visualization
@app.callback(Output('visualization-card', 'children'),
              Input('tab-group', 'value'))
def update_card(tab):
    if tab == 'chart':
        return chart.graph
    elif tab == 'map':
        return maps.graph
    else:
        return html.Div(html.P('ERROR'))


if __name__ == '__main__':
    app.run_server(debug=True)
