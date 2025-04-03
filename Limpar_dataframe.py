import pandas as pd

def limpar_datasets(dataset_path):
    print(f"Iniciando limpeza: {dataset_path}")
    dataframe = pd.read_csv(dataset_path, low_memory=False)
    # drop colunas desnessesarias
    columns_drop = [
        "cbo", "estadoIBGE", "municipioIBGE", "estadoNotificacaoIBGE",
        "municipioNotificacaoIBGE", "codigoEstrategiaCovid",
        "codigoBuscaAtivaAssintomatico", "outroBuscaAtivaAssintomatico",
        "codigoTriagemPopulacaoEspecifica", "outroTriagemPopulacaoEspecifica",
        "codigoLocalRealizacaoTestagem", "outroLocalRealizacaoTestagem",
        "codigoContemComunidadeTradicional", "source_id", "excluido", "validado",
        "codigoLaboratorioPrimeiraDose", "codigoLaboratorioSegundaDose",
        "lotePrimeiraDose", "loteSegundaDose", "codigoDosesVacina",
        "codigoEstadoTeste1", "codigoTipoTeste1", "codigoFabricanteTeste1",
        "codigoResultadoTeste1", "codigoEstadoTeste2", "codigoTipoTeste2",
        "codigoFabricanteTeste2", "codigoResultadoTeste2", "codigoEstadoTeste3",
        "codigoTipoTeste3", "codigoFabricanteTeste3", "codigoResultadoTeste3",
        "codigoEstadoTeste4", "codigoTipoTeste4", "codigoFabricanteTeste4",
        "codigoResultadoTeste4", "dataColetaTeste1", "dataColetaTeste2",
        "dataColetaTeste3", "dataColetaTeste4", "origem", "codigoRecebeuVacina","dataPrimeiraDose","dataSegundaDose"
    ]

    # Cria as colunas booleanas baseado nas datas
    dataframe['tomouPrimeiraDose'] = dataframe['dataPrimeiraDose'].apply(lambda x: True if not pd.isna(x) else False)
    dataframe['tomouSegundaDose'] = dataframe['dataSegundaDose'].apply(lambda x: True if not pd.isna(x) else False)
    print("deletando colunas...")
    dataframe = dataframe.drop(columns=columns_drop)
    #limpa valores nulos
    dataframe = dataframe.dropna()
    print("Convertendo Datas...")
    #converte as datas para timestemp
    colunas_data = [
        "dataNotificacao", "dataInicioSintomas", "dataEncerramento",
    ]
    dataframe[colunas_data] = dataframe[colunas_data].apply(pd.to_datetime)
    print("Finalizado")
    return dataframe



dataframe_limpo = limpar_datasets("./datasets/Brasil-2020-bruto.csv")
dataframe_limpo.to_csv("./datasets/Brasil-2020-limpo.csv",index=False)
dataframe_limpo = limpar_datasets("./datasets/Brasil-2021-bruto.csv")
dataframe_limpo.to_csv("./datasets/Brasil-2021-limpo.csv",index=False)
dataframe_limpo = limpar_datasets("./datasets/Brasil-2022-bruto.csv")
dataframe_limpo.to_csv("./datasets/Brasil-2022-limpo.csv",index=False)
dataframe_limpo = limpar_datasets("./datasets/Brasil-2023-bruto.csv")
dataframe_limpo.to_csv("./datasets/Brasil-2023-limpo.csv",index=False)
dataframe_limpo = limpar_datasets("./datasets/Brasil-2024-bruto.csv")
dataframe_limpo.to_csv("./datasets/Brasil-2024-limpo.csv",index=False)
