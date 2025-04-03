import pandas as pd
import os

estados = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "SC", "SE", "TO", "RR"
]

def compilar_df(estados: list, ano: int ):

    # Lista para armazenar os DataFrames
    dataframes = []

    # Loop sobre os arquivos
    for arquivo in estados:
        caminho_arquivo = f'./datasus/{arquivo}-{ano}.csv'

        # Verifica se o arquivo existe
        if os.path.exists(caminho_arquivo):
            print(f"Lendo arquivo: {caminho_arquivo}")

            # Tenta ler o arquivo CSV
            try:
                df = pd.read_csv(caminho_arquivo, engine="python", sep=";", on_bad_lines="skip")
                dataframes.append(df)  # Adiciona o DataFrame à lista
            except Exception as e:
                print(f"Erro ao ler {caminho_arquivo}: {e}")
        else:
            print(f"Arquivo não encontrado: {caminho_arquivo}")

    # Verifica se a lista de DataFrames não está vazia
    if dataframes:
        # Concatena todos os DataFrames em um único
        df_final = pd.concat(dataframes, ignore_index=True)
        print("Arquivos lidos com sucesso!")
    else:
        print("Nenhum arquivo foi lido.")

    df_final.to_csv(f"./datasets/Brasil-{ano}-bruto.csv", index=False)
    print("finalizado")

compilar_df(estados, 2022)
compilar_df(estados, 2023)
