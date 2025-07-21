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
st.markdown("### Explora el comportamiento del filtro pasa-banda")

# Parámetros del filtro
filter_type = "Pasa-Banda"

# Tipo de señal de entrada
st.sidebar.header("Forma de la Señal")
waveform_type = st.sidebar.selectbox(
    "Tipo de señal",
    ["Sinusoidal", "Cuadrada", "Diente de sierra"]
)

st.sidebar.header("Tipo de Ruido")
noise_type = st.sidebar.selectbox(
    "Tipo de ruido",
    ["Blanco", "Seno con fase aleatoria", "Ruido banda estrecha"]
)

# Parámetros de la señal de entrada
freq_signal = st.sidebar.number_input("Frecuencia de la señal principal (Hz)", 1, 100, 10)
freq_noise = st.sidebar.number_input("Frecuencia del ruido (Hz)", 1, 200, 50)

amplitude_signal = st.sidebar.number_input("Amplitud de la señal", 0.1, 2.0, 1.0, 0.1)
amplitude_noise = st.sidebar.number_input("Amplitud del ruido", 0.0, 1.0, 0.3, 0.1)

st.sidebar.header("Parámetros de la Señal")

# Frecuencia de muestreo
fs = 1000  # Hz

def band_limited_noise(min_freq, max_freq, samples, sample_rate):
    freqs = np.fft.fftfreq(samples, 1/sample_rate)
    spectrum = np.zeros(samples, dtype=complex)

    # Activar solo las componentes entre min y max freq
    mask = (np.abs(freqs) >= min_freq) & (np.abs(freqs) <= max_freq)
    spectrum[mask] = np.random.randn(np.count_nonzero(mask)) + 1j * np.random.randn(np.count_nonzero(mask))

    # Convertir a dominio del tiempo
    noise = np.fft.ifft(spectrum).real
    noise = noise / np.max(np.abs(noise))  # normalizar

    return noise

if noise_type == "Seno con fase aleatoria":
    t = np.linspace(0, 1, fs, endpoint=False)
    phi = np.random.uniform(0, 2*np.pi)  # fase aleatoria
    noise = amplitude_noise * np.sin(2 * np.pi * freq_noise * t + phi)
elif noise_type == "Ruido banda estrecha":
    t = np.linspace(0, 1, fs, endpoint=False)
    noise = band_limited_noise((freq_noise - 5), (freq_noise + 5) , fs, fs)  # ruido centrado en 60Hz ±5Hz
elif noise_type == "Blanco":
    t = np.linspace(0, 1, fs, endpoint=False)
    noise = amplitude_noise * np.random.normal(0, 1, size = t.shape)


# Generar señal base según tipo seleccionado
if waveform_type == "Sinusoidal":
    signal_clean = amplitude_signal * np.sin(2 * np.pi * freq_signal * t)
elif waveform_type == "Cuadrada":
    signal_clean = amplitude_signal * signal.square(2 * np.pi * freq_signal * t)
elif waveform_type == "Diente de sierra":
    signal_clean = amplitude_signal * signal.sawtooth(2 * np.pi * freq_signal * t)

signal_input = signal_clean + noise

# Parámetros específicos del filtro
if filter_type == "Pasa-Banda":
    low_freq = st.sidebar.slider("Frecuencia inferior (Hz)", 1, 80, 15)
    high_freq = st.sidebar.slider("Frecuencia superior (Hz)", 1, 100, 35)
    order = st.sidebar.slider("Orden del filtro", 1, 10, 2, help="El orden del filtro afecta la pendiente de la atenuación")
    
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
    ax3.axvline(low_freq, color='red', linestyle='--', alpha=0.7, label=f'F1 = {low_freq} Hz')
    ax3.axvline(high_freq, color='red', linestyle='--', alpha=0.7, label=f'F2 = {high_freq} Hz')

    plt.tight_layout()
    st.pyplot(fig)
st.subheader("🎚️ Ganancia en Voltaje vs Frecuencia")

# Calcular respuesta en frecuencia del filtro
w, h = signal.freqz(b, a, worN=8000, fs=fs)
gain_voltage = np.abs(h)

# Crear figura
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(w, gain_voltage, label="Ganancia (V/V)", color='blue')
ax.set_title("Respuesta en Frecuencia (Voltaje)")
ax.set_xlabel("Frecuencia (Hz)")
ax.set_ylabel("Ganancia (V/V)")
ax.grid(True, alpha=0.3)

# Marcar frecuencias de corte
if filter_type == "Pasa-Banda":
    ax.axvline(low_freq, color='red', linestyle='--', alpha=0.7, label=f'F1 = {low_freq:.2f} Hz')
    ax.axvline(high_freq, color='red', linestyle='--', alpha=0.7, label=f'F2 = {high_freq:.2f} Hz')

ax.set_xlim(0, 100)
ax.set_ylim(0, 1.1)
ax.legend()
st.pyplot(fig)


# Información adicional
st.subheader("📋 Información del Filtro")

col1, col2 = st.columns(2)

with col1:
    st.metric("Tipo de Filtro", filter_type)
    st.metric("Orden del Filtro", order)

with col2:
    st.metric("Banda de Paso", f"{low_freq}-{high_freq} Hz")
    st.metric("Frecuencia de Muestreo", f"{fs} Hz")

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