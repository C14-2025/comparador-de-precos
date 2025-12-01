import streamlit as st


st.set_page_config(
    page_title="Comparador de preço",
    page_icon="💲",
    layout="wide"
)

import streamlit as st

if "usuario_id" not in st.session_state:
    st.warning("Você precisa fazer login.")
    st.stop()

    st.title("Bem vindo, Usuário") # TROCAR AQUI DEPOIS DE IMPLEMENTAR O SISTEMA DE LOGIN AAAAAAAAAAAAAAAAAAAAAAA
    st.markdown("<br>",unsafe_allow_html=True)
    #st.header("Pesquise um produto que você gostaria de comprar: ")
    
    produto_pesquisado = st.text_input("Pesquise um prduto que você tem interesse em comprar:",placeholder="🔍 Nome do produto...")

    # A ideia é que a home seja um padrão, e que o usuário pode fazer buscas sem estar logado, mas ele nao pode "salvar" um produto.
    # e os preços não serão convertidos.