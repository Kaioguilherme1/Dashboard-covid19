import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash_IA import render_ai_form_content
from dash_view import render_dashboard_content
import os, sys

# Adiciona a referencia da pasta IA_Models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from IA_Models.modelo_otimizado import modelo_otimizado


# Carrega os datasets
dados_IA = pd.read_csv('datasets/Brasil-2021-processado_IA.csv')
dados_IA_2020_2024 = pd.read_csv('datasets/Brasil-2020-2024-processado_IA.csv')
dados_limpos_2020 = pd.read_csv('datasets/Brasil-2020-limpo.csv')
dados_limpos_2021 = pd.read_csv('datasets/Brasil-2021-limpo.csv')
dados_limpos_2022 = pd.read_csv('datasets/Brasil-2022-limpo.csv')
dados_limpos_2023 = pd.read_csv('datasets/Brasil-2023-limpo.csv')
dados_limpos_2024 = pd.read_csv('datasets/Brasil-2024-limpo.csv')

# Concatena os dados de 2020 a 2024
dados_limpos_2020_2024 = pd.concat([dados_limpos_2020, dados_limpos_2021, dados_limpos_2022, dados_limpos_2023, dados_limpos_2024])
dados_IA_2020_2024 = dados_IA_2020_2024.reset_index(drop=True)
dados_limpos_2020_2024 = dados_limpos_2020_2024.reset_index(drop=True)

# Concatena os DataFrames ao longo das colunas (axis=1)
dados_dash_2020_2024 = pd.concat([dados_limpos_2020_2024, dados_IA_2020_2024], axis=1)

# Remove colunas duplicadas
dados_dash_2020_2024 = dados_dash_2020_2024.loc[:, ~dados_dash_2020_2024.columns.duplicated()]

# Adiciona colunas auxiliares
dados_dash_2020_2024['ano'] = pd.to_datetime(dados_dash_2020_2024['dataNotificacao']).dt.year
faixa_etaria_bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100]
faixa_etaria_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
dados_dash_2020_2024['faixa_etaria'] = pd.cut(dados_dash_2020_2024['idade'], bins=faixa_etaria_bins, labels=faixa_etaria_labels, right=False)



# organiza a lista para armazenar os dados do paciente para o processamento de IA
Sintomas = pd.read_csv('datasets/Brasil-2021-processado_IA.csv')
dataset_limpo = pd.read_csv('datasets/Brasil-2021-limpo.csv')
# seleciona somente as colunas de idade e sexo do dataset_limpo
dados = dataset_limpo[['idade', 'sexo']]
# adiciona as colunas do dataset Sintomas
paciente = pd.concat([dados, Sintomas], axis=1)

# Limpa o dataframe do paciente mas mantem
paciente = paciente.iloc[0:0]
# lista todas as colunas
colunas = paciente.columns.tolist()
print(colunas)

# Inicializar o app Dash com suppress_callback_exceptions=True
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Layout com duas abas (Dashboards e IA)
app.layout = html.Div(
    style={
        'display': 'flex',
        'min-height': '100vh',
        'background-color': '#e0f7fa',
        'flex-direction': 'row',
        'border-radius': '10px',
    },
    children=[
        # Menu de abas na lateral esquerda
        html.Div(
            style={
                'width': '220px',
                'background-color': '#ffffff',
                'border-radius': '10px 0 0 10px',
                'padding': '20px',
                'display': 'flex',
                'flexDirection': 'column',
                'height': '100vh',
                'box-shadow': '4px 0px 15px rgba(0, 0, 0, 0.1)',
                'color': '#0288d1',
            },
            children=[
                dcc.Tabs(
                    id="tabs",
                    value='tab-dashboard',
                    children=[
                        dcc.Tab(label='Dashboards', value='tab-dashboard', style={
                            'background-color': 'transparent',
                            'color': '#0288d1',
                            'border': 'none',
                            'border-radius': '8px',
                            'font-family': 'Arial, sans-serif',
                            'padding': '10px 20px',
                            'font-weight': 'bold',
                            'text-align': 'center',
                            'transition': 'background-color 0.3s ease'
                        }),
                        dcc.Tab(label='Inteligência Artificial', value='tab-ai', style={
                            'background-color': 'transparent',
                            'color': '#0288d1',
                            'border': 'none',
                            'border-radius': '8px',
                            'font-family': 'Arial, sans-serif',
                            'padding': '10px 20px',
                            'font-weight': 'bold',
                            'text-align': 'center',
                            'transition': 'background-color 0.3s ease'
                        }),
                    ],
                    style={
                        'height': '100%',
                        'flex': 1,
                        'background-color': 'transparent',
                        'color': '#0288d1',
                        'border': 'none',
                        'font-family': 'Arial, sans-serif',
                        'border-radius': '8px',
                    },
                    className='custom-tabs',
                    vertical=True,
                ),
            ]
        ),

        # Conteúdo das abas
        html.Div(
            html.H1("Dashboard de Dados Covid19 de 2020 - 2024", style={'color': '#1e90ff', 'font-family': 'Arial, sans-serif'}),
            id='tabs-content',
            style={
                'flex': 1,
                'padding': '20px',
                'background-color': '#ffffff',
                'border-radius': '10px',
                'height': '100vh',
                'overflow-y': 'auto',
                'box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.1)',
            }
        )
    ]
)


# Callback para atualizar o conteúdo com base na aba selecionada
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    if tab == 'tab-dashboard':
        return render_dashboard_content(dados_dash_2020_2024)
    elif tab == 'tab-ai':
        return render_ai_form_content()


@app.callback(
    [
        Output('filtered-data', 'children'),
        Output('sexo-dropdown', 'options'),
        Output('sexo-dropdown', 'value'),
        Output('idade-slider', 'value'),
        Output('sintomas-dropdown', 'options'),
        Output('sintomas-dropdown', 'value'),
        Output('idade-slider', 'min'),
        Output('idade-slider', 'max'),
    ],
    [
        Input('idade-slider', 'value'),
        Input('sexo-dropdown', 'value'),
        Input('sintomas-dropdown', 'value'),
    ],
    prevent_initial_call=True
)
def atualizar_filtros_e_dashboard(idade_range, sexo_selecionado, sintomas_selecionados):
    global dados_dash_2020_2024

    # Base original para opções de filtro
    dados_originais = dados_dash_2020_2024.copy()
    dados_filtrados = dados_originais.copy()

    # Aplicação dos filtros
    if idade_range:
        dados_filtrados = dados_filtrados[
            (dados_filtrados['idade'] >= idade_range[0]) &
            (dados_filtrados['idade'] <= idade_range[1])
            ]

    if sexo_selecionado:
        dados_filtrados = dados_filtrados[dados_filtrados['sexo'].isin(sexo_selecionado)]

    if sintomas_selecionados:
        for sintoma in sintomas_selecionados:
            if sintoma in dados_filtrados.columns:
                dados_filtrados = dados_filtrados[dados_filtrados[sintoma] == 1]

    # Renderiza conteúdo do dashboard com dados filtrados
    dashboard_content = render_dashboard_content(dados_filtrados)

    # Atualiza opções dos filtros
    sexo_options = [{'label': s, 'value': s} for s in sorted(dados_originais['sexo'].dropna().unique())]
    sintomas_options = [{'label': s, 'value': s} for s in ['dor_corpo', 'dor_costas', 'dor_abdomen', 'dor_toracica', 'dor_peito', 'dor_olhos', 'dor_geral', 'mialgia', 'algia', 'fadiga', 'febre', 'tosse', 'coriza', 'congestao_nasal', 'diarreia', 'nausea', 'vomito', 'espirros', 'olfato_alterado', 'paladar_alterado', 'garganta', 'dor_de_cabeca', 'mal_estar', 'dor_de_ouvido', 'tontura', 'desconforto_respiratorio', 'saturacao_baixa', 'sintomas_indefinidos', 'asma', 'hipertensao', 'sem_comorbidade', 'diabetes', 'bronquite', 'tabagismo', 'epilepsia', 'ansiedade', 'hipotireoidismo', 'tireoidite', 'rinite', 'sinusite', 'hipotensao', 'comorbidades_indefinidas', 'nao_declarado', 'pre_operatorio', 'Esclerose Lateral Amiotrófica', 'tomouPrimeiraDose', 'tomouSegundaDose', 'diagnosticoCOVID']]

    # Mantém o intervalo atual de idade caso já esteja definido
    idade_min = int(dados_originais['idade'].min())
    idade_max = int(dados_originais['idade'].max())
    idade_value = idade_range if idade_range else [idade_min, idade_max]

    return (
        dashboard_content,
        sexo_options,
        sexo_selecionado,
        idade_value,
        sintomas_options,
        sintomas_selecionados,
        idade_min,
        idade_max
    )


# Callback para exibir os dados selecionados
@app.callback(
    Output('ia-output', 'children'),
    Input('submit-button', 'n_clicks'),
    State('nome', 'value'),
    State('genero', 'value'),
    State('idade', 'value'),
    State('sintomas-gerais-tags', 'value'),
    State('outros-sintomas-tags', 'value'),
    State('comorbidades-tags', 'value'),
    State('vacinacao-dose', 'value')
)
def update_output(n_clicks, nome, genero, idade, sintomas_gerais, outros_sintomas, comorbidades, vacinacao):
    global paciente
    # Cria um dicionario com as mesmas colunas e orden do dataframe paciente
    dados_paciente = {coluna: 0 for coluna in paciente.columns}
    if n_clicks > 0:

        # Preenche os dados do paciente
        info_paciente = {}
        info_paciente['nome'] = nome
        sexo = 0
        # converte o genero para label antes de adicionar ao dicionario
        if genero == 'Masculino':
            sexo = 1
        elif genero == 'Feminino':
            sexo = 2
        elif genero == 'Outro':
            sexo = 3
        dados_paciente['sexo'] = sexo
        dados_paciente['idade'] = idade


        # Adiciona sintomas gerais ao dicionário
        if sintomas_gerais:
            for sintoma in sintomas_gerais:
                dados_paciente[sintoma] = 1

        # Adiciona outros sintomas ao dicionário
        if outros_sintomas:
            for sintoma in outros_sintomas:
                dados_paciente[sintoma] = 1

        # Adiciona comorbidades ao dicionário
        if comorbidades:
            for comorbidade in comorbidades:
                dados_paciente[comorbidade] = 1

        # Adiciona vacinação ao dicionário
        if vacinacao != 'nenhuma_dose':
            dados_paciente[vacinacao] = 1

        # Converte o dicionário em um DataFrame
        paciente = pd.DataFrame([dados_paciente])
        # remove a coluna diagnosticoCOVID
        paciente = paciente.drop(columns=['diagnosticoCOVID','dor_toracica', 'diarreia', 'nausea', 'vomito', 'espirros'], errors='ignore')

        # aplica o modelo de IA para prever a probabilidade de ter covid
        previsao = modelo_otimizado.predict_proba(paciente)
        prob_nao_covid = previsao[0][0]
        prob_covid = previsao[0][1]

        # pega o numero de linhas da base
        num_linhas = dados_dash_2020_2024.shape[0]

        if sintomas_gerais is not None or outros_sintomas is not None or comorbidades is not None:
            # Calcula a porcentagem de pessoas com cada sintoma que estavam ou não com COVID
            sintomas_cols = sintomas_gerais + outros_sintomas + comorbidades if sintomas_gerais and outros_sintomas and comorbidades else sintomas_gerais or outros_sintomas or comorbidades

            frequencia_sintomas = dados_dash_2020_2024.groupby('diagnosticoCOVID')[sintomas_cols].mean().reset_index()
            frequencia_sintomas_long = frequencia_sintomas.melt(id_vars='diagnosticoCOVID', var_name='Sintoma', value_name='Frequência')
            frequencia_sintomas_long['Frequência'] *= 100
            frequencia_sintomas_long['diagnosticoCOVID'] = frequencia_sintomas_long['diagnosticoCOVID'].map({0: 'Covid negativo', 1: 'COVID Positivo'})
        else:
            frequencia_sintomas_long = pd.DataFrame(columns=['diagnosticoCOVID', 'Sintoma', 'Frequência'])

        # Criar gráfico de barras para sintomas
        dist_sintomas = px.bar(frequencia_sintomas_long, x='Sintoma', y='Frequência', color='diagnosticoCOVID',
                               barmode='group',
                               title=f"Frequência de Sintomas por Diagnóstico de COVID entre {num_linhas} pacientes ",
                               labels={'diagnosticoCOVID': 'Diagnóstico', 'Frequência': 'Porcentagem de Sintomas'},
                               facet_col='diagnosticoCOVID')
        dist_sintomas.update_layout(xaxis_title='Sintoma', yaxis_title='Porcentagem de Sintomas', xaxis_tickangle=-45)

        # Formata a exibição dos resultados
        return html.Div([
                html.H3("🔍 Resultado da Análise", style={
                    'color': '#1e90ff',
                    'font-family': 'Arial, sans-serif',
                    'margin-bottom': '20px'
                }),

                # Grupo: Dados pessoais
                html.Div([
                    html.Div([
                        html.P("👤 Nome:", style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.P(nome, style={'font-size': '17px', 'color': '#333'})
                    ], style={'flex': '2'}),

                    html.Div([
                        html.P("⚧️ Gênero:", style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.P(genero, style={'font-size': '17px', 'color': '#333'})
                    ], style={'flex': '1'}),

                    html.Div([
                        html.P("🎂 Idade:", style={'font-weight': 'bold', 'margin-bottom': '2px'}),
                        html.P(f"{idade} anos", style={'font-size': '17px', 'color': '#333'})
                    ], style={'flex': '1'}),
                ], style={'display': 'flex', 'gap': '20px', 'margin-bottom': '20px'}),

                # Grupo: Sintomas e comorbidades
                html.Div([
                    html.P("🦠 Sintomas Gerais:", style={'font-weight': 'bold'}),
                    html.P(', '.join(sintomas_gerais) if sintomas_gerais else 'Nenhum', style={'margin-bottom': '10px'}),

                    html.P("🤒 Outros Sintomas:", style={'font-weight': 'bold'}),
                    html.P(', '.join(outros_sintomas) if outros_sintomas else 'Nenhum', style={'margin-bottom': '10px'}),

                    html.P("💊 Comorbidades:", style={'font-weight': 'bold'}),
                    html.P(', '.join(comorbidades) if comorbidades else 'Nenhuma', style={'margin-bottom': '10px'}),

                    html.P("💉 Vacinação:", style={'font-weight': 'bold'}),
                    html.P(vacinacao, style={'margin-bottom': '20px'}),
                ], style={'font-size': '17px', 'color': '#333'}),

                # Grupo: Resultados da previsão
                html.Div([
                    html.P("📈 Chances de NÃO ter COVID:", style={
                        'font-weight': 'bold',
                        'color': '#2e8b57'
                    }),
                    html.P(f"{prob_nao_covid:.2%}", style={
                        'font-size': '20px',
                        'color': '#2e8b57',
                        'margin-bottom': '10px'
                    }),

                    html.P("📉 Chances de TER COVID:", style={
                        'font-weight': 'bold',
                        'color': '#b22222'
                    }),
                    html.P(f"{prob_covid:.2%}", style={
                        'font-size': '22px',
                        'font-weight': 'bold',
                        'color': '#b22222',
                        'margin-bottom': '20px'
                    }),
                ]),

                # Gráfico de distribuição dos sintomas
                dcc.Graph(figure=dist_sintomas)

            ], style={
                'border-radius': '12px',
                'background-color': '#f9f9f9',
                'padding': '30px',
                'box-shadow': '0px 4px 12px rgba(0, 0, 0, 0.1)',
                'font-family': 'Arial, sans-serif',
                'margin-top': '20px'
            })
    return html.Div()

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)
