from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from plotly import graph_objects as go

import pandas as pd
import pathlib

from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

data = pd.read_csv(DATA_PATH.joinpath("owid-covid-data.csv"))


layout = html.Div([
    dcc.Graph(id='plot', figure={})
])


@app.callback(Output('plot', 'figure'),
              [Input('metric', 'value')])
def update_figure(metric):
    fig = go.Figure(
        go.Scatter(x=data['date'], y=data['total_cases'])
    )

    return fig
