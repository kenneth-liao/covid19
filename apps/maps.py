from dash import dcc, html
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
              [Input('metric', 'value'),
               Input('interval', 'value')])
def update_figure(metric, interval):
    fig = html.Div(html.P('MAP WILL GO HERE'))
    return fig
    # if interval == 'weekly':
    #     # relative logic
    #     if (relative == 'relative') & (metric != 'vaccinations'):
    #         if metric == 'tests':
    #             col_name = 'new_' + metric + '_per_thousand'
    #         else:
    #             col_name = 'new_' + metric + '_per_million'
    #     else:
    #         col_name = 'new_' + metric
    #
    #     resampled = data.data[['location', 'date', col_name]].groupby('location').rolling(7, on='date').sum()
    #
    #     fig = go.Figure(
    #         go.Choropleth(
    #             locations=resampled.iso_code,
    #             z=resampled[col_name]
    #         )
    #     )
    #
    #     return fig
    #
    # else:
    #     # relative logic
    #     if (relative == 'relative') & (metric != 'vaccinations'):
    #         if metric == 'tests':
    #             col_name = interval + '_' + metric + '_per_thousand'
    #         else:
    #             col_name = interval + '_' + metric + '_per_million'
    #     else:
    #         col_name = interval + '_' + metric
    #
    #     fig = go.Figure(
    #         go.Choropleth(
    #             locations=data.data.iso_code,
    #             z=data.data[col_name]
    #         )
    #     )
    #
    #     return fig
