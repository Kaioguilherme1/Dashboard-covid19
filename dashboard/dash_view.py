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

print(dados_IA.columns.to_list())

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
    taxa_confirmados_fig = criar_indicador(taxa_confirmados, "Taxa Confirmados (%)", "#32cd32")

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

    # Lista manual das colunas de sintomas
    sintomas_cols = [
        'dor_corpo', 'dor_costas', 'dor_abdomen',
        'dor_peito', 'dor_olhos', 'dor_geral', 'mialgia', 'algia',
        'fadiga', 'febre', 'tosse', 'coriza', 'congestao_nasal',
        'diarreia', 'nausea', 'olfato_alterado',
        'paladar_alterado', 'garganta', 'dor_de_cabeca',
        'mal_estar', 'dor_de_ouvido', 'tontura', 'desconforto_respiratorio',
        'saturacao_baixa', 'sintomas_indefinidos'
    ]

    # Calcula a frequência média por diagnóstico
    frequencia_sintomas = dados_dash_2020_2024.groupby('diagnosticoCOVID')[sintomas_cols].mean().reset_index()

    # Transforma em formato longo
    frequencia_sintomas_long = frequencia_sintomas.melt(
        id_vars='diagnosticoCOVID',
        var_name='Sintoma',
        value_name='Frequência'
    )

    # Converte para porcentagem
    frequencia_sintomas_long['Frequência'] *= 100

    # Calcula frequência média geral por sintoma
    frequencia_media_sintomas = frequencia_sintomas_long.groupby('Sintoma')['Frequência'].mean().reset_index()

    # Ordena por frequência
    frequencia_media_sintomas = frequencia_media_sintomas.sort_values(by='Frequência', ascending=False)

    # Gráfico com todos os sintomas ordenados por frequência
    sintomas_frequentes_fig = px.bar(
        frequencia_media_sintomas,
        x='Frequência',
        y='Sintoma',
        orientation='h',
        title="Frequência Média de Todos os Sintomas Reportados",
        labels={'Frequência': 'Frequência (%)', 'Sintoma': 'Nome do Sintoma'},
        color_discrete_sequence=['#1e90ff']
    )

    # Ordenação visual e layout
    sintomas_frequentes_fig.update_layout(
        yaxis=dict(categoryorder='total ascending'),
        template='plotly_white'
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
    # Obtém os 20 sintomas mais frequentes com base na média da frequência
    top_20_sintomas = (
        frequencia_sintomas_long
        .groupby('Sintoma')['Frequência']
        .mean()
        .sort_values(ascending=False)
        .head(20)
        .index
    )

    # Filtra os dados apenas com os top 20 e mantém a ordem
    frequencia_sintomas_top_20 = (
        frequencia_sintomas_long[
            frequencia_sintomas_long['Sintoma'].isin(top_20_sintomas)
        ]
        .copy()
    )

    # Garante que a ordem dos sintomas respeite o ranking
    frequencia_sintomas_top_20['Sintoma'] = pd.Categorical(
        frequencia_sintomas_top_20['Sintoma'],
        categories=top_20_sintomas,
        ordered=True
    )

    # Ordena o DataFrame de acordo com a ordem dos top sintomas
    frequencia_sintomas_top_20 = frequencia_sintomas_top_20.sort_values('Sintoma')
    # faz o map da diagnosticoCOVID
    frequencia_sintomas_top_20['diagnosticoCOVID'] = frequencia_sintomas_top_20['diagnosticoCOVID'].map({0: 'Negativo', 1: 'Positivo'})

    # Gráfico atualizado com os 20 sintomas mais frequentes
    sintomas_empilhados_fig = px.bar(
        frequencia_sintomas_top_20,
        x='Sintoma',
        y='Frequência',
        color='diagnosticoCOVID',
        barmode='stack',
        title="Top Sintomas Mais Frequentes por Diagnóstico",
        labels={'diagnosticoCOVID': 'Diagnóstico', 'Frequência': 'Porcentagem'},
        color_discrete_map = {
            'Positivo': '#d62728',  # vermelho
            'Negativo': '#1f77b4'  # azul
        },
        category_orders={
            'diagnosticoCOVID': ['Positivo', 'Negativo']
        }
    )

    # Ajusta o layout do gráfico
    sintomas_empilhados_fig.update_layout(
        xaxis_title="Sintomas",
        yaxis_title="Porcentagem",
        xaxis_tickangle=-45,
        legend_title="Diagnóstico"
    )

    # Filtra as colunas relacionadas a comorbidades
    comorbidades_cols  = [
    'asma', 'hipertensao', 'sem_comorbidade', 'diabetes', 'bronquite',
    'tabagismo', 'epilepsia', 'ansiedade', 'hipotireoidismo',
    'tireoidite', 'rinite', 'sinusite', 'hipotensao',
    'comorbidades_indefinidas', 'nao_declarado', 'pre_operatorio',
    'Esclerose Lateral Amiotrófica']

    # Calcula a frequência média de cada comorbidade por diagnóstico
    frequencia_comorbidades = (
        dados_dash_2020_2024
        .groupby('diagnosticoCOVID')[comorbidades_cols]
        .mean()
        .reset_index()
    )

    # Transforma para formato longo
    frequencia_comorbidades_long = (
        frequencia_comorbidades
        .melt(
            id_vars='diagnosticoCOVID',
            var_name='Comorbidade',
            value_name='Frequência'
        )
    )

    # Converte para porcentagem
    frequencia_comorbidades_long['Frequência'] *= 100

    # Seleciona as 20 comorbidades mais frequentes com base na média
    top_20_comorbidades = (
        frequencia_comorbidades_long
        .groupby('Comorbidade')['Frequência']
        .mean()
        .sort_values(ascending=False)
        .head(20)
        .index
    )

    # Filtra os dados mantendo apenas as top 20 comorbidades
    frequencia_comorbidades_top_20 = (
        frequencia_comorbidades_long[
            frequencia_comorbidades_long['Comorbidade'].isin(top_20_comorbidades)
        ]
        .copy()
    )

    # Define ordem categórica para manter a ordenação nos gráficos
    frequencia_comorbidades_top_20['Comorbidade'] = pd.Categorical(
        frequencia_comorbidades_top_20['Comorbidade'],
        categories=top_20_comorbidades,
        ordered=True
    )

    # Ordena o DataFrame de acordo com o ranking
    frequencia_comorbidades_top_20 = frequencia_comorbidades_top_20.sort_values('Comorbidade')
    # faz o map da diagnosticoCOVID
    frequencia_comorbidades_top_20['diagnosticoCOVID'] = frequencia_comorbidades_top_20['diagnosticoCOVID'].map({0: 'Negativo', 1: 'Positivo'})

    # Gráfico atualizado com as 20 comorbidades mais frequentes
    comorbidades_fig = px.bar(
        frequencia_comorbidades_top_20,
        x='Comorbidade',
        y='Frequência',
        color='diagnosticoCOVID',
        barmode='stack',
        title="Top Comorbidades Mais Frequentes por Diagnóstico",
        labels={'diagnosticoCOVID': 'Diagnóstico', 'Frequência': 'Porcentagem'},
        color_discrete_map = {
            'Positivo': '#d62728',  # vermelho
            'Negativo': '#1f77b4'  # azul
        },
        category_orders = {
            'diagnosticoCOVID': ['Positivo', 'Negativo']
        }
    )

    # Ajusta o layout do gráfico
    comorbidades_fig.update_layout(
        xaxis_title="Comorbidades",
        yaxis_title="Porcentagem",
        xaxis_tickangle=-45,
        legend_title="Diagnóstico"
    )

    heat_data = frequencia_sintomas_top_20.pivot(index='Sintoma', columns='diagnosticoCOVID',
                                                 values='Frequência').fillna(0)

    return html.Div([
        # Cabeçalho Principal
        html.H1("🧠 Explorando Sintomas e Comorbidades com IA", style={
            'textAlign': 'center',
            'color': '#1e90ff',
            'fontSize': '36px',
            'marginTop': '20px'
        }),
        html.H3("Previsão e Visualização Interativa de Casos de COVID-19", style={
            'textAlign': 'center',
            'color': '#333',
            'fontWeight': '300',
            'marginBottom': '30px'
        }),

        html.Hr(),

        # Introdução do Projeto
        html.Div([
            html.H2("📌 Sobre o Projeto", style={'color': '#1e90ff'}),
            html.P(
                "Este dashboard é parte de um estudo acadêmico cujo objetivo é compreender como sintomas, comorbidades "
                "e fatores demográficos influenciam o diagnóstico de COVID-19. Utilizando dados do SINAN (Sistema de Informação de Agravos de Notificação), "
                "coletados entre os anos de 2020 a 2024, foi desenvolvido um modelo de Inteligência Artificial capaz de prever a probabilidade de diagnóstico positivo.",
                style={'textAlign': 'justify'}
            ),
            html.P(
                "Os dados aqui visualizados não apenas possibilitam a análise exploratória, mas também serviram como "
                "**base de treinamento para a IA preditiva**, reforçando a capacidade do modelo em aprender padrões a partir de registros clínicos reais.",
                style={'textAlign': 'justify', 'fontStyle': 'italic'}
            ),
            html.P("📂 Bases consultadas:", style={'marginTop': '15px'}),
            html.Ul([
                html.Li("Notificações de Síndrome Gripal - 2020"),
                html.Li("Notificações de Síndrome Gripal - 2021"),
                html.Li("Notificações de Síndrome Gripal - 2022"),
                html.Li("Notificações de Síndrome Gripal - 2023"),
                html.Li("Notificações de Síndrome Gripal - 2024"),
            ]),
        ], style={'padding': '25px', 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'margin': '20px'}),

        html.Hr(),

        # Filtros
        html.Div([
            html.H2("🎛️ Filtros Interativos", style={'color': '#1e90ff'}),
            html.P("Selecione as faixas de idade, sexo ou sintomas para ajustar os dados exibidos no dashboard."),
            html.Div([
                html.Div([
                    html.Label("Idade:"),
                    dcc.RangeSlider(
                        id='idade-slider',
                        min=data_filtro['idade'].min(),
                        max=data_filtro['idade'].max(),
                        step=1,
                        marks={i: str(i) for i in
                               range(int(data_filtro['idade'].min()), int(data_filtro['idade'].max()) + 1, 10)},
                        value=[data_filtro['idade'].min(), data_filtro['idade'].max()]
                    )
                ], style={'width': '30%', 'display': 'inline-block'}),
                html.Div([
                    html.Label("Sexo:"),
                    dcc.Dropdown(
                        id='sexo-dropdown',
                        options=[{'label': sexo, 'value': sexo} for sexo in data_filtro['sexo'].unique()],
                        multi=True,
                        placeholder="Selecione o sexo"
                    )
                ], style={'width': '30%', 'display': 'inline-block'}),
                html.Div([
                    html.Label("Sintomas:"),
                    dcc.Dropdown(
                        id='sintomas-dropdown',
                        options=[{'label': sintoma, 'value': sintoma} for sintoma in ['dor_corpo', 'dor_costas', 'dor_abdomen', 'dor_toracica', 'dor_peito', 'dor_olhos', 'dor_geral', 'mialgia', 'algia', 'fadiga', 'febre', 'tosse', 'coriza', 'congestao_nasal', 'diarreia', 'nausea', 'vomito', 'espirros', 'olfato_alterado', 'paladar_alterado', 'garganta', 'dor_de_cabeca', 'mal_estar', 'dor_de_ouvido', 'tontura', 'desconforto_respiratorio', 'saturacao_baixa', 'sintomas_indefinidos', 'asma', 'hipertensao', 'sem_comorbidade', 'diabetes', 'bronquite', 'tabagismo', 'epilepsia', 'ansiedade', 'hipotireoidismo', 'tireoidite', 'rinite', 'sinusite', 'hipotensao', 'comorbidades_indefinidas', 'nao_declarado', 'pre_operatorio', 'Esclerose Lateral Amiotrófica', 'tomouPrimeiraDose', 'tomouSegundaDose', 'diagnosticoCOVID']],
                        multi=True,
                        placeholder="Selecione os sintomas"
                    )
                ], style={'width': '30%', 'display': 'inline-block'}),
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '20px'}),
        ]),

        html.Hr(),

        # Indicadores
        html.Div([
            html.H2("📊 Visão Geral dos Casos", style={'color': '#1e90ff'}),
            html.P("Estatísticas principais dos registros clínicos notificados no período de 2020 a 2024."),
            html.Div([
                html.Div(dcc.Graph(figure=total_casos_fig), style={'width': '24%', 'display': 'inline-block'}),
                html.Div(dcc.Graph(figure=casos_confirmados_fig), style={'width': '24%', 'display': 'inline-block'}),
                html.Div(dcc.Graph(figure=casos_negativos_fig), style={'width': '24%', 'display': 'inline-block'}),
                html.Div(dcc.Graph(figure=taxa_confirmados_fig), style={'width': '24%', 'display': 'inline-block'}),
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        ]),

        html.Hr(),

        # Evolução Temporal
        html.Div([
            html.H2("📅 Evolução Temporal por Faixa Etária", style={'color': '#1e90ff'}),
            html.P("Análise temporal dos casos agrupados por faixas etárias e distribuição anual."),
            html.Div([
                html.Div(dcc.Graph(figure=faixa_etaria_fig), style={'width': '48%', 'display': 'inline-block'}),
                html.Div(dcc.Graph(figure=casos_por_ano_fig), style={'width': '48%', 'display': 'inline-block'}),
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        ]),

        html.Hr(),

        # Perfil Demográfico
        html.Div([
            html.H2("👤 Perfil Etário e Diagnóstico", style={'color': '#1e90ff'}),
            html.P("Distribuição das idades e proporção de diagnósticos positivos e negativos."),
            html.Div([
                html.Div(dcc.Graph(figure=dist_idade_fig), style={'width': '48%', 'display': 'inline-block'}),
                html.Div(dcc.Graph(figure=proporcao_casos_fig), style={'width': '48%', 'display': 'inline-block'}),
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        ]),

        html.Hr(),

        # Sessão: Sintomas e Comorbidades
        html.Div([
            html.H2("🤒 Distribuição de Sintomas e Comorbidades", style={'color': '#1e90ff'}),
            html.P(
                "Visualização das proporções de sintomas e comorbidades relatados nos registros clínicos. "
                "Os dados estão segmentados por diagnóstico de COVID-19,"
                "Essa separação permite uma análise comparativa entre os perfis clínicos de infectados e não infectados.",
                style={'font-size': '16px', 'color': '#555'}
            ),
            html.Div([
                html.Div(dcc.Graph(figure=sintomas_empilhados_fig), style={'width': '48%', 'display': 'inline-block'}),
                html.Div(dcc.Graph(figure=comorbidades_fig), style={'width': '48%', 'display': 'inline-block'}),
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),
        ]),

        html.Hr(),

        # Sessão: Sintomas mais Relevantes
        html.Div([
            html.H2("🧬 Frequência Geral dos Sintomas", style={'color': '#1e90ff'}),
            html.P(
                "Visualização dos sintomas relatados em ordem decrescente de frequência média, considerando todos os registros clínicos "
                "entre os anos de 2020 a 2024. Essa ordenação permite identificar os sintomas mais comuns observados independentemente do diagnóstico, ",
                style={'font-size': '16px', 'color': '#555'}
            ),
            html.Div([
                html.Div(dcc.Graph(figure=sintomas_frequentes_fig), style={'width': '100%', 'display': 'inline-block'}),
            ])
        ]),
        html.Hr(),


        html.Div([
            html.H4(
                "🔬 Este dashboard representa uma ponte entre dados clínicos e inteligência artificial aplicada à saúde pública.",
                style={'textAlign': 'center', 'fontStyle': 'italic', 'marginBottom': '40px', 'color': '#555'}),
        ])
    ], id='filtered-data')
