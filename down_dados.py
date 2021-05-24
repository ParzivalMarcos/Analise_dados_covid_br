'''Realiza o download dos dados de covid fornecidos pelo Ministerio da Saude em Formato CSV'''
import wget
import os.path

url = 'https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/2172b7456059f9ce8b2634842d1c96bd_HIST_PAINEL_COVIDBR_22mai2021.csv'
nome_arquivo = 'dados_covid.csv'

try:
    if os.path.exists(nome_arquivo):
        os.remove(nome_arquivo)
        arquivo = wget.download(url, out=nome_arquivo)
    else:
        arquivo = wget.download(url, out=nome_arquivo)
except Exception as e:
    print('Erro ao realizar Download')
