from pathlib import Path
from datetime import date, timedelta

import plotly.express as px
import streamlit as st
import pandas as pd

from utilidades import leitura_de_dados, COMISSAO

# Configurações iniciais
st.set_page_config(
    page_title="Dashboard de Análise",
    page_icon="📊",
    layout="wide"
)

# Dicionário para mapear as chaves de seleção para os nomes das colunas
selecao_keys = {
    'Filial': 'filial',
    'Vendedor': 'vendedor',
    'Produto': 'produto',
    'Forma de Pagamento': 'forma_pagamento',
    'Gênero Cliente': 'cliente_genero',
}

# Dicionário para mapear as opções de agrupamento
agrupamento_keys = {
    'Dia': 'D',
    'Semana': 'W',
    'Mês': 'M',
    'Ano': 'Y'
}

# Carregamento dos dados
leitura_de_dados()

# Obtenção dos dataframes de vendas, filiais e produtos
df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

# Renomeação da coluna 'nome' para 'produto' no dataframe de produtos
df_produtos = df_produtos.rename(columns={'nome': 'produto'})

# Junção dos dataframes de vendas e produtos
df_vendas = df_vendas.reset_index()
df_vendas = pd.merge(left=df_vendas, right=df_produtos[['produto', 'preco']], on='produto', how='left')
df_vendas = df_vendas.set_index('data')
df_vendas['comissao'] = df_vendas['preco'] * COMISSAO

# Seleção de datas, análises e período de agrupamento
data_final_def = df_vendas.index.date.max()
data_inicial_def = date(year=data_final_def.year, month=data_final_def.month, day=1)
data_inicial = st.sidebar.date_input('Data Inicial', data_inicial_def)
data_final = st.sidebar.date_input('Data Final', data_final_def)
analise_selecionada = st.sidebar.selectbox('Analisar:', list(selecao_keys.keys()))
analise_selecionada = selecao_keys[analise_selecionada]
periodo_agrupamento = st.sidebar.selectbox('Agrupar por:', list(agrupamento_keys.keys()))
periodo_agrupamento = agrupamento_keys[periodo_agrupamento]

# Filtragem dos dados de vendas
df_vendas_corte = df_vendas[(df_vendas.index.date >= data_inicial) & (df_vendas.index.date <= data_final)]
df_vendas_corte_anterior = df_vendas[(df_vendas.index.date >= data_inicial - timedelta(days=30)) & 
                                     (df_vendas.index.date <= data_final - timedelta(days=30))]

# Layout do dashboard
st.markdown('<h1 style="text-align:center;">Dashboard de Análise</h1>', unsafe_allow_html=True)

# Métricas principais
st.markdown('<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    valor_vendas = f"R$ {df_vendas_corte['preco'].sum():,.2f}"
    dif_metrica = df_vendas_corte['preco'].sum() - df_vendas_corte_anterior['preco'].sum()
    st.metric('Valor de vendas no período', valor_vendas, float(dif_metrica))

with col2:
    quantidade_vendas = df_vendas_corte['preco'].count()
    dif_metrica = quantidade_vendas - df_vendas_corte_anterior['preco'].count()
    st.metric('Quantidade de vendas no período', quantidade_vendas, int(dif_metrica))

with col3:
    principal_filial = df_vendas_corte['filial'].value_counts().index[0]
    st.metric('Principal Filial', principal_filial)

with col4:
    principal_vendedor = df_vendas_corte['vendedor'].value_counts().index[0]
    st.metric('Principal Vendedor', principal_vendedor)

st.markdown('</div>', unsafe_allow_html=True)

# Primeira linha de gráficos
col1, col2, col3, col4 = st.columns(4)

with col1:
    fig_vendas_tempo = px.line(df_vendas_corte.resample(periodo_agrupamento).sum().reset_index(), 
                               x='data', y='preco', title='Vendas ao longo do tempo')
    fig_vendas_tempo.update_xaxes(title_text='Data')
    fig_vendas_tempo.update_yaxes(title_text='Valor Venda')
    st.plotly_chart(fig_vendas_tempo, use_container_width=True)

with col2:
    fig_analise = px.pie(df_vendas_corte, 
                         names=analise_selecionada, 
                         title=f'Distribuição por {analise_selecionada}')
    st.plotly_chart(fig_analise, use_container_width=True)

with col3:
    vendas_por_filial = df_vendas_corte.groupby('filial').sum().reset_index()
    fig_vendas_filial = px.bar(vendas_por_filial, 
                               x='filial', y='preco', 
                               title='Vendas por Filial', 
                               color='preco', 
                               color_continuous_scale='RdYlGn')
    fig_vendas_filial.update_xaxes(title_text='Filial')
    fig_vendas_filial.update_yaxes(title_text='Valor Venda')
    st.plotly_chart(fig_vendas_filial, use_container_width=True)

with col4:
    vendas_por_vendedor = df_vendas_corte.groupby(['vendedor', 'produto']).sum().reset_index()
    fig_vendas_vendedor = px.bar(vendas_por_vendedor, 
                                 x='vendedor', y='preco', 
                                 title='Ranking de Vendedores', 
                                 color='produto', 
                                 labels={'preco': 'Valor Venda', 'vendedor': 'Vendedor', 'produto': 'Produto'},
                                 text_auto=True)
    fig_vendas_vendedor.update_xaxes(title_text='Vendedor')
    fig_vendas_vendedor.update_yaxes(title_text='Valor Venda')
    st.plotly_chart(fig_vendas_vendedor, use_container_width=True)

# Segunda linha de gráficos
col5, col6, col7, col8 = st.columns(4)

with col5:
    fig_vendas_genero = px.bar(df_vendas_corte.groupby('cliente_genero').sum().reset_index(), 
                               x='cliente_genero', y='preco', 
                               title='Vendas por Gênero do Cliente', 
                               color='preco', 
                               color_continuous_scale='Bluered')
    fig_vendas_genero.update_xaxes(title_text='Gênero do Cliente')
    fig_vendas_genero.update_yaxes(title_text='Valor Venda')
    st.plotly_chart(fig_vendas_genero, use_container_width=True)

with col6:
    fig_vendas_pagamento = px.pie(df_vendas_corte, 
                                  names='forma_pagamento', 
                                  values='preco', 
                                  title='Vendas por Forma de Pagamento')
    st.plotly_chart(fig_vendas_pagamento, use_container_width=True)

with col7:
    fig_comissoes = px.bar(df_vendas_corte.groupby('vendedor').sum().reset_index(), 
                           x='vendedor', y='comissao', 
                           title='Comissões Geradas por Vendedor', 
                           color='comissao', 
                           color_continuous_scale='Viridis')
    fig_comissoes.update_xaxes(title_text='Vendedor')
    fig_comissoes.update_yaxes(title_text='Comissão')
    st.plotly_chart(fig_comissoes, use_container_width=True)

with col8:
    df_vendas_corte['vendas_acumuladas'] = df_vendas_corte['preco'].cumsum()
    fig_vendas_acumuladas = px.line(df_vendas_corte.reset_index(), 
                                    x='data', y='vendas_acumuladas', 
                                    title='Evolução de Vendas Acumuladas')
    fig_vendas_acumuladas.update_xaxes(title_text='Data')
    fig_vendas_acumuladas.update_yaxes(title_text='Vendas Acumuladas')
    st.plotly_chart(fig_vendas_acumuladas, use_container_width=True)


# CSS para centralizar e aumentar a fonte da tabela de dados e para alterar o fundo para branco
st.markdown("""
    <style>
    .center-table {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .big-font {
        font-size: 20px !important;
    }
    .reportview-container .main .block-container {
        background-color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Reorganização das colunas da tabela
df_vendas_corte = df_vendas_corte.reset_index()
df_vendas_corte = df_vendas_corte[['filial', 'vendedor', 'id_venda', 'produto', 'data', 'cliente_nome', 'cliente_genero', 'forma_pagamento', 'preco', 'comissao']]

# Tabela com dados filtrados centralizada e com fonte aumentada
st.markdown('<h2 style="text-align:center;">Tabela de Dados</h2>', unsafe_allow_html=True)
st.markdown('<div class="center-table big-font">', unsafe_allow_html=True)
st.dataframe(df_vendas_corte)
st.markdown('</div>', unsafe_allow_html=True)

# Fim do dashboard
st.markdown('<hr>', unsafe_allow_html=True)

# Rodapé
st.sidebar.markdown('Desenvolvido por [Bruno Almeida](https://www.linkedin.com/in/brunodesouzaalmeida/)')
