
import requests
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt

import seaborn as sns
import seaborn.objects as so

url_default="https://randomuser.me/api/"
qtd_default=600

def colunas_to_list(dados: pd.DataFrame) -> list:
    return dados.columns.tolist()

def remove_colunas(colunas1: list, colunas2: list) -> list:
    for item in colunas2:
        if item in colunas1:
            colunas1.remove(item)
    return colunas1

def coletando_dados(qtd=None):
    return requests.get(url if not qtd else url+"?results="+str(qtd))

def to_DataFrame(dados: "json") -> pd.DataFrame:
    return pd.json_normalize(dados)

def save_DataFrame_CSV(dataframe,file_name):
    dataframe.to_csv(file_name)

def formatar_numeros(numero: str) -> str:
    return ''.join(filter(str.isdigit, numero))

def formatar_dataframe(dados: pd.DataFrame, col: str) -> pd.DataFrame:
    dados_formatado = dados.copy()
    dados_formatado[col] = dados_formatado[col].apply(formatar_numeros)
    return dados_formatado

def calcular_porc(dados: pd.DataFrame, col: str, valor: str) -> float:
    # retorna a % de itens iguais a "valor" de uma coluna do Dataframe
    total_de_linhas = len(dados)
    qtd = (dados[col] == valor).sum()
    return round(qtd/total_de_linhas, 2)*100


def qtd_por_coluna(dados: pd.DataFrame, col: str) -> int:
    # retorna a qtd de itens diferentes em uma coluna
    # normalize=True indica que o resultado será em relação ao total
    return dados[col].value_counts(normalize=True) 

def group(dados: pd.DataFrame, campos: list, manter_campos=True) -> pd.DataFrame:
    agr = dados.groupby(campos)
    if manter_campos:
        pass # não descobri como manter os outros campos.
    return agr

def save_dados_string(dados_string: str, arquivo="resultado.txt"):
    with open(arquivo, 'w') as f:
        f.write(dados_string)
    f.close()


def save_grafico_pdf(dados: pd.DataFrame, campos: list, arquivo = "histograma.pdf"):    
    sns.histplot(dados[campos])
    plt.savefig(arquivo)


def etapa_1(qtd):
    return coletando_dados(qtd)

def etapa_2(dados):
    dados=resposta.json()["results"]
    dados = to_DataFrame(dados)
    save_DataFrame_CSV(dados,"tabela.csv")
    return dados

def etapa_3(dados):
    dados=formatar_dataframe(dados,"phone")
    dados=formatar_dataframe(dados,"cell")
    save_DataFrame_CSV(dados,"tabela_formatada.csv")
    return dados

def etapa_4(dados: pd.DataFrame):
    porc_male = calcular_porc(dados, "gender","male")
    porc_female = calcular_porc(dados, "gender","female")
    list_porc_por_pais = qtd_por_coluna(dados,"location.country")*100
    resultado = """ Segue o relatório
    Porcentagem masculina: {} %
    Porcentagem feminina: {} %
    Porcentagem por país (%):
{}"""
    resultado = resultado.format(porc_male,porc_female,list_porc_por_pais)
    print("resultado", resultado)
    save_dados_string(resultado,"resultado.txt")
    save_grafico_pdf(dados,"dob.age")

def etapa_5(dados,campos):
    dados_agrupados=group(dados,campos)
    print(dados_agrupados.mean())
    resultado = """ Segue o agrupamento
{}"""
    resultado = resultado.format(dados_agrupados.mean())
    save_dados_string(resultado,"resultado_agrupados.txt")

print()
print("Digite abaixo as informações desejadas:")
url=input("URL (https://")
url = url if url else url_default

qtd=input("Quantidade de amostragem (600): ")
qtd = qtd if qtd else qtd_default

campos =input("Quais campos deseja agregar? (Cidade, Estado): ")
campos = campos.strip(" ").split(",") if campos else ["location.country","location.state"]

print()

print("Segue o resultado abaixo e os arquivos gerados:")
print("===============================================")
print()

resposta = etapa_1(qtd)
dados = etapa_2(resposta)
dados = etapa_3(dados)
etapa_4(dados)
etapa_5(dados,campos)

### tentativa de obter a tabela toda agrupada porém mantendo todas as colunas
### não achei nada do Pandas que fizesse isso automaticamente. Não tive tempo de achar.
### os códigos abaixo nao estão funcionando adequadamente.
#import pdb; pdb.set_trace()

def group2(dados: pd.DataFrame, campos: list, colunas: list, manter_campos=True) -> pd.DataFrame:
    agr = dados.groupby(campos)
    if not manter_campos:
        colunas = remove_colunas(colunas_to_list(dados),campos)
    return agr[colunas].agg(list).reset_index()

colunas=remove_colunas(colunas_to_list(dados),["location.country","location.state"])

dados_agrupados = group2(dados, ["location.country", "location.state"], ["gender","picture.thumbnail"])
dados_agrupados = group2(dados, ["location.country", "location.state"], colunas)

