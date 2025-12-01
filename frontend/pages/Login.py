import streamlit as st
import re
import requests

class Login:
    st.set_page_config(
        page_title="Login",
        page_icon="💲",
        layout="wide"
    )

    st.markdown("""
        <style>
            div.stButton > button {
                width: 225px;
                height: 40px;
                background-color: #43B929;
                color: white;
                border-radius: 10px;
            }
            
            .centered-header {
                text-align: center;
            }
                    
            .stSidebar {
                background: #43B929
            }
        </style>
        """, unsafe_allow_html=True)

    # st.navigation(["Home","Login","Criar Conta"], position="top")
    
    coluna_1, coluna_2, coluna_3 = st.columns(3)

    with coluna_2:

        st.markdown('<h2 class="centered-header"><bold>ACESSE SUA CONTA</bold></h2>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        email = st.text_input("E-mail")
        senha = st.text_input("Senha",type="password")

        ativar = bool(bool(email) and bool(senha))

        if st.button("Login", disabled=not ativar):

            resposta = requests.post(
                "http://127.0.0.1:8000/api/usuarios/login/",
                json={"email": email, "senha": senha}
            )

            if resposta.status_code == 200:
                st.success("Logado com sucesso!")
                dados = resposta.json()
                st.session_state["usuario_id"] = dados["usuario_id"]
                st.session_state["usuario_nome"] = dados["nome"]

                st.switch_page("Home.py")
            
            else:
                st.error(resposta.json().get("erro", "Erro desconhecido"))
