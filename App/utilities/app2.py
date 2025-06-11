import streamlit as st
from PIL import Image

# Configurar el estado inicial
if 'button_states' not in st.session_state:
    st.session_state.button_states = [0, 0, 0]  # 0 para imagen A, 1 para imagen B

st.title("3 Botones con Imágenes Alternables")

# Rutas de las imágenes (ajusta estas rutas según tus archivos)
image_paths = {
    'button1_a': '..\images\RC1.jpg',
    'button1_b': '..\images\RL1.jpg',
    'button2_a': '..\images\RC2.jpg', 
    'button2_b': '..\images\RL2.jpg',
    'button3_a': '..\images\RLC1.jpg',
    'button3_b': '..\images\RLC2.jpg'
}

# Función para alternar el estado de un botón
def toggle_image(button_index):
    st.session_state.button_states[button_index] = 1 - st.session_state.button_states[button_index]

# Crear los 3 botones con imágenes alternables
for i in range(3):
    st.subheader(f"Botón {i+1}")
    
    # Crear columnas para los controles
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("🔄 Cambiar", key=f"toggle_{i}"):
            toggle_image(i)
    
    with col2:
        # Determinar qué imagen mostrar
        current_state = st.session_state.button_states[i]
        if current_state == 0:
            image_key = f'button{i+1}_a'
            image_label = "Imagen A"
        else:
            image_key = f'button{i+1}_b'
            image_label = "Imagen B"
        
        try:
            # Cargar la imagen
            image = Image.open(image_paths[image_key])
            
            # Imagen clickeable como botón de selección
            if st.button(f"🖼️", key=f"select_{i}", help=f"Seleccionar {image_label} - Botón {i+1}"):
                st.success(f"¡Seleccionaste {image_label} del Botón {i+1}!")
            
            # Mostrar la imagen
            st.image(image, caption=f"{image_label} - Botón {i+1}", use_column_width=True)
                
        except FileNotFoundError:
            st.error(f"No se encontró la imagen: {image_paths[image_key]}")
            st.info("Asegúrate de que las imágenes estén en el directorio correcto")
    
    with col3:
        # Columna vacía para mantener el layout centrado
        st.write("")
    
    st.divider()

# Mostrar el estado actual (opcional, para debug)
with st.expander("Estado actual de los botones"):
    for i, state in enumerate(st.session_state.button_states):
        image_type = "A" if state == 0 else "B"
        st.write(f"Botón {i+1}: Imagen {image_type}")