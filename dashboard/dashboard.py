import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash_IA import render_ai_form_content
from dash_view import render_dashboard_content, dados_dash_2020_2024
import os, sys

# Adiciona a referencia da pasta IA_Models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from IA_Models.modelo_otimizado import modelo_otimizado



# organiza a lista para armazenar os dados do paciente para o processamento de IA
paciente = pd.read_csv('datasets/Brasil-2021-processado_IA.csv')

# Limpa o dataframe do paciente mas mantem
paciente = paciente.iloc[0:0]
# lista todas as colunas
colunas = paciente.columns.tolist()

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
        return render_dashboard_content()
    elif tab == 'tab-ai':
        return render_ai_form_content()

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
        info_paciente['genero'] = genero
        info_paciente['idade'] = idade

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
        paciente = paciente.drop(columns=['diagnosticoCOVID'], errors='ignore')

        # aplica o modelo de IA para prever a probabilidade de ter covid
        previsao = modelo_otimizado.predict_proba(paciente)
        prob_nao_covid = previsao[0][0]
        prob_covid = previsao[0][1]

        # Calcula a porcentagem de pessoas com cada sintoma que estavam ou não com COVID
        sintomas_cols = sintomas_gerais + outros_sintomas if sintomas_gerais and outros_sintomas else sintomas_gerais or outros_sintomas
        frequencia_sintomas = dados_dash_2020_2024.groupby('diagnosticoCOVID')[sintomas_cols].mean().reset_index()
        frequencia_sintomas_long = frequencia_sintomas.melt(id_vars='diagnosticoCOVID', var_name='Sintoma', value_name='Frequência')
        frequencia_sintomas_long['Frequência'] *= 100
        frequencia_sintomas_long['diagnosticoCOVID'] = frequencia_sintomas_long['diagnosticoCOVID'].map({0: 'Covid negativo', 1: 'COVID Positivo'})

        # Criar gráfico de barras
        dist_sintomas = px.bar(frequencia_sintomas_long, x='Sintoma', y='Frequência', color='diagnosticoCOVID',
                               barmode='group',
                               title="Frequência de Sintomas por Diagnóstico de COVID",
                               labels={'diagnosticoCOVID': 'Diagnóstico', 'Frequência': 'Porcentagem de Sintomas'})
        dist_sintomas.update_layout(xaxis_title='Sintoma', yaxis_title='Porcentagem de Sintomas', xaxis_tickangle=-45)

        # Formata a exibição dos resultados
        return html.Div([
            html.H3("Resultado da Análise", style={'color': '#1e90ff', 'font-family': 'Arial, sans-serif'}),
            html.P(f"Nome: {nome}", style={'font-size': '18px', 'color': '#333'}),
            html.P(f"Gênero: {genero}", style={'font-size': '18px', 'color': '#333'}),
            html.P(f"Idade: {idade}", style={'font-size': '18px', 'color': '#333'}),
            html.P(f"Sintomas Gerais: {', '.join(sintomas_gerais) if sintomas_gerais else 'Nenhum'}",
                   style={'font-size': '18px', 'color': '#333'}),
            html.P(f"Outros Sintomas: {', '.join(outros_sintomas) if outros_sintomas else 'Nenhum'}",
                   style={'font-size': '18px', 'color': '#333'}),
            html.P(f"Comorbidades: {', '.join(comorbidades) if comorbidades else 'Nenhuma'}",
                   style={'font-size': '18px', 'color': '#333'}),
            html.P(f"Vacinação: {vacinacao}", style={'font-size': '18px', 'color': '#333'}),
            html.P(f"Chances de não ter COVID: {prob_nao_covid:.2%}", style={'font-size': '18px', 'color': '#333'}),
            html.P(f"Chances de ter COVID: {prob_covid:.2%}",
                   style={'font-size': '18px', 'color': '#333', 'font-weight': 'bold'}),
            dcc.Graph(figure=dist_sintomas)
        ], style={'border-radius': '10px', 'background-color': '#f9f9f9', 'padding': '20px',
                  'box-shadow': '0px 0px 10px rgba(0, 0, 0, 0.1)'})
    return html.Div()

# Rodar o servidor
if __name__ == '__main__':
    app.run(debug=True)
