import dash

# instantiate app
# these meta tags configure the app to be viewable on mobile devices
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial_scale=1.0'}])

# instantiate server
server = app.server
