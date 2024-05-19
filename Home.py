import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações iniciais
st.set_page_config(
    page_title="Analisador de Vendas",
    page_icon="📊",
    layout="wide"
)

# Barra lateral
st.sidebar.markdown('Desenvolvido por [Bruno Almeida](https://www.linkedin.com/in/brunodesouzaalmeida/)')
st.sidebar.header('Opções')

# Carregar dados
def carregar_dados():
    uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.session_state['data'] = data
        st.success("Dados carregados com sucesso!")
    else:
        st.info("Por favor, faça o upload de um arquivo CSV.")
    return st.session_state.get('data')

# Visualização de dados
def visualizar_dados(data):
    st.markdown("## Visualização de Dados")
    st.dataframe(data)
    st.markdown("### Estatísticas Descritivas")
    st.write(data.describe())

# Gráficos
def gerar_graficos(data):
    st.markdown("## Gráficos Interativos")
    fig1 = px.histogram(data, x='vendas', nbins=50, title='Distribuição de Vendas')
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.box(data, y='vendas', title='Boxplot das Vendas')
    st.plotly_chart(fig2, use_container_width=True)

# Título principal
st.markdown('# Bem-vindo ao Analisador de Vendas')

# Divisor
st.divider()

# Introdução
st.markdown(
    '''
    Esse projeto foi desenvolvido como projeto final do curso ***Python para Usuários de Excel***.

    Utilizaremos três principais bibliotecas para o seu desenvolvimento:

    - `pandas`: para manipulação de dados em tabelas
    - `plotly`: para geração de gráficos
    - `streamlit`: para criação desse webApp interativo que você se encontra nesse momento

    Os dados utilizados foram gerados pelo script 'gerador_de_vendas.py' que se encontra junto do código fonte do projeto. Os dados podem ser visualizados na aba de tabelas!
    '''
)

# Divisor
st.divider()

# Carregar dados
data = carregar_dados()

# Se os dados foram carregados, exibir visualização e gráficos
if data is not None:
    visualizar_dados(data)
    gerar_graficos(data)
