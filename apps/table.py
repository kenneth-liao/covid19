from dash import dcc, html
from dash import dash_table
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
        dash_table.DataTable(
            id='data-table'
        ), style={'height': '51vh', 'overflow-y': 'auto', 'margin-bottom': '10px'}
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


@app.callback(Output('data-table', 'columns'),
              Output('data-table', 'data'),
              Input('metric', 'value'),
              Input('interval', 'value'),
              Input('relative_option', 'value'),
              Input('table-date-slider', 'value'))
def update_figure(metric, interval, relative_option, date_range):
    date_range = [data.marks[date_range[0]], data.marks[date_range[1]]]

    # relative logic
    if (relative_option == ['relative']) & (metric != 'vaccinations'):
        if metric == 'tests':
            col_name = f'new_{metric}_per_thousand'
        else:
            col_name = f'new_{metric}_per_million'
    else:
        col_name = f'new_{metric}'

    # weekly interval data is precomputed in data file
    if interval == 'weekly':
        # filter to col and dates
        table_data = data.weekly_data[['location', 'date', col_name]]
    else:
        table_data = data.data[['location', 'date', col_name]]

    # convert date_range to datetimes
    date_range = [pd.to_datetime(i) for i in date_range]

    # create new location and date dataframe with two dates in date_range
    dfs = []
    for country in table_data.location.unique():
        dfs.append(pd.DataFrame(data={'location': country, 'date': date_range}))
    dfs = pd.concat(dfs)

    # left join data
    table_data = dfs.merge(table_data, how='left', on=['location', 'date'])

    # fill missing values with 0
    table_data = table_data.fillna(0)

    # unstack df
    table_data = table_data.set_index(['location', 'date']).unstack('date')
    table_data.columns = table_data.columns.droplevel()

    # add absolute change col
    table_data['Absolute Change'] = table_data[date_range[1]] - table_data[date_range[0]]

    # fix column names
    table_data.columns = [str(table_data.columns[0])[:10], str(table_data.columns[1])[:10], table_data.columns[2]]

    # add relative change col
    def relative_calc(x):
        # if both 0, 0: 0
        if (x[0] == 0) & (x[1] == 0):
            return 0
        # if both #, #: #
        elif (x[0] != 0) & (x[1] != 0):
            return round((x[2] / x[0]) * 100)
        # if 0, #: blank
        elif (x[0] == 0) & (x[1] != 0):
            return
            # if #, 0: -%100%
            return -100

    table_data['Relative Change'] = table_data.apply(relative_calc, axis=1)

    # reset the index to include the location column
    table_data = table_data.reset_index()

    return [{'name': i, 'id': i} for i in table_data.columns], table_data.to_dict('records')
