# aquecimento
Link das instruções: https://github.com/prefeitura-rio/aquecimento-formacao-infra

Arquivos gerados:
tabela.csv
tabela_formatada.csv
resultado.txt
resultado_agrupados.txt
histograma.pdf


FUNÇÕES PRINCIPAIS:

def coletando_dados(qtd=None):<br/>
==>obtêm os dados da API

def to_DataFrame(dados: "json") -> pd.DataFrame:<br/>
==>transforma json recebido em dataframe normalizado

def save_DataFrame_CSV(dataframe,file_name):<br/>
==>salva dataframe como CSV

def formatar_dataframe(dados: pd.DataFrame, col: str) -> pd.DataFrame:<br/>
==>formata coluna (Col) para somente números (aplicado em telefones

def calcular_porc(dados: pd.DataFrame, col: str, valor: str) -> float:<br/>
==>calcula porcentagem

def group(dados: pd.DataFrame, campos: list, manter_campos=True) -> pd.DataFrame:<br/>
==>agrupa dataframe nos campos passados (obs.: precisa alterar para manter os outros campos da tabela)

def save_grafico_pdf(dados: pd.DataFrame, campos: list, arquivo = "histograma.pdf"):<br/>
==>salva o resultado em gráfico histograma como PDF
