# css style
style_header={
        'backgroundColor': 'white',
        'fontWeight': 'bold'
    }

style_header2 = {
    'backgroundColor': '#96B9C4',
    'color': '#F3FBFB',
    'fontWeight': 'bold'
}
style_cell={
    'font-family': 'Overpass',
    'overflow': 'hidden',
    'textOverflow': 'ellipsis',
    'maxWidth': 0,
}

style_cell2={
    'padding': '5px',
    'font-family': 'Overpass'
}

style_cell_conditional = [
    {
        'textAlign': 'center'
    }
]

style_data = {
    'color': 'black',
    'backgroundColor': 'white',
    'whiteSpace': 'normal',
    'height': 'auto',
    'lineHeight': '40px'
}

style_data_conditional = [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': '#EEEFF1',
    }
]