import pandas as pd
import numpy as np

dataset = "Brasil-2024-processado_IA.csv"
df = pd.read_csv(dataset)
original_columns = df.columns.to_list()

merge_dict = {
    # --------------------- SINTOMAS ---------------------
    "dor_corpo": [
        'outrosSintomas_DOR_NO_CORPO', 'outrosSintomas_CORPO', 'outrosSintomas_corpo'
    ],
    "dor_costas": ['outrosSintomas_DOR_NAS_COSTAS', 'outrosSintomas_COSTAS'],
    "dor_abdomen": ['outrosSintomas_DOR_ABDOMINAL', 'outrosSintomas_ABDOMINAL'],
    "dor_toracica": ['outrosSintomas_DOR_TORACICA'],
    "dor_peito": ['outrosSintomas_DOR_NO_PEITO', 'outrosSintomas_PEITO'],
    "dor_olhos": ['outrosSintomas_DOR_NOs_OLHOS', 'outrosSintomas_DOR_NOS_OLHOS'],
    "dor_geral": ['outrosSintomas_DOR', 'outrosSintomas_Dor', 'outrosSintomas_dor', 'outrosSintomas_DORES'],

    "mialgia": ['outrosSintomas_MIALGIA', 'outrosSintomas__Mialgia', 'outrosSintomas_Mialgia,',
                'outrasCondicoes_MIALGIA'],
    "algia": ['outrosSintomas_ALGIA', 'outrasCondicoes_ALGIA'],

    "fadiga": [
        'outrosSintomas_FRAQUEZA_FADIGA', 'outrosSintomas_CANSAÇO', 'outrosSintomas__CANSAÇO',
        'outrosSintomas_ASTENIA', 'outrosSintomas__ASTENIA', 'outrosSintomas_ADINAMIA'
    ],
    "febre": ['sintomas_Febre'],
    "tosse": ['sintomas_Tosse'],
    "coriza": ['sintomas_Coriza'],

    "congestao_nasal": [
        'outrosSintomas_CONGESTAO_NASAL', 'outrosSintomas__CONGESTÃO_NASAL', 'outrosSintomas_CONGESTAO'
    ],

    "diarreia": ['outrosSintomas_DIARREIA'],
    "nausea": ['outrosSintomas_NAUSEA'],
    "vomito": ['outrosSintomas_VOMITO'],
    "espirros": ['outrosSintomas_ESPIRROS'],

    "olfato_alterado": ['sintomas_Distúrbios_Olfativos'],
    "paladar_alterado": ['sintomas_Distúrbios_Gustativos'],
    "garganta": ['sintomas_Dor_de_Garganta', 'outrosSintomas_DINOFAGIA', 'outrosSintomas_ODINOFAGIA'],
    "dor_de_cabeca": ['sintomas_Dor_de_Cabeça', 'outrosSintomas_CEFALEIA'],

    "falta_de_ar": ['sintomas_Dispneia', 'outrosSintomas_FALTA_DE_AR', 'outrosSintomas_FALTA_DE_'],
    "mal_estar": ['outrosSintomas_MAL', 'outrosSintomas_MAL_ESTAR'],
    "dor_de_ouvido": ['outrosSintomas_OUVIDO'],
    "tontura": ['outrosSintomas_TONTURA'],

    "desconforto_respiratorio": ['outrosSintomas_DESCONFORTO', 'outrosSintomas_DESCONFORTO_RESPIRATORIO'],
    "saturacao_baixa": ['outrosSintomas_SATURAÇÃO'],
    "sintomas_indefinidos": ['outrosSintomas_SINTOMAS'],

    # ------------------- COMORBIDADES -------------------
    "asma": ['outrasCondicoes_ASMA', 'outrasCondicoes_ASM', 'outrasCondicoes_asma'],

    "hipertensao": [
        'outrasCondicoes_HIPERTENSÃO', 'outrasCondicoes_IPERTENSÃO', 'outrasCondicoes_IPERTENSA',
        'outrasCondicoes_HIPERTENSA', 'outrasCondicoes_HIPERTENSAO', 'outrasCondicoes_Hipertensão',
        'outrasCondicoes_Hipertensão_', 'outrasCondicoes_hipertensão', 'outrasCondicoes_HIPERTENSÃO_',
        'outrasCondicoes_HIPERTENSO', 'outrasCondicoes_IPERTENSO', 'outrasCondicoes_HAS',
        'outrasCondicoes_HAS,'
    ],

    "sem_comorbidade": [
        'outrasCondicoes_Sem_Comorbidade', 'outrasCondicoes_SEM_COMORBIDADE',
        'outrasCondicoes_SEM_COMORBIDADES', 'outrasCondicoes_sem_comorbidade',
        'outrasCondicoes_sem_comorbidades'
    ],

    "diabetes": ['condicoes_Diabetes'],
    "bronquite": ['outrasCondicoes_BRONQUITE'],
    "tabagismo": ['outrasCondicoes_TABAGISTA', 'outrasCondicoes_TABAGISMO', 'outrasCondicoes_TAB'],
    "epilepsia": ['outrasCondicoes_EPILEPSIA'],
    "ansiedade": ['outrasCondicoes_ANSIEDADE'],
    "hipotireoidismo": ['outrasCondicoes_HIPOTIREOIDISMO'],
    "tireoidite": ['outrasCondicoes_TIREOIDISMO'],
    "rinite": ['outrasCondicoes_RINITE'],
    "sinusite": ['outrasCondicoes_SINUSITE'],
    "hipotensao": ['outrasCondicoes_HIPOT'],
    "comorbidades_indefinidas": ['outrasCondicoes_comorbidades'],
    "nao_declarado": ['outrasCondicoes_Não', 'outrasCondicoes_NAO','outrosSintomas_ND'],
    "pre_operatorio": ['outrasCondicoes_PRÉ-OPERATÓRIO', 'outrosSintomas_PRÉ-OPERATÓRIO'],
    "Esclerose Lateral Amiotrófica": ['outrasCondicoes_ELA'],

    # ----------------- INFORMAÇÕES ADICIONAIS -----------------
    "tomouPrimeiraDose": ['tomouPrimeiraDose'],
    "tomouSegundaDose": ['tomouSegundaDose'],
    "diagnosticoCOVID": ['diagnosticoCOVID', 'DiagnosticoCOVID'],
}

def unificar_e_limpar(df, merge_dict):
    novo_df = pd.DataFrame(index=df.index)

    for nova_coluna, colunas_agrupadas in merge_dict.items():
        colunas_existentes = [col for col in colunas_agrupadas if col in df.columns]
        if colunas_existentes:
            novo_df[nova_coluna] = df[colunas_existentes].max(axis=1)

    return novo_df

df_limpo = unificar_e_limpar(df, merge_dict)

print("Colunas finais:", df_limpo.columns.tolist())
print("Quantidade de linhas:", len(df_limpo))
print("Quantidade de colunas:", len(df_limpo.columns))

# Salvar o DataFrame limpo em um novo arquivo CSV
df_limpo.to_csv(dataset, index=False)