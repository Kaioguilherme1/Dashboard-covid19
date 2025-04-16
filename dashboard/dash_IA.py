
from dash import dcc, html

def render_ai_form_content():
    """Function to render the form with choices in the left column and doses as a single selection."""
    return html.Div([
    html.H3("📝 Formulário de Sintomas e Condições", style={
        'color': '#1e90ff',
        'font-family': 'Segoe UI, sans-serif',
        'text-align': 'center',
        'margin-bottom': '30px'
    }),

    html.Div([
        ## 🧍 Coluna Esquerda (Formulário)
        html.Div([
            html.Div([
                html.Div([
                    html.Label("Nome", style={'color': '#333', 'font-weight': 'bold'}),
                    dcc.Input(
                        id='nome',
                        type='text',
                        placeholder="Digite seu nome completo",
                        style={
                            'width': '100%',
                            'padding': '12px',
                            'border-radius': '6px',
                            'font-size': '16px'
                        }
                    ),
                ], style={'flex': '2', 'margin-right': '10px'}),

                html.Div([
                    html.Label("Gênero", style={'color': '#333', 'font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='genero',
                        options=[
                            {'label': 'Masculino', 'value': 'masculino'},
                            {'label': 'Feminino', 'value': 'feminino'},
                            {'label': 'Outro', 'value': 'outro'},
                        ],
                        value='masculino',
                        style={
                            'width': '100%',
                            'padding': '10px',
                            'border-radius': '6px',
                            'font-size': '16px'
                        }
                    ),
                ], style={'flex': '1', 'margin-right': '10px'}),

                html.Div([
                    html.Label("Idade", style={'color': '#333', 'font-weight': 'bold'}),
                    dcc.Input(
                        id='idade',
                        type='number',
                        placeholder="Ex: 32",
                        style={
                            'width': '100%',
                            'padding': '12px',
                            'border-radius': '6px',
                            'font-size': '16px'
                        }
                    ),
                ], style={'flex': '1'}),
            ], style={
                'display': 'flex',
                'gap': '10px',
                'margin-bottom': '25px',
                'flex-wrap': 'wrap'
            }),
            html.Div([
                html.H4("💢 Sintomas Gerais", className='section-title'),
                dcc.Dropdown(
                    id='sintomas-gerais-tags',
                    options=[
                        {'label': 'Dor no corpo', 'value': 'dor_corpo'},
                        {'label': 'Dor nas costas', 'value': 'dor_costas'},
                        {'label': 'Dor abdominal', 'value': 'dor_abdomen'},
                        {'label': 'Dor torácica', 'value': 'dor_toracica'},
                        {'label': 'Dor no peito', 'value': 'dor_peito'},
                        {'label': 'Dor nos olhos', 'value': 'dor_olhos'},
                        {'label': 'Dor geral', 'value': 'dor_geral'},
                        {'label': 'Mialgia', 'value': 'mialgia'},
                        {'label': 'Fadiga', 'value': 'fadiga'},
                        {'label': 'Febre', 'value': 'febre'},
                        {'label': 'Mal-estar', 'value': 'mal_estar'},
                        {'label': 'Tontura', 'value': 'tontura'},
                        {'label': 'Desconforto respiratório', 'value': 'desconforto_respiratorio'},
                        {'label': 'Saturação baixa', 'value': 'saturacao_baixa'},
                        {'label': 'Sintomas indefinidos', 'value': 'sintomas_indefinidos'}
                    ],
                    multi=True,
                    className='form-dropdown'
                ),
            ], className='form-group'),

            html.Div([
                html.H4("🤒 Sintomas Específicos", className='section-title'),
                dcc.Dropdown(
                    id='outros-sintomas-tags',
                    options=[
                        {'label': 'Tosse', 'value': 'tosse'},
                        {'label': 'Coriza', 'value': 'coriza'},
                        {'label': 'Congestão nasal', 'value': 'congestao_nasal'},
                        {'label': 'Diarreia', 'value': 'diarreia'},
                        {'label': 'Náusea', 'value': 'nausea'},
                        {'label': 'Vômito', 'value': 'vomito'},
                        {'label': 'Espirros', 'value': 'espirros'},
                        {'label': 'Alteração no olfato', 'value': 'olfato_alterado'},
                        {'label': 'Alteração no paladar', 'value': 'paladar_alterado'},
                        {'label': 'Dor de garganta', 'value': 'garganta'},
                        {'label': 'Dor de cabeça', 'value': 'dor_de_cabeca'},
                        {'label': 'Falta de ar', 'value': 'falta_de_ar'},
                        {'label': 'Dor no ouvido', 'value': 'dor_de_ouvido'}
                    ],
                    multi=True,
                    className='form-dropdown'
                ),
            ], className='form-group'),

            html.Div([
                html.H4("🧬 Comorbidades", className='section-title'),
                dcc.Dropdown(
                    id='comorbidades-tags',
                    options=[
                        {'label': 'Asma', 'value': 'asma'},
                        {'label': 'Hipertensão', 'value': 'hipertensao'},
                        {'label': 'Sem comorbidade', 'value': 'sem_comorbidade'},
                        {'label': 'Diabetes', 'value': 'diabetes'},
                        {'label': 'Bronquite', 'value': 'bronquite'},
                        {'label': 'Tabagismo', 'value': 'tabagismo'},
                        {'label': 'Epilepsia', 'value': 'epilepsia'},
                        {'label': 'Ansiedade', 'value': 'ansiedade'},
                        {'label': 'Hipotireoidismo', 'value': 'hipotireoidismo'},
                        {'label': 'Tireoidite', 'value': 'tireoidite'},
                        {'label': 'Rinite', 'value': 'rinite'},
                        {'label': 'Sinusite', 'value': 'sinusite'},
                        {'label': 'Hipotensão', 'value': 'hipotensao'},
                        {'label': 'Comorbidades indefinidas', 'value': 'comorbidades_indefinidas'},
                        {'label': 'Não declarado', 'value': 'nao_declarado'},
                        {'label': 'Pré-operatório', 'value': 'pre_operatorio'},
                        {'label': 'Esclerose Lateral Amiotrófica', 'value': 'esclerose_lateral_amiotrofica'}
                    ],
                    multi=True,
                    className='form-dropdown'
                ),
            ], className='form-group'),

            html.Div([
                html.H4("💉 Status de Vacinação", className='section-title'),
                dcc.RadioItems(
                    id='vacinacao-dose',
                    options=[
                        {'label': 'Primeira Dose', 'value': 'tomouPrimeiraDose'},
                        {'label': 'Segunda Dose', 'value': 'tomouSegundaDose'},
                        {'label': 'Nenhuma Dose', 'value': 'nenhuma_dose'},
                    ],
                    value='nenhuma_dose',
                    labelStyle={'display': 'block', 'margin': '5px 0'}
                )
            ], className='form-group'),

        ], style={
            'width': '50%',
            'padding': '30px',
            'border-right': '1px solid #eee'
        }),

        ## 🤖 Coluna Direita (Resultado IA)
        html.Div(id='ia-output', style={
            'width': '50%',
            'padding': '30px',
            'background-color': '#f9f9f9'
        }),

    ], style={'display': 'flex', 'border-radius': '10px', 'box-shadow': '0 0 10px rgba(0,0,0,0.05)', 'overflow': 'hidden'}),

    html.Button('🚀 Submeter', id='submit-button', n_clicks=0, style={
        'background-color': '#1e90ff',
        'color': 'white',
        'padding': '12px 24px',
        'font-size': '16px',
        'border': 'none',
        'border-radius': '8px',
        'cursor': 'pointer',
        'margin': '30px auto',
        'display': 'block'
    }),

    html.Div(id='output-container', style={'text-align': 'center', 'margin-top': '20px', 'font-size': '16px', 'color': '#333'})
])