# css style
style_header = {
            'backgroundColor': '#96B9C4',
            'color': '#F3FBFB',
            'fontWeight': 'bold'
        }

style_header_conditional = [
            {'if': {'column_id': 'id', },
             'display': 'None', }]

style_cell = {
            'font-family': 'Overpass'
        }

style_data = {
            'color': 'black',
            'backgroundColor': 'white',
            'whiteSpace': 'normal',
            'height': 'auto',

        }

style_table = {'overflowX': 'auto'}

style_data_conditional = [
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#EEEFF1',
            },
            {'if': {'column_id': 'id', },
             'display': 'None', }
        ]

style_data_conditional2 = [
            {
                "if": {
                    "state": "active"  # 'active' | 'selected'
                },
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            },
            {
                "if": {
                    "state": "selected"  # 'active' | 'selected'
                },
                "backgroundColor": "rgba(0, 116, 217, 0.3)",
                "border": "1px solid rgb(0, 116, 217)",
            },
            {'if': {'column_id': 'id', },
             'display': 'None', }
        ]