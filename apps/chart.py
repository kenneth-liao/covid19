from dash import dcc
from dash import html
from dash.dependencies import Input, Output

import pandas as pd
import pathlib

from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()

data = pd.read_csv(DATA_PATH.joinpath("owid-covid-data.csv"))


layout = html.Div([
    html.H1('CHART TEST')
])
