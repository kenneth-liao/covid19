# core component library (dcc)
from dash import dcc

# html component library (html)
from dash import html

# Input and Output objects for callback decorator
from dash.dependencies import Input, Output

# connect app.py file
from app import app

# connect app pages
from apps import chart
from apps import maps

app.layout = html.Div([
    html.H1('Hello World'),
    # the Location component stores the url in the address bar
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.H5('Metric'),
        dcc.Dropdown(id='metric',
                     options=[{'label': 'Confirmed cases', 'value': 'cases'}])
    ], style={'width': '200px'}),
    # the page-content Div is where we will display the plots
    html.Div(id='page-content', children=[]),
    html.Div([
        dcc.Link(' Chart |', href='/apps/chart'),
        dcc.Link(' Map |', href='/apps/map')
    ])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def update_content(pathname):
    if pathname == '/apps/chart':
        return chart.layout
    elif pathname == '/apps/map':
        return maps.layout
    else:
        return '404 Error. Please click a link.'


if __name__ == '__main__':
    app.run_server(debug=False)
