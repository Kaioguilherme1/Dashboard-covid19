import pandas as pd

# Carrega os datasets
brasil_2020 = pd.read_csv('datasets/Brasil-2020-limpo.csv')
brasil_2021 = pd.read_csv('datasets/Brasil-2021-limpo.csv')
brasil_2022 = pd.read_csv('datasets/Brasil-2022-limpo.csv')
brasil_2023 = pd.read_csv('datasets/Brasil-2023-limpo.csv')
brasil_2024 = pd.read_csv('datasets/Brasil-2024-limpo.csv')

# Concatena os datasets em um único DataFrame
data = pd.concat([brasil_2020, brasil_2021, brasil_2022, brasil_2023, brasil_2024], ignore_index=True)
# data = brasil_2024

# Remove linhas completamente nulas no DataFrame
data = data.dropna(how='all').reset_index(drop=True)

# 1. Categoriza pessoas com e sem diagnóstico de COVID
data['diagnosticoCOVID'] = data['classificacaoFinal'].isin([
    'Confirmado Laboratorial',
    'Confirmado Clínico',
    'Confirmado Clínico-Epidemiológico',
    'Confirmado Clínico-Imagem']).astype(int)

# 2. Mapeamento de dados de evolução
mapeamento_evolucao = {
    'Cura': 0,
    'Em tratamento domiciliar': 1,
    'Internado': 2,
    'Internado em UTI': 3,
    'Óbito': 4,
    'Ignorado': -1,
    'Cancelado': -2
}
data['evolucaoCaso'] = data['evolucaoCaso'].map(mapeamento_evolucao)

# 3. Mapeamento de valores dos profissionais da segurança
data['profissionalSeguranca'] = data['profissionalSeguranca'].map({
    'Sim': 1,
    'Não': 0,
    'Não Informado': -1
})


# Função para aplicar sistema de frequências em colunas com listas (separadas por vírgulas)
def processar_coluna_binaria_listas(data, coluna, top_percent):
    """
    Transforma valores de uma coluna que contém listas (em strings separadas por vírgulas)
    em colunas binárias. Considera apenas os valores mais frequentes com base no top_percent.

    Retorna um DataFrame com as colunas binárias para serem concatenadas após o processamento.
    """
    if coluna in data.columns:
        print(f'Processando coluna "{coluna}" com {int(top_percent * 100)}% dos valores mais frequentes...')
        try:
            # Separar os valores únicos da "lista" representada por string
            separados = data[coluna].str.split(', ', expand=True).stack().reset_index(drop=True)

            # Contar a frequência de cada valor
            frequencias = separados.value_counts()

            # Selecionar os valores mais frequentes com base no top_percent
            limite_top = int(len(frequencias) * top_percent)  # Exemplo: 0.5 para os 50% mais frequentes
            mais_frequentes = frequencias.iloc[:limite_top].index

            # Criar um DataFrame temporário para armazenar as colunas binárias
            colunas_binarias = pd.DataFrame(index=data.index)  # Garantir que índices correspondam ao DataFrame original

            # Criar uma coluna binária para cada valor nos "mais frequentes"
            for valor in mais_frequentes:
                nome_coluna = f"{coluna}_{valor.replace(' ', '_')}"  # Ex.: `sintomas_Febre`
                colunas_binarias[nome_coluna] = data[coluna].apply(lambda x: 1 if pd.notna(x) and valor in x else 0)

            print(f'{len(mais_frequentes)} valores processados para a coluna "{coluna}".\n')
            return colunas_binarias
        except Exception as e:
            print(f"Erro ao processar a coluna '{coluna}': {e}")
            return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro
    else:
        print(f"Coluna {coluna} não encontrada no DataFrame.")
        return pd.DataFrame()


# 4. Configuração dos percentuais personalizados para cada coluna
percentuais_por_coluna = {
    'sintomas': 1.0,  # 100% dos valores mais frequentes
    'outrosSintomas': 0.5,  # 50% dos valores mais frequentes
    'condicoes': 0.25,  # 25% dos valores mais frequentes
    'outrasCondicoes': 0.25  # 25% dos valores mais frequentes
}

# 5. Criar as colunas binárias para todas as colunas relevantes e concatenar ao final
novas_colunas_binarias = []  # Lista para armazenar os DataFrames das colunas binárias

for coluna, percentual in percentuais_por_coluna.items():
    novas_colunas = processar_coluna_binaria_listas(data, coluna, percentual)
    novas_colunas_binarias.append(novas_colunas)

# 6. Concatenar apenas uma vez as novas colunas binárias ao lado do DataFrame original
# Garantindo que o DataFrame principal seja atualizado com os novos dados
print('Finalizando processamento...')
data = pd.concat([data] + novas_colunas_binarias, axis=1)

# 7. Salvar o novo dataset processado com as colunas binárias
try:
    data.to_csv('datasets/Brasil-2020-2024-processado.csv', index=False)
    print(f"Novo dataset salvo com {data.shape[0]} linhas e {data.shape[1]} colunas.")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV: {e}")