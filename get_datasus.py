import requests
import os

from sphinx.util import url_re

estados = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN",
    "RS", "SC", "SE", "TO", "RR"
]


import requests
import concurrent.futures

def download_file(estado, ano):
    print(f'Start: {estado}-{ano}')
    if ano == 2024:
        url = f'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SGL/2023/uf={estado}/lote=1/part-00000-825092a3-a4f8-4c27-ac1a-884d2beef656.c000.csv'
    elif ano == 2023:
        url = f'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SGL/2023/uf={estado}/lote=1/part-00000-ff9728e1-65ff-475f-836d-ce04aea93a4f.c000.csv'
    elif ano == 2022:
        url = f'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SGL/2022/uf={estado}/lote=1/part-00000-ff23f197-0c47-41b5-85d8-cb639fd1b961.c000.csv'
    elif ano == 2021:
        url = f'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SGL/2021/uf={estado}/lote=1/part-00000-2b201470-294e-4e36-9081-66206e30b61f.c000.csv'
    elif ano==  2020:
        url = f'https://s3.sa-east-1.amazonaws.com/ckan.saude.gov.br/SGL/2020/uf={estado}/lote=1/part-00000-88c624d4-1d68-4120-abe3-57f21bbfa4b0.c000.csv'
    nome_arquivo = f"./datasus/{estado}-{ano}.csv"

    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(nome_arquivo, 'wb') as f:
            for chunk in response.iter_content(1024):
                if chunk:
                    f.write(chunk)
        print(f"Arquivo baixado com sucesso: {nome_arquivo}")
    else:
        print(f"Falha ao baixar o arquivo. status: {response.status_code}, URL= {url}")

    print("Finalizado")

def get_dataset_multithreaded(UF, ano, max_workers=5):
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(download_file, estado, ano) for estado in UF]
        concurrent.futures.wait(futures)


get_dataset_multithreaded(estados, 2023, 20)
