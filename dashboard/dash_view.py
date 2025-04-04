import pandas as pd
import plotly.express as px
from dash import dcc, html

# Carrega os datasets
dados_IA = pd.read_csv('datasets/Brasil-2021-processado_IA.csv')
dados_IA_2020_2024 = pd.read_csv('datasets/Brasil-2020-2024-processado_IA.csv')
dados_limpos_2020 = pd.read_csv('datasets/Brasil-2020-limpo.csv')
dados_limpos_2021 = pd.read_csv('datasets/Brasil-2021-limpo.csv')
dados_limpos_2022 = pd.read_csv('datasets/Brasil-2022-limpo.csv')
dados_limpos_2023 = pd.read_csv('datasets/Brasil-2023-limpo.csv')
dados_limpos_2024 = pd.read_csv('datasets/Brasil-2024-limpo.csv')
# faz a concatenação na lista dos dados de 2020 a 2024
dados_limpos_2020_2024 = pd.concat([dados_limpos_2020, dados_limpos_2021, dados_limpos_2022, dados_limpos_2023, dados_limpos_2024])

dados_IA_2020_2024 = dados_IA_2020_2024.reset_index(drop=True)
dados_limpos_2020_2024 = dados_limpos_2020_2024.reset_index(drop=True)

# Concatena os DataFrames ao longo das colunas (axis=1)
dados_dash_2020_2024 = pd.concat([dados_limpos_2020_2024, dados_IA_2020_2024], axis=1)
# Identifica colunas duplicadas
colunas_duplicadas = dados_dash_2020_2024.columns.duplicated(keep='first')
# Remove as colunas duplicadas
dados_dash_2020_2024 = dados_dash_2020_2024.loc[:, ~colunas_duplicadas]

# mostra as colunas do dataframe
# colunas = dados_dash_2020_2024.columns.tolist()
# print(colunas)

# Gráfico de distribuição de Idade
dist_idade = px.histogram(dados_dash_2020_2024, x='idade', nbins=30, title="Distribuição de Idade (2020 - 2024)",
                       labels={'idade': 'Idade', 'count': 'Frequência'},
                       color_discrete_sequence=['blue'], marginal='box')
dist_idade.update_layout(xaxis_title='Idade', yaxis_title='Frequência')

# Gráfico de distribuição da Classificação Final
dist_Clas_final = px.histogram(dados_dash_2020_2024, x='classificacaoFinal', title="Distribuição de Classificação Final dos Casos",
                       labels={'classificacaoFinal': 'Classificação Final', 'count': 'Número de Casos'},
                       color='classificacaoFinal',
                       histfunc='count')
dist_Clas_final.update_layout(xaxis_title='Classificação Final', yaxis_title='Número de Casos',
                  xaxis_tickangle=-45)  # Rotaciona os rótulos do eixo X

# Gráfico de distribuição dos sintomas de 2020 a 2024
sintomas_cols = ['outrosSintomas_DOR_NO_CORPO', 'outrosSintomas_DOR_NAS_COSTAS', 'outrosSintomas_DOR_ABDOMINAL', 'outrosSintomas_DOR_TORACICA', 'outrosSintomas_MIALGIA', 'outrosSintomas_ALGIA', 'outrosSintomas_CALAFRIOS', 'outrosSintomas_CONGESTAO_NASAL', 'outrosSintomas_DIARREIA', 'outrosSintomas_NAUSEA', 'outrosSintomas_VOMITO', 'outrosSintomas_ESPIRROS', 'outrosSintomas_FRAQUEZA_FADIGA', 'outrosSintomas_DOR_NOs_OLHOS', 'sintomas_Tosse', 'sintomas_Dor_de_Cabeça', 'diagnosticoCOVID', 'sintomas_Febre', 'sintomas_Dor_de_Garganta', 'sintomas_Coriza', 'outrosSintomas_DOR', 'outrasCondicoes_HA', 'outrasCondicoes_HAS', 'sintomas_Dispneia', 'outrasCondicoes_n', 'outrasCondicoes_HI', 'outrasCondicoes_SM', 'outrosSintomas_CORPO', 'outrasCondicoes_ASM', 'outrasCondicoes_ASMA', 'outrasCondicoes_CA', 'outrasCondicoes_NI', 'sintomas_Distúrbios_Gustativos', 'condicoes_Diabetes', 'outrosSintomas_NASAL', 'outrosSintomas_as', 'outrosSintomas_dor', 'sintomas_Distúrbios_Olfativos', 'outrasCondicoes_IPERTENSÃO', 'outrasCondicoes_HIPERTENSÃO', 'outrasCondicoes_IPERTENSA', 'outrasCondicoes_HIPERTENSA', 'outrosSintomas_Dor', 'outrosSintomas_FRIO', 'outrosSintomas_corpo', 'outrasCondicoes_Sem_Comorbidade', 'outrosSintomas_CANSAÇO', 'outrasCondicoes_BRONQUITE', 'outrasCondicoes_HIPERTENSAO', 'outrosSintomas_ASTENIA', 'outrasCondicoes_SEM_COMORBIDADE', 'outrasCondicoes_INFLUENZA', 'outrosSintomas_DORES', 'outrosSintomas_ABDOMINAL', 'outrosSintomas_DESCONFORTO', 'outrasCondicoes_TAB', 'outrasCondicoes_comorbidades', 'outrasCondicoes_HIPOT', 'outrasCondicoes_SEM_COMORBIDADES', 'outrosSintomas_CONGESTAO', 'outrosSintomas_COSTAS', 'outrasCondicoes_sem_comorbidade', 'outrasCondicoes_sem_comorbidades', 'outrasCondicoes_Hipertensão', 'outrasCondicoes_TIREOIDISMO', 'outrosSintomas_MAL', 'outrosSintomas_ARTRALGIA', 'outrosSintomas_PEITO', 'outrasCondicoes_RINITE', 'outrosSintomas_MAL_ESTAR', 'outrasCondicoes_HIPOTIREOIDISMO', 'outrosSintomas_CEFALEIA', 'outrasCondicoes_SINUSITE', 'outrasCondicoes_Não', 'outrosSintomas_FALTA_DE_', 'outrasCondicoes_IPERTENSO', 'outrasCondicoes_HIPERTENSO', 'outrasCondicoes_TABAGISTA', 'outrosSintomas_NOS_OLHOS', 'outrosSintomas_Mialgia,', 'outrasCondicoes_PRESSÃO', 'outrosSintomas_DESCONFORTO_RESPIRATORIO', 'outrosSintomas_TONTURA', 'outrasCondicoes_NAO', 'outrosSintomas_DOR_NO_PEITO', 'outrasCondicoes_ANSIEDADE', 'outrosSintomas_CONTATO', 'outrosSintomas__Mialgia', 'outrasCondicoes_ALGIA', 'outrosSintomas__CANSAÇO', 'outrasCondicoes_asma', 'outrosSintomas_OUVIDO', 'outrosSintomas_ADINAMIA', 'outrasCondicoes_ELA', 'outrosSintomas_FALTA_DE_AR', 'outrosSintomas_SINTOMAS', 'outrasCondicoes_MIALGIA', 'outrosSintomas__CONGESTÃO_NASAL', 'outrasCondicoes_Hipertensão_', 'outrasCondicoes_PRÉ-OPERATÓRIO', 'outrosSintomas_PRÉ-OPERATÓRIO', 'outrosSintomas_DINOFAGIA', 'outrosSintomas_ODINOFAGIA', 'outrasCondicoes_HIPERTENSÃO_', 'outrasCondicoes_hipertensão', 'outrasCondicoes_HAS,', 'outrasCondicoes_EPILEPSIA', 'outrosSintomas_ND', 'outrosSintomas_SATURAÇÃO', 'outrosSintomas__ASTENIA', 'outrasCondicoes_TABAGISMO', 'outrosSintomas_DOR_NOS_OLHOS', 'outrosSintomas_;']
frequencia_sintomas = dados_dash_2020_2024.groupby('diagnosticoCOVID')[sintomas_cols].mean()

# Remover a coluna 'diagnosticoCOVID' antes de resetar o índice
frequencia_sintomas = frequencia_sintomas.drop(columns=['diagnosticoCOVID'], errors='ignore').reset_index()

# Converter para formato longo
frequencia_sintomas_long = frequencia_sintomas.melt(id_vars='diagnosticoCOVID', var_name='Sintoma', value_name='Frequência')

# Normalizar para porcentagem
frequencia_sintomas_long['Frequência'] *= 100

N = 10  # Número de sintomas a serem exibidos por grupo
top_sintomas = frequencia_sintomas_long.groupby('diagnosticoCOVID').apply(lambda x: x.nlargest(N, 'Frequência')).reset_index(drop=True)

# Mapear os valores de diagnóstico para legendas claras
top_sintomas['diagnosticoCOVID'] = top_sintomas['diagnosticoCOVID'].map({0: 'Covid negativo', 1: 'COVID Positivo'})

# Ordenar os sintomas por frequência em ordem decrescente
top_sintomas = top_sintomas.sort_values(by='Frequência', ascending=False)

# Criar gráfico de barras
dist_sintomas = px.bar(top_sintomas, x='Sintoma', y='Frequência', color='diagnosticoCOVID',
             barmode='group',
             title="Frequência de Sintomas por Diagnóstico de COVID",
             labels={'diagnosticoCOVID': 'Diagnóstico', 'Frequência': 'Porcentagem de Sintomas'})

dist_sintomas.update_layout(xaxis_title='Sintoma', yaxis_title='Porcentagem de Sintomas', xaxis_tickangle=-45)

# Gráfico de distribuição de Casos por Estado
dist_estado = px.histogram(dados_dash_2020_2024, x='estado', title="Distribuição de Casos por Estado",
                           labels={'estado': 'Estado', 'count': 'Número de Casos'},
                           color_discrete_sequence=['blue'])
dist_estado.update_layout(xaxis_title='Estado', yaxis_title='Número de Casos', xaxis_tickangle=-45)

# Gráfico de distribuição de Casos por Sexo
dist_sexo = px.histogram(dados_dash_2020_2024, x='sexo', title="Distribuição de Casos por Sexo",
                         labels={'sexo': 'Sexo', 'count': 'Número de Casos'},
                         color_discrete_sequence=['green'])
dist_sexo.update_layout(xaxis_title='Sexo', yaxis_title='Número de Casos')

# Gráfico de distribuição de Casos por Faixa Etária
faixa_etaria_bins = [0, 18, 30, 40, 50, 60, 70, 80, 90, 100]
faixa_etaria_labels = ['0-18', '19-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
dados_dash_2020_2024['faixa_etaria'] = pd.cut(dados_dash_2020_2024['idade'], bins=faixa_etaria_bins, labels=faixa_etaria_labels, right=False)

# Ordenar a coluna faixa_etaria
dados_dash_2020_2024 = dados_dash_2020_2024.sort_values(by='faixa_etaria')

dist_faixa_etaria = px.histogram(dados_dash_2020_2024, x='faixa_etaria', title="Distribuição de Casos por Faixa Etária",
                                 labels={'faixa_etaria': 'Faixa Etária', 'count': 'Número de Casos'},
                                 category_orders={'faixa_etaria': faixa_etaria_labels},
                                 color_discrete_sequence=['purple'])
dist_faixa_etaria.update_layout(xaxis_title='Faixa Etária', yaxis_title='Número de Casos')

def render_dashboard_content():
    """
    Function to render the Dashboard content.
    """
    return html.Div([
        html.H3("Dashboard de Dados", style={'color': '#1e90ff', 'font-family': 'Arial, sans-serif'}),
        html.Div([
            dcc.Graph(figure=dist_estado, style={'grid-column': '1 / 2'}),
            dcc.Graph(figure=dist_sexo, style={'grid-column': '2 / 3'}),
            dcc.Graph(figure=dist_faixa_etaria, style={'grid-column': '1 / 3'}),
            dcc.Graph(figure=dist_idade, style={'grid-column': '1 / 2'}),
            dcc.Graph(figure=dist_Clas_final, style={'grid-column': '2 / 3'}),
            dcc.Graph(figure=dist_sintomas, style={'grid-column': '1 / 3'})
        ], style={
            'display': 'grid',
            'grid-template-columns': '1fr 1fr',
            'gap': '20px'
        })
    ], style={'border-radius': '10px', 'background-color': 'white', 'padding': '20px'})