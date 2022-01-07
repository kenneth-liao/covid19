from dash import dcc
from dash.dependencies import Input, Output
from plotly import graph_objects as go

# connect app files
from app import app
from apps import data


# ------------------------------------------------------------------------------
# Graph Object


graph = dcc.Graph(
        id='visualization',
        figure={},
        className='h-100',
        config={'displayModeBar': False}
    )


# ------------------------------------------------------------------------------
# Callbacks


@app.callback(Output('visualization', 'figure'),
              [Input('location', 'value'),
               Input('metric', 'value'),
               Input('interval', 'value'),
               Input('relative', 'value')])
def update_figure():

    fig = go.Figure()

    return fig
