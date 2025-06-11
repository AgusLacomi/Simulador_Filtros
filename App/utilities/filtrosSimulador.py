import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Simulador de Filtros de Señales",
    page_icon="📡",
    layout="wide"
)

st.title("🔧 Simulador de Filtros de Señales")
st.markdown("### Explora el comportamiento de filtros pasa-alto, pasa-bajo y pasa-banda")

# Sidebar para controles
st.sidebar.header("Parámetros de la Señal")

# Parámetros de la señal de entrada
freq_signal = st.sidebar.slider("Frecuencia de la señal principal (Hz)", 1, 100, 10)
freq_noise = st.sidebar.slider("Frecuencia del ruido (Hz)", 1, 200, 50)
amplitude_signal = st.sidebar.slider("Amplitud de la señal", 0.1, 2.0, 1.0, 0.1)
amplitude_noise = st.sidebar.slider("Amplitud del ruido", 0.0, 1.0, 0.3, 0.1)

# Parámetros del filtro
st.sidebar.header("Parámetros del Filtro")
filter_type = st.sidebar.selectbox(
    "Tipo de Filtro",
    ["Pasa-Bajo", "Pasa-Alto", "Pasa-Banda"]
)

# Frecuencia de muestreo
fs = 1000  # Hz
t = np.linspace(0, 2, fs * 2, endpoint=False)

# Generar señal de entrada
signal_clean = amplitude_signal * np.sin(2 * np.pi * freq_signal * t)
noise = amplitude_noise * np.sin(2 * np.pi * freq_noise * t)
signal_input = signal_clean + noise

# Parámetros específicos del filtro
if filter_type == "Pasa-Bajo":
    cutoff = st.sidebar.slider("Frecuencia de corte (Hz)", 1, 100, 30)
    order = st.sidebar.slider("Orden del filtro", 1, 10, 4)
    
    # Diseño del filtro pasa-bajo
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='low', analog=False)
    
elif filter_type == "Pasa-Alto":
    cutoff = st.sidebar.slider("Frecuencia de corte (Hz)", 1, 100, 20)
    order = st.sidebar.slider("Orden del filtro", 1, 10, 4)
    
    # Diseño del filtro pasa-alto
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    
else:  # Pasa-Banda
    low_freq = st.sidebar.slider("Frecuencia inferior (Hz)", 1, 80, 15)
    high_freq = st.sidebar.slider("Frecuencia superior (Hz)", 20, 100, 35)
    order = st.sidebar.slider("Orden del filtro", 1, 10, 4)
    
    # Diseño del filtro pasa-banda
    nyquist = fs / 2
    low = low_freq / nyquist
    high = high_freq / nyquist
    b, a = signal.butter(order, [low, high], btype='band', analog=False)

# Aplicar filtro
signal_filtered = signal.filtfilt(b, a, signal_input)

# Layout en columnas
col1, col2 = st.columns(2)

with col1:
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

with col2:
    st.subheader("📊 Análisis Frecuencial")
    
    # FFT de las señales
    fft_input = np.fft.fft(signal_input)
    fft_filtered = np.fft.fft(signal_filtered)
    freqs = np.fft.fftfreq(len(signal_input), 1/fs)
    
    # Solo frecuencias positivas
    pos_mask = freqs > 0
    freqs_pos = freqs[pos_mask]
    fft_input_pos = np.abs(fft_input[pos_mask])
    fft_filtered_pos = np.abs(fft_filtered[pos_mask])
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    
    # Espectro de entrada
    ax1.plot(freqs_pos[:len(freqs_pos)//4], fft_input_pos[:len(freqs_pos)//4], 'b-', linewidth=1.5)
    ax1.set_title('Espectro de Frecuencias - Entrada')
    ax1.set_ylabel('Magnitud')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 100)
    
    # Espectro filtrado
    ax2.plot(freqs_pos[:len(freqs_pos)//4], fft_filtered_pos[:len(freqs_pos)//4], 'r-', linewidth=1.5)
    ax2.set_title('Espectro de Frecuencias - Filtrada')
    ax2.set_ylabel('Magnitud')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 100)
    
    # Comparación de espectros
    ax3.plot(freqs_pos[:len(freqs_pos)//4], fft_input_pos[:len(freqs_pos)//4], 'b-', 
             linewidth=1, alpha=0.6, label='Entrada')
    ax3.plot(freqs_pos[:len(freqs_pos)//4], fft_filtered_pos[:len(freqs_pos)//4], 'r-', 
             linewidth=1.5, label='Filtrada')
    ax3.set_title('Comparación Espectral')
    ax3.set_xlabel('Frecuencia (Hz)')
    ax3.set_ylabel('Magnitud')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0, 100)
    
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
elif filter_type == "Pasa-Alto":
    ax1.axvline(cutoff, color='red', linestyle='--', alpha=0.7, label=f'Fc = {cutoff} Hz')
else:
    ax1.axvline(low_freq, color='red', linestyle='--', alpha=0.7, label=f'F1 = {low_freq} Hz')
    ax1.axvline(high_freq, color='red', linestyle='--', alpha=0.7, label=f'F2 = {high_freq} Hz')

ax1.legend()

# Fase
phase = np.unwrap(np.angle(h))
ax2.plot(freq_response, np.degrees(phase), 'purple', linewidth=2)
ax2.set_title('Respuesta en Fase')
ax2.set_xlabel('Frecuencia (Hz)')
ax2.set_ylabel('Fase (grados)')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 100)

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
    else:
        st.metric("Banda de Paso", f"{low_freq}-{high_freq} Hz")
    
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