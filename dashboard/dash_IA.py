
from dash import dcc, html

def render_ai_form_content():
    """Function to render the form with choices in the left column and doses as a single selection."""
    return html.Div([
        html.H3("Formulário de Sintomas e Condições", style={'color': '#1e90ff', 'font-family': 'Arial, sans-serif', 'text-align': 'center'}),

        html.Div([
            # Left Column
            html.Div([
                html.Div([
                    html.Label("Nome", style={'color': '#333', 'font-weight': 'bold'}),
                    dcc.Input(id='nome', type='text', placeholder="Digite seu nome", style={'width': '100%', 'padding': '10px', 'border-radius': '5px'}),
                ], style={'margin-bottom': '20px'}),

                # Gender and Age on the same line
                html.Div([
                    html.Div([
                        html.Label("Gênero", style={'color': '#333', 'font-weight': 'bold'}),
                        dcc.Dropdown(
                            id='genero',
                            options=[
                                {'label': 'Masculino', 'value': 'masculino'},
                                {'label': 'Feminino', 'value': 'feminino'},
                                {'label': 'Outro', 'value': 'outro'},
                            ],
                            value='masculino',  # Default value
                            style={'width': '100%', 'padding': '10px', 'border-radius': '5px'}
                        ),
                    ], style={'flex': '1', 'margin-right': '10px'}),

                    html.Div([
                        html.Label("Idade", style={'color': '#333', 'font-weight': 'bold'}),
                        dcc.Input(id='idade', type='number', placeholder="Digite sua idade", style={'width': '100%', 'padding': '10px', 'border-radius': '5px'}),
                    ], style={'flex': '1'}),
                ], style={'display': 'flex', 'margin-bottom': '20px', 'gap': '10px'}),

                # General Symptoms
                html.Div([
                    html.H4("Sintomas Gerais", style={'color': '#333', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='sintomas-gerais-tags',
                        options=[
                            {'label': 'Tosse', 'value': 'sintomas_Tosse'},
                            {'label': 'Dor de Cabeça', 'value': 'sintomas_Dor_de_Cabeça'},
                            {'label': 'Febre', 'value': 'sintomas_Febre'},
                            {'label': 'Dor de Garganta', 'value': 'sintomas_Dor_de_Garganta'},
                            {'label': 'Coriza', 'value': 'sintomas_Coriza'},
                            {'label': 'Dispneia', 'value': 'sintomas_Dispneia'},
                            {'label': 'Distúrbios Gustativos', 'value': 'sintomas_Distúrbios_Gustativos'},
                            {'label': 'Distúrbios Olfativos', 'value': 'sintomas_Distúrbios_Olfativos'},
                        ],
                        multi=True,
                        style={'width': '100%', 'padding': '10px', 'border-radius': '5px'}
                    ),
                ], style={'margin-bottom': '20px'}),

                # Other Symptoms
                html.Div([
                    html.H4("Outros Sintomas", style={'color': '#333', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='outros-sintomas-tags',
                        options=[
                            {'label': 'Dor no Corpo', 'value': 'outrosSintomas_DOR_NO_CORPO'},
                            {'label': 'Dor nas Costas', 'value': 'outrosSintomas_DOR_NAS_COSTAS'},
                            {'label': 'Dor Abdominal', 'value': 'outrosSintomas_DOR_ABDOMINAL'},
                            {'label': 'Dor Torácica', 'value': 'outrosSintomas_DOR_TORACICA'},
                            {'label': 'Mialgia', 'value': 'outrosSintomas_MIALGIA'},
                            {'label': 'Artralgia', 'value': 'outrosSintomas_ARTRALGIA'},
                            {'label': 'Calafrios', 'value': 'outrosSintomas_CALAFRIOS'},
                            {'label': 'Congestão Nasal', 'value': 'outrosSintomas_CONGESTAO_NASAL'},
                            {'label': 'Diarréia', 'value': 'outrosSintomas_DIARREIA'},
                            {'label': 'Náusea', 'value': 'outrosSintomas_NAUSEA'},
                            {'label': 'Vômito', 'value': 'outrosSintomas_VOMITO'},
                            {'label': 'Espirros', 'value': 'outrosSintomas_ESPIRROS'},
                            {'label': 'Fraqueza/Fadiga', 'value': 'outrosSintomas_FRAQUEZA_FADIGA'},
                            {'label': 'Dor nos Olhos', 'value': 'outrosSintomas_DOR_NOs_OLHOS'},
                            {'label': 'Dor', 'value': 'outrosSintomas_DOR'},
                            {'label': 'Cansaço', 'value': 'outrosSintomas_CANSAÇO'},
                            {'label': 'Astenia', 'value': 'outrosSintomas_ASTENIA'},
                            {'label': 'Desconforto', 'value': 'outrosSintomas_DESCONFORTO'},
                            {'label': 'Mal Estar', 'value': 'outrosSintomas_MAL_ESTAR'},
                            {'label': 'Cefaleia', 'value': 'outrosSintomas_CEFALEIA'},
                            {'label': 'Falta de ar', 'value': 'outrosSintomas_FALTA_DE_AR'},
                            {'label': 'Desconforto respiratório', 'value': 'outrosSintomas_DESCONFORTO_RESPIRATORIO'},
                            {'label': 'Tontura', 'value': 'outrosSintomas_TONTURA'},
                            {'label': 'Dor no peito', 'value': 'outrosSintomas_DOR_NO_PEITO'},
                            {'label': 'Dor no ouvido', 'value': 'outrosSintomas_OUVIDO'},
                            {'label': 'Adinamia', 'value': 'outrosSintomas_ADINAMIA'},
                            {'label': 'Odinofagia', 'value': 'outrosSintomas_ODINOFAGIA'},
                        ],
                        multi=True,
                        style={'width': '100%', 'padding': '10px', 'border-radius': '5px'}
                    ),
                ], style={'margin-bottom': '20px'}),

                # Preexisting Conditions (Comorbidities)
                html.Div([
                    html.H4("Condições Preexistentes (Comorbidades)", style={'color': '#333', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='comorbidades-tags',
                        options=[
                            {'label': 'Hipertensão', 'value': 'outrasCondicoes_HIPERTENSAO'},
                            {'label': 'Diabetes', 'value': 'condicoes_Diabetes'},
                            {'label': 'Asma', 'value': 'outrasCondicoes_ASMA'},
                            {'label': 'Bronquite', 'value': 'outrasCondicoes_BRONQUITE'},
                            {'label': 'Rinite', 'value': 'outrasCondicoes_RINITE'},
                            {'label': 'Sinusite', 'value': 'outrasCondicoes_SINUSITE'},
                            {'label': 'Epilepsia', 'value': 'outrasCondicoes_EPILEPSIA'},
                            {'label': 'Tireoidismo', 'value': 'outrasCondicoes_TIREOIDISMO'},
                            {'label': 'Ansiedade', 'value': 'outrasCondicoes_ANSIEDADE'},
                            {'label': 'Tabagismo', 'value': 'outrasCondicoes_TABAGISMO'},
                            {'label': 'Sem Comorbidade', 'value': 'outrasCondicoes_SEM_COMORBIDADE'},
                        ],
                        multi=True,
                        style={'width': '100%', 'padding': '10px', 'border-radius': '5px'}
                    ),
                ], style={'margin-bottom': '20px'}),

                html.H4("Vacinação", style={'color': '#333', 'font-weight': 'bold'}),
                dcc.RadioItems(
                    id='vacinacao-dose',
                    options=[
                        {'label': 'Primeira Dose', 'value': 'tomouPrimeiraDose'},
                        {'label': 'Segunda Dose', 'value': 'tomouSegundaDose'},
                        {'label': 'Nenhuma Dose', 'value': 'nenhuma_dose'},
                    ],
                    value='nenhuma_dose',  # Default value
                    labelStyle={'display': 'block', 'padding': '5px 0'}
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '20px'}),

            # Right Column for Display
            html.Div(id='ia-output', children=[
            ], style={'width': '48%', 'display': 'inline-block', 'margin-left': '4%', 'padding': '20px'}),
        ], style={'display': 'flex', 'justify-content': 'space-between'}),

        html.Button('Submeter', id='submit-button', n_clicks=0, style={'background-color': '#1e90ff', 'color': 'white', 'padding': '10px 20px', 'border-radius': '10px', 'border': 'none', 'cursor': 'pointer', 'display': 'block', 'margin': '20px auto'}),
        html.Div(id='output-container', style={'margin-top': '20px', 'color': '#333', 'text-align': 'center'})
    ], style={'border-radius': '10px', 'background-color': 'white', 'padding': '20px'})