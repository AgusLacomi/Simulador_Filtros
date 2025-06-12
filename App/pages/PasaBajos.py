import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

MODO_FC = "A"  # Modo inicial para la frecuencia de corte
MODO_TAU = "B"  # Modo alternativo para el tiempo característico

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Filtros de Señales",
    page_icon="📡",
    layout="wide"
)

st.title("🔧 Simulador de Filtros de Señales")
st.markdown("### Explora el comportamiento del filtro pasa-bajo")

# Sidebar para controles
st.sidebar.header("Parámetros de la Señal")

# Parámetros de la señal de entrada
freq_signal = st.sidebar.number_input("Frecuencia de la señal principal (Hz)", min_value=1.0, max_value=100.0, step=0.1)
freq_noise = st.sidebar.number_input("Frecuencia del ruido (Hz)", min_value=1.0, max_value=200.0, step=0.1)
amplitude_signal = st.sidebar.number_input("Amplitud de la señal", min_value=0.1, max_value=12.0)
amplitude_noise = st.sidebar.number_input("Amplitud del ruido", min_value=0.0, max_value=1.0, step=0.1)

#freq_signal = st.sidebar.slider("Frecuencia de la señal principal (Hz)", 1, 1000, 10)
#freq_noise = st.sidebar.slider("Frecuencia del ruido (Hz)", 1, 200, 50)
#amplitude_signal = st.sidebar.slider("Amplitud de la señal", 0.1, 2.0, 1.0, 0.1)
#amplitude_noise = st.sidebar.slider("Amplitud del ruido", 0.0, 1.0, 0.3, 0.1)

# Parámetros del filtro
st.sidebar.header("Parámetros del Filtro")
filter_type = "Pasa-Bajo"  # Filtro fijo para este ejemplo

# Frecuencia de muestreo
fs = 1000  # Hz
t = np.linspace(0, 2, fs * 2, endpoint=False)

# Generar señal de entrada
signal_clean = amplitude_signal * np.sin(2 * np.pi * freq_signal * t)
noise = amplitude_noise * np.sin(2 * np.pi * freq_noise * t)
signal_input = signal_clean + noise

# Función para alternar entre modos
def alternar_modo():
    st.session_state.modo = MODO_TAU if st.session_state.modo == MODO_FC else "A"

# Parámetros específicos del filtro
if filter_type == "Pasa-Bajo":
    # Inicializar el estado si no existe
    if "modo" not in st.session_state:
        st.session_state.modo = MODO_FC
    
    st.sidebar.button( "Frecuencia de Corte" if st.session_state.modo == MODO_FC else "Tiempo Característico",
    on_click = alternar_modo)

    # Mostrar contenido según modo
    if st.session_state.modo == MODO_FC:
        """st.sidebar.success("Este es el contenido de la sidebar (Modo A)")"""
        cutoff = st.sidebar.number_input("Frecuencia de corte (Hz)", min_value=1.0, max_value=100.0, step=0.1)
        #cutoff = st.sidebar.slider("Frecuencia de corte (Hz)", 0.1, 100.0, 10.0)
    else:
        """valor = st.number_input("Ingresa un valor numérico (Modo B)", min_value=0, max_value=100)
        st.write("Valor ingresado:", valor)"""
        resist = st.sidebar.number_input("valor R1 - Resistencia (Ω)", min_value = 1.0, max_value = 10.0, step=0.1)
        capacitance = st.sidebar.number_input("valor C1 - Capacitancia (ϝ)", min_value = 1.0, max_value = 10.0, step=0.1)
        cutoff =  1 / (2 * np.pi * resist * capacitance)  # Frecuencia de corte calculada
    
    order = st.sidebar.slider("Orden del filtro", 1, 10, 4)

    
    # Diseño del filtro pasa-bajo
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)

# Aplicar filtro
signal_filtered = signal.filtfilt(b, a, signal_input)

st.subheader("📈 Señales en el Tiempo")

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))

# Señal original
ax1.plot(t[:500], signal_input[:500], 'b-', linewidth=1, label='Señal + Ruido')
ax1.plot(t[:500], signal_clean[:500], 'g--', linewidth=2, alpha=0.7, label='Señal Original')
ax1.set_title('Señal de Entrada')
ax1.set_ylabel('Amplitud')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Señal filtrada
ax2.plot(t[:500], signal_filtered[:500], 'r-', linewidth=1.5, label='Señal Filtrada')
ax2.plot(t[:500], signal_clean[:500], 'g--', linewidth=2, alpha=0.7, label='Señal Original')
ax2.set_title(f'Señal Filtrada - {filter_type}')
ax2.set_ylabel('Amplitud')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Comparación
ax3.plot(t[:500], signal_input[:500], 'b-', linewidth=1, alpha=0.6, label='Entrada')
ax3.plot(t[:500], signal_filtered[:500], 'r-', linewidth=1.5, label='Filtrada')
ax3.set_title('Comparación')
ax3.set_xlabel('Tiempo (s)')
ax3.set_ylabel('Amplitud')
ax3.legend()
ax3.grid(True, alpha=0.3)

plt.tight_layout()
st.pyplot(fig)

# Respuesta en frecuencia del filtro
st.subheader("🎯 Respuesta en Frecuencia del Filtro")

# Calcular respuesta en frecuencia
w, h = signal.freqz(b, a, worN=8000)
freq_response = w * fs / (2 * np.pi)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

# Magnitud
ax1.plot(freq_response, 20 * np.log10(abs(h)), 'g-', linewidth=2)
ax1.set_title(f'Respuesta en Magnitud - Filtro {filter_type}')
ax1.set_xlabel('Frecuencia (Hz)')
ax1.set_ylabel('Magnitud (dB)')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 100)

# Marcar frecuencias de corte
if filter_type == "Pasa-Bajo":
    ax1.axvline(cutoff, color='red', linestyle='--', alpha=0.7, label=f'Fc = {cutoff} Hz')

ax1.legend()

# Fase
phase = np.unwrap(np.angle(h))
ax2.plot(freq_response, np.degrees(phase), 'purple', linewidth=2)
ax2.set_title('Respuesta en Fase')
ax2.set_xlabel('Frecuencia (Hz)')
ax2.set_ylabel('Fase (grados)')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 500)

plt.tight_layout()
st.pyplot(fig)

# Información adicional
st.subheader("📋 Información del Filtro")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Tipo de Filtro", filter_type)
    st.metric("Orden del Filtro", order)

with col2:
    if filter_type in ["Pasa-Bajo", "Pasa-Alto"]:
        st.metric("Frecuencia de Corte", f"{cutoff} Hz")
    
    st.metric("Frecuencia de Muestreo", f"{fs} Hz")

with col3:
    # Calcular atenuación en la frecuencia del ruido
    noise_freq_idx = np.argmin(np.abs(freq_response - freq_noise))
    attenuation = 20 * np.log10(abs(h[noise_freq_idx]))
    st.metric("Atenuación del Ruido", f"{attenuation:.1f} dB")
    
    # SNR mejorado
    snr_input = 20 * np.log10(amplitude_signal / amplitude_noise)
    signal_power_filtered = np.var(signal_filtered)
    noise_power_filtered = np.var(signal_filtered - signal_clean)
    if noise_power_filtered > 0:
        snr_output = 10 * np.log10(signal_power_filtered / noise_power_filtered)
        st.metric("Mejora SNR", f"{snr_output - snr_input:.1f} dB")
    else:
        st.metric("Mejora SNR", "∞ dB")

# Explicación del filtro
st.subheader("💡 Explicación")
if filter_type == "Pasa-Bajo":
    st.info("""
    **Filtro Pasa-Bajo**: Permite el paso de frecuencias por debajo de la frecuencia de corte 
    y atenúa las frecuencias superiores. Útil para eliminar ruido de alta frecuencia.
    """)
elif filter_type == "Pasa-Alto":
    st.info("""
    **Filtro Pasa-Alto**: Permite el paso de frecuencias por encima de la frecuencia de corte 
    y atenúa las frecuencias inferiores. Útil para eliminar componentes de baja frecuencia como DC offset.
    """)
else:
    st.info("""
    **Filtro Pasa-Banda**: Permite el paso de frecuencias dentro de un rango específico 
    y atenúa tanto las frecuencias más bajas como las más altas. Útil para seleccionar una banda específica.
    """)

if st.button(
    label="volver",
    key="btn_volver_opcion1"
):
    if "page_to_go" in st.session_state:
        del st.session_state.page_to_go
    st.switch_page("app.py")