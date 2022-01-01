# core component library (dcc)
from dash import dcc

# html component library (html)
from dash import html

# Input and Output objects for callback decorator
from dash.dependencies import Input, Output

# connect app.py file
from app import app

app.layout = html.Div([
    html.H1('Hello World')
])


if __name__ == '__main__':
    app.run_server(debug=False)