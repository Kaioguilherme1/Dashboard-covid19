import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('../Brasil-2020-2024-processado.csv')

# Criar a lista para armazenar as colunas binárias e suas contagens de '1'
binary_columns = {}

# Identificar colunas binárias e contar os valores '1'
for col in df.columns:
    # Verificar se a coluna é binária (contém apenas dois valores distintos)
    if df[col].dropna().nunique() == 2:
        # Contar o número de vezes que aparece o valor 1
        count_ones = (df[col] == 1).sum()
        binary_columns[col] = count_ones

# Converter para um DataFrame
binary_df = pd.DataFrame(list(binary_columns.items()), columns=['Column', 'Count_1'])

# Ordenar do maior para o menor
binary_df = binary_df.sort_values(by='Count_1', ascending=False)

# Selecionar as primeiras 200 colunas
binary_top_200 = binary_df.head(200)

# Exportar para CSV
binary_top_200.to_csv('binary_columns_top_200.csv', index=False)

print("Arquivo CSV com as 200 colunas binárias principais criado: binary_columns_top_200.csv")