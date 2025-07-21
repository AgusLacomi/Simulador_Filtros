import streamlit as st
from pathlib import Path
from PIL import Image

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Filtros",
                   layout="wide",
                  page_icon="🔷")

# Configurar el estado inicial
if 'button_states' not in st.session_state:
    st.session_state.button_states = [0, 0, 0]  # 0 para imagen A, 1 para imagen B

st.title("Selecciona una opción")

# Rutas de las imágenes (ajusta estas rutas según tus archivos)
image_paths = {
    'button1_a': 'images\RC1.jpg',
    'button1_b': 'images\RL1.jpg',
    'button2_a': 'images\RC2.jpg', 
    'button2_b': 'images\RL2.jpg',
    'button3_a': 'images\RLC1.jpg',
    'button3_b': 'images\RLC2.jpg'
}

# Ruta base de imágenes
img_dir = Path(__file__).parent / "images"

# Configuración de imágenes locales y sus páginas destino
opciones = [
    {"nombre": "Opción PARC", "archivo": "RC1.jpg", "pagina": "PasaAltos"},
    {"nombre": "Opción PBRC", "archivo": "RC2.jpg", "pagina": "PasaBajos"},
    {"nombre": "Opción 3", "archivo": "RLC1.jpg", "pagina": "PasaBanda"},
]
cols = st.columns(3, vertical_alignment= "center")

# Función para alternar el estado de un botón
def toggle_image(button_index):
    st.session_state.button_states[button_index] = 1 - st.session_state.button_states[button_index]

# Bucle de botones
for idx, (col, opcion) in enumerate(zip(cols, opciones)):

    with col:
        if st.button("🔄 Cambiar", key=f"toggle_{idx}", help = "Permite ver las diferentes distribuciones"):
            toggle_image(idx)
        
        # Determinar qué imagen mostrar
        current_state = st.session_state.button_states[idx]
        if current_state == 0:
            image_key = f'button{idx+1}_a'
            image_label = "Imagen A"
        else:
            image_key = f'button{idx+1}_b'
            image_label = "Imagen B"
        
        try:
            # Cargar la imagen
            image = Image.open(image_paths[image_key])
            # Mostrar la imagen
            st.image(image, use_container_width=True)
        except FileNotFoundError:
            st.error(f"No se encontró la imagen: {image_paths[image_key]}")
            st.info("Asegúrate de que las imágenes estén en el directorio correcto")
        # Botón de opción al fondo
        left_spacer, center_col, right_spacer = st.columns([1, 1, 1])
        with center_col:
            if st.button(
                label=f"Seleccionar {idx+1}",
                key=f"btn_{idx}"
            ):
                st.session_state.page_to_go = opcion["pagina"]

with st.expander("¿Qué hace este Simulador? ❓"):
    st.markdown("""
    - Podrás simular filtros eléctricos pasivos de primer orden (Pasa-Bajo, Pasa-Alto y Pasa-Banda).
    
    Elegí multiples opciones para ver los comportamientos de los filtros y su respuesta en frecuencia.
    """)

with st.expander("Créditos"):
    st.markdown("""
    - **Autor**: Agustín Lacomi
    - **Fecha de Entrega**: 29/07/2025
    - **Materia dictada por**: Pablo König y Juan Carlos Muñoz
    """)

# Redirección fuera del bucle de botones
if "page_to_go" in st.session_state:
    st.switch_page(f"pages/{st.session_state.page_to_go}.py")