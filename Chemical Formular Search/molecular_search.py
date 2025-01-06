import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
from bs4 import BeautifulSoup
from itertools import combinations
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Molecular Search', className='text-center mb-4 mt-4'),
            
            dbc.Card([
                dbc.CardBody([
                    html.Label('Target Molecular Weight:', className='fw-bold'),
                    dcc.Input(
                        id='target-weight',
                        type='number',
                        value=12,
                        step=0.01,
                        className='form-control mb-3'
                    ),
                    
                    html.Label('Tolerance:', className='fw-bold'),
                    dcc.Input(
                        id='tolerance',
                        type='number',
                        value=0.1,
                        step=0.01,
                        className='form-control mb-3'
                    ),
                    
                    html.Label('Min Weight (optional):', className='fw-bold'),
                    dcc.Input(
                        id='min-weight',
                        type='number',
                        step=0.01,
                        className='form-control mb-3'
                    ),
                    
                    html.Label('Max Weight (optional):', className='fw-bold'),
                    dcc.Input(
                        id='max-weight',
                        type='number',
                        step=0.01,
                        className='form-control mb-3'
                    ),
                    
                    html.Label('Select Elements:', className='fw-bold'),
                    dcc.Dropdown(
                        id='element-list',
                        options=[
                            {'label': 'Carbon (C)', 'value': 'C'},
                            {'label': 'Oxygen (O)', 'value': 'O'},
                            {'label': 'Fluorine (F)', 'value': 'F'},
                            {'label': 'Hydrogen (H)', 'value': 'H'},
                            {'label': 'Nitrogen (N)', 'value': 'N'},
                            {'label': 'Argon (Ar)', 'value': 'Ar'},
                            {'label': 'Silicon (Si)', 'value': 'Si'},
                            {'label': 'Aluminum (Al)', 'value': 'Al'},
                            {'label': 'Chlorine (Cl)', 'value': 'Cl'},
                            {'label': 'Germanium (Ge)', 'value': 'Ge'},
                            {'label': 'Yttrium (Y)', 'value': 'Y'},
                            {'label': 'Zirconium (Zr)', 'value': 'Zr'},
                            {'label': 'Molybdenum (Mo)', 'value': 'Mo'}
                        ],
                        multi=True,
                        className='mb-4'
                    ),
                    
                    dbc.Button(
                        'Search',
                        id='search-button',
                        color='primary',
                        className='w-100'
                    ),
                ])
            ], className='shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.Div(id='results')
                ])
            ], className='mt-4 shadow')
            
        ], width=8, className='mx-auto')
    ])
], fluid=True, className='bg-light min-vh-100 py-4')

def search_nist(min_value, max_value, elements):
    all_results = []

    for r in range(1, len(elements) + 1):
        for comb in combinations(elements, r):
            formula = '%2C'.join(comb)
            url = f"https://webbook.nist.gov/cgi/cbook.cgi?Value={min_value}%2C{max_value}&VType=MW&Formula={formula}&AllowExtra=on&NoIon=on&Units=SI"
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            results = []
            list_items = soup.select('ol li')

            for li in list_items:
                try:
                    molecular_weight = li.find('strong').text
                    molecular_formula = li.find('a').text
                    formula_link = li.find('a')['href']
                    img_url = f"https://webbook.nist.gov/cgi/cbook.cgi?Struct={formula_link.split('ID=')[1]}&Type=Color"
                    
                    results.append((molecular_weight, molecular_formula, img_url))
                except (AttributeError, TypeError):
                    continue

            all_results.extend(results)
    all_results.sort(key=lambda x: float(x[0]))
    return all_results

@app.callback(
    Output('results', 'children'),
    Input('search-button', 'n_clicks'),
    State('target-weight', 'value'),
    State('tolerance', 'value'),
    State('min-weight', 'value'),
    State('max-weight', 'value'),
    State('element-list', 'value')
)
def update_results(n_clicks, target_weight, tolerance, min_weight, max_weight, included_elements):
    if n_clicks is None:
        return 'Enter search criteria and click "Search"'
        
    if n_clicks > 0:
        if min_weight is not None and max_weight is not None:
            min_value = min_weight
            max_value = max_weight
        else:
            min_value = target_weight - tolerance
            max_value = target_weight + tolerance
        
        try:
            search_results = search_nist(min_value, max_value, included_elements)
            if len(search_results) == 0:
                return html.Div('No results found', className='text-danger')
            else:
                return [
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Span(f"Weight: {mw}", className='fw-bold me-2'),
                                    html.Span(f"Formula: {formula}")
                                ], width=8),
                                dbc.Col([
                                    html.Img(src=img_url, style={'max-width': '100%'}) if img_url else html.Div("No structure image available")
                                ], width=4)
                            ])
                        ])
                    ], className='mb-3') for mw, formula, img_url in search_results
                ]
        except requests.exceptions.RequestException as e:
            return html.Div(f"An error occurred: {e}", className='text-danger')
            
    return 'Enter search criteria and click "Search"'

if __name__ == '__main__':
    app.run_server(debug=True)
