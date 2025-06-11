import streamlit as st
from pathlib import Path

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Filtros",
                   layout="wide",
                  page_icon="🔷")

st.title("Selecciona una opción")

# Ruta base de imágenes
img_dir = Path(__file__).parent / "images"

cols = st.columns(3, vertical_alignment= "center")

# Configuración de imágenes locales y sus páginas destino
opciones = [
    {"nombre": "Opción 1", "archivo": "RL1.jpg", "pagina": "Opcion1"},
    {"nombre": "Opción 2", "archivo": "RL2.jpg", "pagina": "Opcion2"},
    {"nombre": "Opción 3", "archivo": "RLC1.jpg", "pagina": "Opcion3"},
]

# Bucle de botones
for col, opcion in zip(cols, opciones):
    with col:
        if (opcion["nombre"] == "Opción 1"):
            st.image(img_dir / opcion["archivo"], width=460)
            left_spacer, center_col, right_spacer = st.columns([1.5, 1, 2.3])
        elif (opcion["nombre"] == "Opción 2"):
            st.image(img_dir / opcion["archivo"], width=470)
            left_spacer, center_col, right_spacer = st.columns([1.5, 1, 1.9])    
        else:    
            st.image(img_dir / opcion["archivo"], width=500)
            left_spacer, center_col, right_spacer = st.columns([1.5, 1, 1.5])
        
        with center_col:
            if st.button(
                label=opcion["nombre"].capitalize(),
                key=f"btn_{opcion['nombre']}"
            ):
                st.session_state.page_to_go = opcion["pagina"]

# Redirección fuera del bucle de botones
if "page_to_go" in st.session_state:
    st.switch_page(f"pages/{st.session_state.page_to_go}.py")