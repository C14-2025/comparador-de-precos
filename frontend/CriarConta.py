import streamlit as st
import re
import requests

class CriarConta:

    def validar_dados_sinc(tipo,dado):
        
        if(tipo == "email"):
            email_padrao = r"^[^@\s]+@[^@\s]+\.[a-zA-Z]+$"
            return bool(re.match(email_padrao,dado))
        
        if(tipo == "senha"):
            senha_padrao = r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[^a-zA-Z0-9]).{12,}$"  
            return bool(re.match(senha_padrao,dado))
        
        if(tipo=="cep"):
            match = re.match(r"^\d{5}-?\d{3}$", dado) # verifica se o valor inserido segue o padrão de cep/zip code

            if not match:
                return False
            else:
                dado = re.sub('-','',dado)

            cep_existe = requests.get(f"https://viacep.com.br/ws/{dado}/json")

            dados_cep = cep_existe.json()

            if dados_cep.get("erro"):
                return False
            
            return True
        
    def validar_senha(senha,confirmar_senha):
        return bool(senha == confirmar_senha)

    st.set_page_config(
        page_title="Criar conta",
        page_icon="💲",
        layout="centered"
    )

    st.markdown("""
        <style>    
                    
            body {
                background-color: #1A1423;
            }
            .stApp {
                background-color: #1A1423;
            }
                        
            div.stButton > button {
                width: 340px;
                height: 40px;
                background-color: #43B929;
                color: white;
                border-radius: 10px;
            }

        </style>        
    """,unsafe_allow_html=True)
    
    nationalidades = [
        "Brasileiro", "Americano", "Alemão", "Francês", "Italiano",
        "Japones", "Chines", "Indiano", "Mexicano", "Canadense",
        "Espanhol", "Argentino", "Africano do sul", "Australiano", "Britanico"
    ] # Usar por enquanto, depois puxar do backend

    st.title(f"Crie a sua conta para economizar!")

    st.markdown("<br>", unsafe_allow_html=True)

    coluna_1,coluna_2 = st.columns(2)

    with coluna_1:
        st.image(
            "https://gifdb.com/images/high/rich-lolo-cat-counting-money-mrqt0i7cn24lct0m.gif",
            width="stretch"
            )

    with coluna_2:
        nome = st.text_input("Nome")

        email = st.text_input("Email")
        email_valido = validar_dados_sinc("email", email) if email else False

        if email and not email_valido:
            st.markdown(
                "<p style='color: red; font-size: 13px; margin-top: -10px;'>⚠ Email inválido</p>",
                unsafe_allow_html=True
            )

        senha = st.text_input("Senha", type="password")
        senha_valida = validar_dados_sinc("senha", senha) if senha else False

        if senha and not senha_valida:
            st.markdown(
                """
                <p style='color: red; font-size: 13px; margin-top: -10px;'>⚠ Senha inválida</p>
                <p style='color: red; font-size: 13px; margin-top: -10px;'>A senha precisa ter pelo menos: um cáracter especial, um número e uma letra. E no mínimo 12 dígitos.</p>
                """,
                unsafe_allow_html=True
            )

        confirmar_senha = st.text_input("Confirmar senha", type="password")
        senhas_iguais = validar_senha(senha, confirmar_senha) if senha and confirmar_senha else False

        if senha and confirmar_senha and not senhas_iguais:
            st.markdown(
                "<p style='color: red; font-size: 13px; margin-top: -10px;'>⚠ Senhas não batem uma com a outra</p>",
                unsafe_allow_html=True
            )
        
        col_1,col_2 = st.columns(2)

        with col_1:
            cep = st.text_input("CEP")
            cep_valido = validar_dados_sinc("cep", cep) if cep else False

            if cep and not cep_valido:
                st.markdown(
                    "<p style='color: red; font-size: 13px; margin-top: -10px;'>⚠ CEP inválido</p>",
                    unsafe_allow_html=True
                )

            
        with col_2:
            nacionalidade = st.selectbox("Nacionalidade", nationalidades)

        termos = st.checkbox("Eu aceito os [Termos de Condições de Uso](https://www.youtube.com/watch?v=dQw4w9WgXcQ)")

        campos_obrigatorios_preenchidos = bool(
            bool(nome) and
            bool(email) and
            bool(senha) and
            bool(confirmar_senha) and
            bool(cep) and
            bool(nacionalidade) and
            bool(termos)
            )
        
        validacoes_passaram = email_valido and senha_valida and senhas_iguais and cep_valido
        ativar_botao = campos_obrigatorios_preenchidos and validacoes_passaram

        if st.button("Criar conta", disabled=not ativar_botao):
            dados = {
                "nome": nome,
                "email": email,
                "senha": senha,
                "cep": cep,
                "nacionalidade": nacionalidade,
            }

            resposta = requests.post(
                "http://127.0.0.1:8000/api/usuarios/cadastrar/",
                json=dados
            )

            if resposta.status_code == 201:
                st.success("Conta criada com sucesso!")
            else:
                st.error("Usuário já cadastrado.")


