# core component library (dcc)
from dash import dcc

# html component library (html)
from dash import html

# Input and Output objects for callback decorator
from dash.dependencies import Input, Output

# connect app.py file
from app import app

# connect app pages
from apps import page1

app.layout = html.Div([
    html.H1('Hello World'),
    html.Div([
        html.H5('Metric'),
        dcc.Dropdown(id='metric',
                     options=[{'label':'Confirmed cases', 'value':'cases'}])
    ], style={'width': '200px'})
])


if __name__ == '__main__':
    app.run_server(debug=False)