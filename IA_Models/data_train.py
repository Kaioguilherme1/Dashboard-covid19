import os, sys

# Adiciona a referencia da pasta IA_Models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Carregar o dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

Sintomas = pd.read_csv('datasets/Brasil-2020-2024-processado_IA.csv')
# dataset_limpo = pd.read_csv('datasets/Brasil-2022-limpo.csv')
data_2020 = pd.read_csv('datasets/Brasil-2020-limpo.csv')
data_2021 = pd.read_csv('datasets/Brasil-2021-limpo.csv')
data_2022 = pd.read_csv('datasets/Brasil-2022-limpo.csv')
data_2023 = pd.read_csv('datasets/Brasil-2023-limpo.csv')
data_2024 = pd.read_csv('datasets/Brasil-2024-limpo.csv')
# # # Concatena os datasets em um único DataFrame
dataset_limpo = pd.concat([data_2020, data_2021, data_2022, data_2023, data_2024], ignore_index=True)

# seleciona somente as colunas de idade e sexo do dataset_limpo
dados = dataset_limpo[['idade', 'sexo']]
# adiciona as colunas do dataset Sintomas
dados_final = pd.concat([dados, Sintomas], axis=1)

print(f'Dataset IA shape: {dados_final.shape}')
# print(f'Colunas: {dados_final.columns.tolist} ')

# Divide os dados De treino
# print(f"Dataset Final shape: {dados_final.shape}")
# print(dados_final.head())


# Codificar "sexo" para valores numéricos com LabelEncoder
if 'sexo' in dados.columns:
   label_encoder = LabelEncoder()
   dados_final['sexo'] = label_encoder.fit_transform(dados_final['sexo'])

# remove colunas que não tem correlação com o diagnosticoCOVID

dados_final = dados_final.drop(columns=['dor_toracica', 'diarreia', 'nausea', 'vomito', 'espirros'])

# Separar variáveis independentes (Features) e a variável alvo (Label)
Features = dados_final.drop(columns=['diagnosticoCOVID'])  # Remove a variável alvo das Features
Label = dados_final['diagnosticoCOVID']


# # mostra corr entre as variáveis com o diagnosticoCOVID[
# print(dados_final.corr()['diagnosticoCOVID'].sort_values(ascending=False))

# Dividir os dados em treino (80%) e teste (20%)
X_train, X_test, y_train, y_test = train_test_split(Features, Label, test_size=0.25, random_state=42)

print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
print(f"y_train shape: {y_train.shape}, y_test shape: {y_test.shape}")
# Mostra uma lista com todas as colunas selecionadas
