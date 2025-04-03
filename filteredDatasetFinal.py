import pandas as pd

# **Passo 1**: Carregar o arquivo com as 200 colunas mais relevantes
binary_columns_file = 'binary_columns_top_200.csv'
binary_columns_df = pd.read_csv(binary_columns_file)

top_200_columns = binary_columns_df['Column'].tolist()

# **Passo 2**: Carregar o dataset principal
data = pd.read_csv('../Brasil-2020-2024-processado.csv')

# **Passo 3**: Definir os grupos de colunas semelhantes
column_groups = {
    "outrosSintomas_DOR_NO_CORPO": [
        "outrosSintomas_DOR_NO_CORPO", "outrosSintomas_DOR_NO_CORPO,", "outrosSintomas_dor_no_corpo", "outrosSintomas_Dor_no_corpo"
    ],
    "outrosSintomas_DOR_NAS_COSTAS": [
        "outrosSintomas_DOR_NAS_COSTAS", "outrosSintomas_DOR_NAS_COSTA", "outrosSintomas_NAS_COSTAS"
    ],
    "outrosSintomas_DOR_ABDOMINAL": [
        "outrosSintomas_DOR_ABD", "outrosSintomas_DOR_ABDOMINAL"
    ],
    "outrosSintomas_DOR_TORACICA": [
        "outrosSintomas_DOR_TORACIC", "outrosSintomas_DOR_TORACICA"
    ],
    "outrosSintomas_MIALGIA": [
        "outrosSintomas_MIALGI", "outrosSintomas_MIALGIA", "outrosSintomas__MIALGIA", "outrosSintomas_mialgia",
        "outrosSintomas_Mialgia", "outrosSintomas_MIALGIA_", "outrosSintomas_MIALGIA,", "outrosSintomas_mialgia,"
    ],
    "outrosSintomas_ALGIA": [
        "outrosSintomas_ALGIA", "outrosSintomas_algia", "outrosSintomas_ALGIA,"
    ],
    "outrosSintomas_CALAFRIOS": [
        "outrosSintomas_CALAFRIO", "outrosSintomas_CALAFRIOS", "outrosSintomas__CALAFRIOS", "outrosSintomas_CALAFRIOS,"
    ],
    "outrosSintomas_CONGESTAO_NASAL": [
        "outrosSintomas_CONGESTÃO_NASA", "outrosSintomas_CONGESTÃO_NASAL", "outrosSintomas_CONGESTÃO_", "outrosSintomas_CONGESTÃO",
        "outrosSintomas_CONGESTAO_NASAL", "outrosSintomas_congestão_nasal", "outrosSintomas_congestão"
    ],
    "outrosSintomas_DIARREIA": [
        "outrosSintomas_DIARREIA", "outrosSintomas_DIARREIA,", "outrosSintomas_DIARREIA_", "outrosSintomas__DIARREIA",
        "outrosSintomas_diarreia", "outrosSintomas_Diarreia", "outrosSintomas_DIARRÉI", "outrosSintomas_DIARRÉIA"
    ],
    "outrosSintomas_NAUSEA": [
        "outrosSintomas_NAUSE", "outrosSintomas_NAUSEA", "outrosSintomas__NAUSEA", "outrosSintomas_NAUSEAS"
    ],
    "outrosSintomas_VOMITO": [
        "outrosSintomas_VOMITO", "outrosSintomas_VÔMITO", "outrosSintomas_VOMITOS", "outrosSintomas_vomito", "outrosSintomas_VOMITO,"
    ],
    "outrosSintomas_ESPIRROS": [
        "outrosSintomas_ESPIRRO", "outrosSintomas_ESPIRROS", "outrosSintomas_ESPIRROS,", "outrosSintomas__ESPIRROS", "outrosSintomas_espirro"
    ],
    "outrosSintomas_FRAQUEZA_FADIGA": [
        "outrosSintomas_FRAQUEZA", "outrosSintomas_FRAQUEZA,", "outrosSintomas__FRAQUEZA", "outrosSintomas_FADIGA", "outrosSintomas__FADIGA"
    ],
    "outrosSintomas_DOR_NOs_OLHOS": [
        "outrosSintomas_OLHO", "outrosSintomas_OLHOS",
    ]
}

# **Passo 4**: Criar colunas agrupadas
for group_name, columns in column_groups.items():
    existing_cols = [col for col in columns if col in data.columns]
    if existing_cols:
        data[group_name] = data[existing_cols].sum(axis=1)
        data.drop(columns=existing_cols, inplace=True)  # Remover as colunas que foram agrupadas

# **Passo 5**: Criar colunas ausentes com valor 0
desired_columns = list(column_groups.keys()) + [col for col in top_200_columns if
                                                col not in sum(column_groups.values(), [])]

# Certifique-se de que apenas as colunas desejadas que não existem no dataset atual sejam criadas
for col in desired_columns:
    if col not in data.columns:
        data[col] = 0


# **Passo 6**: Filtrar apenas as colunas finais
data = data[desired_columns]

# **Passo 7**: Salvar o resultado em um novo arquivo CSV
output_file = 'datasets/Brasil-2020-2024-processado_IA.csv'
data.to_csv(output_file, index=False)

# Exibir informações no terminal
print(f"Número total de colunas após agrupamento: {len(desired_columns)}")
print("As colunas finais consideradas no dataset são:")
print(desired_columns)
