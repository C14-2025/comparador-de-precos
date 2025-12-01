import streamlit as st

# ============================================================
# CONFIGURAÇÕES INICIAIS
# ============================================================
st.set_page_config(
    page_title="Comparador de preço",
    page_icon="💲",
    layout="wide"
)

# ============================================================
# INICIALIZAÇÃO DA SESSION_STATE (evita KeyError)
# ============================================================
if "usuario_id" not in st.session_state:
    st.session_state["usuario_id"] = None

if "usuario_nome" not in st.session_state:
    st.session_state["usuario_nome"] = ""

if "go_login" not in st.session_state:
    st.session_state.go_login = False

if "go_criar" not in st.session_state:
    st.session_state.go_criar = False


def logout():
    st.session_state["usuario_id"] = None
    st.session_state["usuario_nome"] = ""
    st.rerun()

header_html = f"""
<style>
#custom-header {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    background: #1e1e1e;
    color: white;
    padding: 12px 20px;
    font-size: 20px;
    z-index: 9999;
    display: flex;
    justify-content: space-between;
    align-items: center;
}}
#logout-btn {{
    background: #e74c3c;
    color: white;
    border: none;
    padding: 8px 15px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 16px;
}}
#logout-btn:hover {{
    background: #c0392b;
}}
</style>

<div id="custom-header">
    <div>🛒 Comparador de Preços</div>
    <div>
        {"<button id='logout-btn' onclick='logout()'>Logout</button>" if st.session_state.get("usuario_id") else ""}
    </div>
</div>

<script>
function logout() {{
    fetch('/logout', {{method: 'POST'}})
        .then(() => window.location.reload());
}}
</script>
"""

st.markdown(header_html, unsafe_allow_html=True)

st.write("<br><br><br><br>", unsafe_allow_html=True)

@st.dialog("Acesso negado")
def mostrar_popup_login():
    st.write("Você precisa estar logado para continuar.")

    if st.button(
        "Login",
        use_container_width=True,
        on_click=lambda: st.session_state.update({"go_login": True})
    ):
        st.switch_page("pages/Login.py")

    if st.button(
        "Criar conta",
        use_container_width=True,
        on_click=lambda: st.session_state.update({"go_criar": True})
    ):
        st.switch_page("pages/CriarConta.py")

if not st.session_state.get("usuario_id"):
    mostrar_popup_login()
    st.stop()

nome = st.session_state.get("usuario_nome", "Usuário")
st.title(f"Bem-vindo, {nome} 👋")

produto_pesquisado = st.text_input(
    "Pesquise um produto que você tem interesse em comprar:",
    placeholder="🔍 Nome do produto..."
)
