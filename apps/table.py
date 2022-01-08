from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

# connect app files
from app import app
from apps import data


# ------------------------------------------------------------------------------
# Graph Object


graph = [

    html.Div(
        dcc.Graph(
            id='table-graph',
            figure={},
            className='h-100',
            config={'displayModeBar': False}
        ), style={'height': '52vh'}
    ),

    html.Div(
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.P(
                        id='table-slider-label-1',
                        children={}
                    )
                ), width=2, style={'text-align': 'center'}
            ),
            dbc.Col(
                dcc.RangeSlider(
                    id='table-date-slider',
                    min=0,
                    max=len(data.marks) - 1,
                    value=[0, len(data.marks) - 1],
                    dots=True,
                    allowCross=False,
                    updatemode='drag'
                ), width=8
            ),
            dbc.Col(
                html.Div(
                    html.P(
                        id='table-slider-label-2',
                        children={}
                    )
                ), width=2, style={'text-align': 'center'}
            )
        ]), style={'height': '3vh'}
    )
]


# ------------------------------------------------------------------------------
# Callbacks
@app.callback(Output('table-slider-label-1', 'children'),
              Output('table-slider-label-2', 'children'),
              Input('table-date-slider', 'value'))
def update_slider_labels(slider_range):
    label1, label2 = slider_range
    return data.marks[label1], data.marks[label2]


@app.callback(Output('table-graph', 'figure'),
              [Input('location', 'value'),
               Input('metric', 'value'),
               Input('interval', 'value'),
               Input('relative_option', 'value'),
               Input('table-date-slider', 'value')])
def update_figure(location, metric, interval, relative_option, date_range):
    date1, date2 = date_range

    # weekly interval data is precomputed in data file
    if interval == 'weekly':
        date_filter = (data.weekly_data.date >= pd.to_datetime(data.marks[date1])) & \
                      (data.weekly_data.date <= pd.to_datetime(data.marks[date2]))
        # relative logic
        if (relative_option == ['relative']) & (metric != 'vaccinations'):
            if metric == 'tests':
                col_name = f'new_{metric}_per_thousand'
            else:
                col_name = f'new_{metric}_per_million'
        else:
            col_name = f'new_{metric}'

        table_data = data.weekly_data[date_filter]
        table_data = table_data[['iso_code', col_name]].groupby('iso_code').sum()
        # filter out OWID calculated regions (like continent totals)
        table_data = table_data.drop([i for i in table_data.index if 'OWID' in i])



    else:
        date_filter = (data.data.date >= pd.to_datetime(data.marks[date1])) & \
                      (data.data.date <= pd.to_datetime(data.marks[date2]))

        # relative logic
        if (relative_option == ['relative']) & (metric != 'vaccinations'):
            if metric == 'tests':
                col_name = f'{interval}_{metric}_per_thousand'
            else:
                col_name = f'{interval}_{metric}_per_million'
        else:
            col_name = f'{interval}_{metric}'



    return fig