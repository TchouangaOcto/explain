# css style
style_header = {
    'backgroundColor': '#96B9C4',
    'color': '#F3FBFB',
    'fontWeight': 'bold'
}

style_data = {
    'color': 'black',
    'backgroundColor': 'white',
    'whiteSpace': 'normal',
    'height': 'auto',
    'lineHeight': '40px'
}

style_cell={
    'font-family': 'Overpass'
}

style_cell_conditional = [
    {
    'if': {'column_id': 'fichier'},
        'textAlign': 'center'
    },
    {
        'if': {'column_id': 'date'},
        'textAlign': 'center'
    }
]

style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': '#EEEFF1',
    }
]