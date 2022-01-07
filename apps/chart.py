from dash import dcc
from dash.dependencies import Input, Output
from plotly import graph_objects as go

# connect app files
from app import app
from apps import data


# ------------------------------------------------------------------------------
# Graph Object


graph = [dcc.Graph(
        id='visualization',
        figure={},
        className='h-100',
        config={'displayModeBar': False}
    ),
    dcc.RangeSlider(
        id='date-slider',
        min=data.data.date.min(),
        max=data.data.date.max(),
        value=[data.data.date.min(), data.data.date.max()]
    )]


# ------------------------------------------------------------------------------
# Callbacks


@app.callback(Output('visualization', 'figure'),
              [Input('location', 'value'),
               Input('metric', 'value'),
               Input('interval', 'value'),
               Input('relative', 'value')])
def update_figure(location, metric, interval, relative):
    # resample data to weekly
    if interval == 'weekly':
        # relative logic
        if (relative == 'relative') & (metric != 'vaccinations'):
            if metric == 'tests':
                col_name = 'new_' + metric + '_per_thousand'
            else:
                col_name = 'new_' + metric + '_per_million'
        else:
            col_name = 'new_' + metric

        resampled = data.data[['location', 'date', col_name]].groupby('location').rolling(7, on='date').sum()

        traces = []
        for country in location:
            traces.append(
                go.Scatter(name=country, mode='markers+lines',
                           x=resampled.loc[country, :]['date'],
                           y=resampled.loc[country, :][col_name])
            )

    else:
        # relative logic
        if (relative == 'relative') & (metric != 'vaccinations'):
            if metric == 'tests':
                col_name = interval + '_' + metric + '_per_thousand'
            else:
                col_name = interval + '_' + metric + '_per_million'
        else:
            col_name = interval + '_' + metric

        traces = []
        for country in location:
            traces.append(
                go.Scatter(name=country, mode='markers+lines',
                           x=data.data[data.data['location'] == country]['date'],
                           y=data.data[data.data['location'] == country][col_name])
            )

    fig = go.Figure(data=traces)
    fig.update_traces(marker={'size': 3}, line={'width': 1})
    fig.update_layout(hovermode='x', showlegend=True,
                      legend={'orientation': 'h'},
                      margin={'t': 50})

    return fig
