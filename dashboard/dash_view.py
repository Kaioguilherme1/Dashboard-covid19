import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash
import plotly.graph_objects as go
from sympy.physics.units import length

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
data_filtro = pd.concat([dados_limpos_2020_2024, dados_IA_2020_2024], axis=1)

# Remove colunas duplicadas
data_filtro = data_filtro.loc[:, ~data_filtro.columns.duplicated()]

# Adiciona colunas auxiliares
data_filtro['ano'] = pd.to_datetime(data_filtro['dataNotificacao']).dt.year
faixa_etaria_bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100]
faixa_etaria_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
data_filtro['faixa_etaria'] = pd.cut(data_filtro['idade'], bins=faixa_etaria_bins, labels=faixa_etaria_labels, right=False)


def criar_indicador(valor, titulo, cor):
    return go.Figure(go.Indicator(
        mode="number",
        value=valor,
        title={"text": titulo},
        number={"font": {"color": cor}}
    ))

# Função para renderizar o conteúdo do dashboard
def render_dashboard_content(dados_dash_2020_2024):
    # Estatísticas principais
    total_casos = len(dados_dash_2020_2024)
    total_confirmados = dados_dash_2020_2024[dados_dash_2020_2024['diagnosticoCOVID'] == 1].shape[0]
    total_negativos = dados_dash_2020_2024[dados_dash_2020_2024['diagnosticoCOVID'] == 0].shape[0]
    taxa_confirmados = (total_confirmados / total_casos) * 100 if total_casos > 0 else 0

    # Indicadores
    total_casos_fig = criar_indicador(total_casos, "Total de Casos", "#333")
    casos_confirmados_fig = criar_indicador(total_confirmados, "Casos Confirmados", "#1e90ff")
    casos_negativos_fig = criar_indicador(total_negativos, "Casos Negativos", "#ff6347")
    taxa_confirmados_fig = criar_indicador(taxa_confirmados, "Taxa de Confirmação (%)", "#32cd32")

    # Gráficos
    faixa_etaria_fig = px.line(
        dados_dash_2020_2024.groupby(['ano', 'faixa_etaria']).size().reset_index(name='Número de Casos'),
        x='ano', y='Número de Casos', color='faixa_etaria',
        title="Evolução Temporal dos Casos por Faixa Etária"
    )

    dist_idade_fig = px.histogram(
        dados_dash_2020_2024, x='idade', nbins=30, title="Distribuição de Idade",
        labels={'idade': 'Idade', 'count': 'Frequência'}, color_discrete_sequence=['blue']
    )

    sintomas_cols = [col for col in dados_dash_2020_2024.columns if 'sintomas_' in col or 'outrosSintomas_' in col]
    frequencia_sintomas = dados_dash_2020_2024.groupby('diagnosticoCOVID')[sintomas_cols].mean().reset_index()
    frequencia_sintomas_long = frequencia_sintomas.melt(id_vars='diagnosticoCOVID', var_name='Sintoma', value_name='Frequência')
    frequencia_sintomas_long['Frequência'] *= 100
    sintomas_frequentes_fig = px.bar(
        frequencia_sintomas_long.groupby('Sintoma')['Frequência'].mean().nlargest(20).reset_index(),
        x='Frequência', y='Sintoma', orientation='h', title="Top 20 Sintomas Mais Frequentes"
    )
    casos_por_ano_fig = px.bar(
        dados_dash_2020_2024.groupby('ano').size().reset_index(name='Número de Casos'),
        x='ano', y='Número de Casos', title="Distribuição de Casos por Ano",
        labels={'ano': 'Ano', 'Número de Casos': 'Número de Casos'}
    )
    proporcao_casos_fig = px.pie(
        names=['Confirmados', 'Negativos'],
        values=[total_confirmados, total_negativos],
        title="Proporção de Casos Confirmados e Negativos"
    )
    # Filtra os 20 sintomas mais frequentes
    top_20_sintomas = frequencia_sintomas_long.groupby('Sintoma')['Frequência'].mean().nlargest(20).index
    frequencia_sintomas_top_20 = frequencia_sintomas_long[frequencia_sintomas_long['Sintoma'].isin(top_20_sintomas)]

    # Gráfico atualizado com os 20 sintomas mais frequentes
    sintomas_empilhados_fig = px.bar(
        frequencia_sintomas_top_20,
        x='Sintoma',
        y='Frequência',
        color='diagnosticoCOVID',
        barmode='stack',
        title="Top 20 Sintomas Mais Frequentes por Diagnóstico",
        labels={'diagnosticoCOVID': 'Diagnóstico', 'Frequência': 'Porcentagem'}
    )

    # Ajusta o layout do gráfico
    sintomas_empilhados_fig.update_layout(
        xaxis_title="Sintomas",
        yaxis_title="Porcentagem",
        xaxis_tickangle=-45,
        legend_title="Diagnóstico"
    )

    # Filtra as colunas relacionadas a comorbidades
    comorbidades_cols = [col for col in dados_dash_2020_2024.columns if 'outrasCondicoes_' in col]

    # Calcula a frequência média de cada comorbidade por diagnóstico
    frequencia_comorbidades = dados_dash_2020_2024.groupby('diagnosticoCOVID')[comorbidades_cols].mean().reset_index()
    frequencia_comorbidades_long = frequencia_comorbidades.melt(id_vars='diagnosticoCOVID', var_name='Comorbidade', value_name='Frequência')
    frequencia_comorbidades_long['Frequência'] *= 100  # Converte para porcentagem

    # Seleciona as 20 comorbidades mais frequentes
    top_20_comorbidades = frequencia_comorbidades_long.groupby('Comorbidade')['Frequência'].mean().nlargest(20).index
    frequencia_comorbidades_top_20 = frequencia_comorbidades_long[frequencia_comorbidades_long['Comorbidade'].isin(top_20_comorbidades)]

    # Gráfico atualizado com as 20 comorbidades mais frequentes
    comorbidades_fig = px.bar(
        frequencia_comorbidades_top_20,
        x='Comorbidade',
        y='Frequência',
        color='diagnosticoCOVID',
        barmode='stack',
        title="Top 20 Comorbidades Mais Frequentes por Diagnóstico",
        labels={'diagnosticoCOVID': 'Diagnóstico', 'Frequência': 'Porcentagem'}
    )

    # Ajusta o layout do gráfico
    comorbidades_fig.update_layout(
        xaxis_title="Comorbidades",
        yaxis_title="Porcentagem",
        xaxis_tickangle=-45,
        legend_title="Diagnóstico"
    )

    return html.Div([
        html.H1("Dashboard de Dados de COVID-19 (2020 - 2024)", style={'textAlign': 'center', 'color': '#1e90ff'}),

        # Filtros
        html.Div([
          html.Div([
              html.Label("Idade:"),
              dcc.RangeSlider(
                  id='idade-slider',
                  min=data_filtro['idade'].min(),
                  max=data_filtro['idade'].max(),
                  step=1,
                  marks={i: str(i) for i in range(int(data_filtro['idade'].min()), int(data_filtro['idade'].max()) + 1, 10)},
                  value=[data_filtro['idade'].min(), data_filtro['idade'].max()]
              )
          ], style={'width': '25%', 'display': 'inline-block'}),
          html.Div([
              html.Label("Sexo:"),
              dcc.Dropdown(
                  id='sexo-dropdown',
                  options=[{'label': sexo, 'value': sexo} for sexo in data_filtro['sexo'].unique()],
                  multi=True, placeholder="Selecione o sexo",
              )
          ], style={'width': '25%', 'display': 'inline-block'}),
          html.Div([
              html.Label("Sintomas:"),
              dcc.Dropdown(
                  id='sintomas-dropdown',
                  options=[{'label': sintoma, 'value': sintoma} for sintoma in data_filtro.columns if 'sintomas_' in sintoma],
                  multi=True, placeholder="Selecione os sintomas",
              )
          ], style={'width': '25%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'justify-content': 'space-between', 'padding': '20px'}),

        # Indicadores
        html.Div([
            html.Div(dcc.Graph(figure=total_casos_fig), style={'width': '24%','height': '3%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(figure=casos_confirmados_fig), style={'width': '24%','height': '3%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(figure=casos_negativos_fig), style={'width': '24%','height': '3%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(figure=taxa_confirmados_fig), style={'width': '24%','height': '3%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'justify-content': 'space-between'}),

        # Gráficos
        html.Div([
            html.Div(dcc.Graph(figure=faixa_etaria_fig), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(figure=dist_idade_fig), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(figure=sintomas_frequentes_fig), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(figure=comorbidades_fig), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(figure=proporcao_casos_fig), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(figure=sintomas_empilhados_fig), style={'width': '48%', 'display': 'inline-block'}),
            html.Div(dcc.Graph(figure=casos_por_ano_fig), style={'width': '48%', 'display': 'inline-block'}),
        ], style={'display': 'flex', 'flex-wrap': 'wrap', 'justify-content': 'space-between'}),
    ], id='filtered-data')