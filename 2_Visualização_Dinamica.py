from pathlib import Path
import streamlit as st
import pandas as pd
from utilidades import leitura_de_dados, COMISSAO

# Definindo constantes e funções fora do corpo do script
COLUNAS_ANALISE = ['filial', 'vendedor', 'produto', 'cliente_genero', 'forma_pagamento']
COLUNAS_VALOR = ['preco', 'comissao']
FUNCOES_AGG = {'soma': 'sum', 'contagem': 'count'}

# Carregando os dados
leitura_de_dados()
df_vendas = st.session_state['dados']['df_vendas']
df_filiais = st.session_state['dados']['df_filiais']
df_produtos = st.session_state['dados']['df_produtos']

# Renomeando coluna de produtos
df_produtos = df_produtos.rename(columns={'nome': 'produto'})

# Realizando o merge dos dataframes
df_vendas = df_vendas.reset_index()
df_vendas = pd.merge(left=df_vendas,
                     right=df_produtos[['produto', 'preco']],
                     on='produto',  
                     how='left')
df_vendas = df_vendas.set_index('data')
df_vendas['comissao'] = df_vendas['preco'] * COMISSAO

# Criando a interface do usuário
indices_selecionados = st.sidebar.multiselect('Selecione os índices', COLUNAS_ANALISE)
col_analises_exc = [c for c in COLUNAS_ANALISE if c not in indices_selecionados]
colunas_selecionadas = st.sidebar.multiselect('Selecione as colunas', col_analises_exc)
valor_selecionado = st.sidebar.selectbox('Selecione o valor de análise:', COLUNAS_VALOR)
metrica_selecionada = st.sidebar.selectbox('Selecione a métrica:', list(FUNCOES_AGG.keys()))

# Realizando a análise e exibindo os resultados
if indices_selecionados and colunas_selecionadas:
    metrica_selecionada = FUNCOES_AGG[metrica_selecionada]
    vendas_pivotadas = pd.pivot_table(df_vendas, 
                                      index=indices_selecionados,
                                      columns=colunas_selecionadas,
                                      values=valor_selecionado,
                                      aggfunc=metrica_selecionada)
    vendas_pivotadas['TOTAL GERAL'] = vendas_pivotadas.sum(axis=1)
    vendas_pivotadas.loc['TOTAL GERAL'] = vendas_pivotadas.sum(axis=0).to_list()
    st.dataframe(vendas_pivotadas)
