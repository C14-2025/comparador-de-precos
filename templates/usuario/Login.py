import streamlit as st

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

        nome_de_usuario = st.text_input("Nome de usuario")
        senha = st.text_input("Senha",type="password")

        ativar = bool(bool(nome_de_usuario) and bool(senha))

        if st.button("Login",disabled=ativar):
            st.success("Logado com sucesso!")
            
            #st.switch_page("pages/Home.py")
