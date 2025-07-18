from dash import html, dcc
import dash_cytoscape as cyto

PREFIX = 'most-common-tree-'

layout = html.Div([
    html.H2('Most Common Tree'),
    html.P(id=PREFIX+'intro'),
    cyto.Cytoscape(
        id=PREFIX+'cyto-tree',
        userZoomingEnabled=False,
        userPanningEnabled=False,
        layout={
            'name': 'breadthfirst',
            'roots': '[id = "0"]',
            'directed': True
        },
        stylesheet=[
            {'selector': 'edge', 'style': {'label': 'data(label)'}},
            {'selector': 'node', 'style': {'label': 'data(label)'}}
        ],
        style={'width': '50vw', 'height': '90vh'}
    ),
    dcc.Graph(id=PREFIX+'graph-threshold-distribution', style={'display': 'none'})
])
