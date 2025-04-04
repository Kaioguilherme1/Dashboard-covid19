import os, sys

# Adiciona a referencia da pasta IA_Models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Carregar o dataset
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

Sintomas = pd.read_csv('datasets/Brasil-2021-processado_IA.csv')
dataset_limpo = pd.read_csv('datasets/Brasil-2021-limpo.csv')
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

# Separar variáveis independentes (Features) e a variável alvo (Label)
Features = dados_final.drop(columns=['diagnosticoCOVID'])  # Remove a variável alvo das Features
Label = dados_final['diagnosticoCOVID']

# Dividir os dados em treino (80%) e teste (20%)
X_train, X_test, y_train, y_test = train_test_split(Features, Label, test_size=0.25, random_state=42)

# print(f"X_train shape: {X_train.shape}, X_test shape: {X_test.shape}")
# print(f"y_train shape: {y_train.shape}, y_test shape: {y_test.shape}")
# Mostra uma lista com todas as colunas selecionadas
