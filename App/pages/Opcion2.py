import streamlit as st

st.title("Página de la Opción 2")
st.write("Aquí va el contenido específico para la Opción 2.")

if st.button(
    label="volver",
    key="btn_volver_opcion1"
):
    if "page_to_go" in st.session_state:
        del st.session_state.page_to_go
    st.switch_page("app.py")