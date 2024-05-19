from pathlib import Path
import streamlit as st
import pandas as pd

COMISSAO = 0.08

def configurar_streamlit():
    """Configurações iniciais do Streamlit."""
    st.set_page_config(
        page_title="Analisador de Vendas",
        page_icon="📊",
        layout="wide"
    )

def verificar_arquivos(pasta_datasets):
    """Verifica se os arquivos necessários existem."""
    arquivos = ['vendas.csv', 'filiais.csv', 'produtos.csv']
    for arquivo in arquivos:
        caminho_arquivo = pasta_datasets / arquivo
        if not caminho_arquivo.exists():
            st.error(f"Arquivo {arquivo} não encontrado na pasta {pasta_datasets}.")
            return False
    return True

def leitura_de_dados():
    """Lê os dados dos arquivos CSV e os armazena no estado da sessão."""
    if 'dados' not in st.session_state:
        pasta_datasets = Path(__file__).parents[1] / 'datasets'
        
        if verificar_arquivos(pasta_datasets):
            df_vendas = pd.read_csv(pasta_datasets / 'vendas.csv', decimal=',', sep=';', index_col=0, parse_dates=True)
            df_filiais = pd.read_csv(pasta_datasets / 'filiais.csv', decimal=',', sep=';', index_col=0)
            df_produtos = pd.read_csv(pasta_datasets / 'produtos.csv', decimal=',', sep=';', index_col=0)
            dados = {
                'df_vendas': df_vendas,
                'df_filiais': df_filiais,
                'df_produtos': df_produtos
            }
            st.session_state['caminho_datasets'] = pasta_datasets
            st.session_state['dados'] = dados
            st.success("Dados carregados com sucesso!")
        else:
            st.error("Erro ao carregar os dados. Verifique os arquivos e tente novamente.")
    else:
        st.info("Dados já carregados na sessão.")

def main():
    """Função principal que executa o fluxo do programa."""
    configurar_streamlit()
    
    st.sidebar.markdown('Desenvolvido por [Bruno Almeida](https://www.linkedin.com/in/brunodesouzaalmeida/)')
    st.markdown('# Bem-vindo ao Analisador de Vendas')
    
    leitura_de_dados()
    
    if 'dados' in st.session_state:
        st.write("Dados carregados com sucesso. Pronto para análise.")
        st.dataframe(st.session_state['dados']['df_vendas'].head())  # Exemplo de visualização inicial
    
if __name__ == "__main__":
    main()
