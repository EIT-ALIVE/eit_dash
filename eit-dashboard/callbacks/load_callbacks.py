from dash import callback, Output, Input

@callback(
    Output('test-label', 'children'),
    Input('add-data-button', 'n_clicks')
)
def update_graph(value):
    return value