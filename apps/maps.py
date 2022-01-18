from dash import dcc, html
from dash.dependencies import Input, Output
from plotly import graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd

# connect app files
from app import app
from apps import data


# ------------------------------------------------------------------------------
# Graph Object


graph = [

    html.Div(
        dcc.Markdown(id='map-title'), style={'margin': 'auto', 'height': '13%'}
    ),

    html.Div(
        dcc.Graph(
            id='map-graph',
            figure={},
            className='h-100',
            config={'displayModeBar': False}
        ), style={'height': '79%'}
    ),

    html.Div(
        dbc.Row([
            dbc.Col(
                html.Div(
                    html.P(
                        id='map-slider-label-1',
                        children={}
                    )
                ), width=2, style={'text-align': 'center'}
            ),
            dbc.Col(
                dcc.RangeSlider(
                    id='map-date-slider',
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
                        id='map-slider-label-2',
                        children={}
                    )
                ), width=2, style={'text-align': 'center'}
            )
        ]), style={'height': '8%'}
    )
]


# ------------------------------------------------------------------------------
# Callbacks
@app.callback(Output('map-slider-label-1', 'children'),
              Output('map-slider-label-2', 'children'),
              Input('map-date-slider', 'value'))
def update_slider_labels(slider_range):
    label1, label2 = slider_range
    return data.marks[label1], data.marks[label2]


@app.callback(Output('map-graph', 'figure'),
              Output('map-title', 'children'),
              [Input('location', 'value'),
               Input('metric', 'value'),
               Input('interval', 'value'),
               Input('relative_option', 'value'),
               Input('map-date-slider', 'value')])
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

        map_data = data.weekly_data[date_filter]
        map_data = map_data[['iso_code', col_name]].groupby('iso_code').sum()
        # filter out OWID calculated regions (like continent totals)
        map_data = map_data.drop([i for i in map_data.index if 'OWID' in i])

        fig = go.Figure(
            go.Choropleth(
                locations=map_data.index,
                z=map_data[col_name],
                colorscale='dense',
                autocolorscale=False
            )
        )

        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )

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

        map_data = data.data[date_filter]
        map_data = map_data[['iso_code', col_name]].groupby('iso_code').sum()
        # filter out OWID calculated regions (like continent totals)
        map_data = map_data.drop([i for i in map_data.index if 'OWID' in i])

        fig = go.Figure(
            go.Choropleth(
                locations=map_data.index,
                z=map_data[col_name],
                colorscale='dense',
                autocolorscale=False
            )
        )

        fig.update_layout(
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            )
        )

    # figure title
    if interval == 'new':
        fig_title = f'''
            ###### Daily new confirmed COVID-19 {metric}
            Due to limited testing, the number of confirmed cases is lower than the true number of infections.
        '''
    elif interval == 'weekly':
        fig_title = f'''
            ###### Weekly new confirmed COVID-19 {metric}
            Due to limited testing, the number of confirmed cases is lower than the true number of infections.
        '''
    else:
        fig_title = f'''
            ###### Total confirmed COVID-19 {metric}
            Due to limited testing, the number of confirmed cases is lower than the true number of infections.
        '''

    return fig, fig_title