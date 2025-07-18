from dash import html, dcc, dash_table
import dash_cytoscape as cyto

PREFIX = 'forest-'
persist = {'persistence': True, 'persistence_type': 'session'}
leaf_options = [{'label': 'Plot leaf', 'value': True}, {'label': 'Show prediction only', 'value': False}]

table_styles = [

    # Color the p_corrected column of all insignificant thresholds in red
    {
        'if': {
            'filter_query': '{p_corrected} > 0.05',
            'column_id': 'p_corrected'
        },
        'backgroundColor': 'tomato'
    },

    # Color the p_corrected column of all insignificant thresholds in green
    {
        'if': {
            'filter_query': '{p_corrected} <= 0.05',
            'column_id': 'p_corrected'
        },
        'backgroundColor': 'yellowgreen'
    },

    # Color the p_corrected column in red when p_corrected is nan
    {
        'if': {
            'filter_query': '{p_corrected} is nil',
        },
        'backgroundColor': 'tomato'
    }

]

layout = html.Div([
    
    # Used only when the page is loaded but no tree has been selected in Home
    html.H2('Causal Forest'),

    # Select an individual tree from the whole forest
    html.P(['Select a tree to interact with or go back to ', dcc.Link('Model Selection', href='/thesis')]),
    dcc.RadioItems(id=PREFIX+'radio-tree', inline=True),

    # Print some information about the selected tree
    html.P(id=PREFIX+'txt-tree'),
    
    # Graph for the tree
    cyto.Cytoscape(
        id=PREFIX+'cyto-tree',
        userZoomingEnabled=False,
        userPanningEnabled=False,
        layout={'name': 'breadthfirst', 'roots': '[id = "0"]', 'directed': True},
        stylesheet=[
            {'selector': 'edge', 'style': {'label': 'data(label)'}},
            {'selector': 'node', 'style': {'label': 'data(label)'}}
        ],
        style={'width': '50vw', 'height': '90vh'}
    ),

    # Show statistics for that node in text
    html.P(id=PREFIX+'txt-click-tree-node'),

    # Draw the graph at that node
    dcc.Graph(id=PREFIX+'graph-at-node', style={'display': 'none'}),

    # Select a specific variable in the current node
    html.P(id=PREFIX+'variable-selection-header'),
    dcc.RadioItems(id=PREFIX+'radio-variable'),
    
    html.Div(
        children=[
            html.Br(),
            html.H3('Stage 1'),
            html.P('Considering each variable independently. Select a row to visualize the split'),

            # The table for the selected variable at that node
            dash_table.DataTable(
                id=PREFIX+'table',
                row_selectable='single',
                column_selectable='single',
                style_cell={
                    'whiteSpace': 'pre-line',
                    'textAlign': 'left',
                },
                style_data_conditional=table_styles
            ),

            # Draw the graph at the selected row in the table
            dcc.Graph(id=PREFIX+'graph-at-split', style={'display': 'none'}),
            
            html.Br(),
            html.H3('Stage 2'),
            html.P('Controlling for the other variables. Selec a row to visualize the strata'),
            dash_table.DataTable(
                id=PREFIX+'table-stratified',
                row_selectable='single',
                column_selectable='single',
                style_cell={
                    'whiteSpace': 'pre-line',
                    'textAlign': 'left',
                },
                style_data_conditional=table_styles
            )
        ],
        id=PREFIX+'div-tables',
        hidden=True
    ),

    html.P(id=PREFIX+'txt-strata'),
    dcc.Loading(dcc.Graph(id=PREFIX+'graph-at-stratum', style={'display': 'none'}))
])
