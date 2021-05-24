import pandas as pd
import plotly.express as px
import streamlit as st


# -- Carregamento das informações
@st.cache
def carrega_dados():
    df = pd.read_csv('dados_covid.csv', sep=';')
    return df

@st.cache
def carrega_dados_brasil(df):
    dados_brasil = df[df['estado'].isna()]
    return dados_brasil


@st.cache
def carrega_dados_gerais_brasil(df):
    dados_geral_brasil = (df[df['municipio'].isna()])
    dados_geral_brasil = dados_geral_brasil.groupby('regiao').sum().sort_values('casosAcumulado', ascending=False)
    dados_geral_brasil.drop('Brasil', inplace=True)

    return dados_geral_brasil


# -- Gráficos
def graficos_dados_gerais_brasil(df, indice):
    # -- Ajuste dos dados
    dados_geral_brasil = (df[df['municipio'].isna()])
    dados_geral_brasil = dados_geral_brasil.groupby('regiao').sum().sort_values('casosAcumulado', ascending=False)
    dados_geral_brasil.drop('Brasil', inplace=True)

    grafico_por_regiao = px.bar(
        data_frame=dados_geral_brasil,
        x=dados_geral_brasil.index,
        y=indice,
        title=f'Grafico de  {indice} por região'
    )


    # -- Plot dos gráficos
    st.plotly_chart(grafico_por_regiao)


def grafico_barras(df, titulo, indice):
    return px.bar(data_frame=df, x=df.index, y=indice, title=titulo)


def apresentacao():
    st.title('Analise de dados Covid')
    st.subheader('Projeto realizado para fins de estudo')
    st.write('Dados fornecidos por https://covid.saude.gov.br/')


def finalizcao():
    st.markdown('<br> <br> <br> <br> <br> <br> <br> <br> <br> <br>', unsafe_allow_html=True)
    st.markdown('- Desenvolvido por: Marcos Lima Marinho 🧑🏻‍💻 <br> \
        - Linkedin: https://www.linkedin.com/in/marcos-lima-marinho-878564168/ <br> \
        - GitHub: https://github.com/ParzivalMarcos',
         unsafe_allow_html=True)


@st.cache
def extrai_dados_casos_recuperados(dados):
    recuperados = dados['Recuperadosnovos'].iloc[-1]
    acompanhamento = dados['emAcompanhamentoNovos'].iloc[-1]

    return (int(recuperados), int(acompanhamento))


def carrega_pagina():
    # Carregando  iniciais
    dados = carrega_dados()
    regioes = ['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste']

    apresentacao()
    recuperados, acompanhamento = extrai_dados_casos_recuperados(dados[dados['estado'].isna()])

    col1, col2 = st.beta_columns(2)
    col1.subheader('Casos Recuperados')
    col2.subheader('Casos em Acompanhamento')

    col1.markdown(f'# {recuperados:_}'.replace('_', '.'))
    col2.markdown(f'# {acompanhamento:_}'.replace('_', '.'))


    st.sidebar.header('Opções')
    if st.sidebar.checkbox('Dados Gerais Brasil'):
        df_brasil = carrega_dados_brasil(dados)
        # Tratamento de datas duplicadas
        data_duplicada = df_brasil[df_brasil['data'].duplicated()].index
        df_brasil = df_brasil.drop(data_duplicada)

        titulo = 'Escolha o índice que deseja visualizar:'
        indices_br = ['casosNovos', 'casosAcumulado', 'obitosAcumulado', 'obitosNovos']
        indice_brasil = st.sidebar.selectbox(label=titulo, options=indices_br)
        graficos_dados_gerais_brasil(dados, indice_brasil)


    if st.sidebar.checkbox('Visualizar por Região'):
        titulo = 'Escolha o índice que deseja visualizar:'
        indices = ['casosAcumulado', 'casosNovos', 'obitosAcumulado', 'obitosNovos']
        indice_regiao = st.sidebar.selectbox(label=titulo, options=indices)

        filtro_regiao = st.sidebar.selectbox('Escolha por Região', regioes)
        df_regiao = dados[dados['municipio'].isna() & (dados['regiao'] == filtro_regiao)]
        df_regiao = df_regiao.groupby('estado').sum().sort_values(indice_regiao, ascending=False)
        grafico_casos_acumulados = grafico_barras(df_regiao, f'Dados por estado da região {filtro_regiao}', indice_regiao)
        st.plotly_chart(grafico_casos_acumulados)

        if st.sidebar.checkbox('Visualizar Tabela'):
            st.dataframe(data=df_regiao)


    st.sidebar.info(f'Data dos dados analizados: {dados["data"].iloc[-1]}')
    finalizcao()


carrega_pagina()
