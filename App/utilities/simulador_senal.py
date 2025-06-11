import streamlit as st
import plotly.graph_objs as go
import numpy as np
import time

st.set_page_config(layout="wide")
st.title("🧲 Simulador de Señal con Múltiples Inductores")

if st.button("🔁 Reiniciar fase"):
    st.session_state.phase = 0.0

# Columnas: izq, centro (gráfico), der
col1, col2, col3 = st.columns([1.2, 2.5, 1.2])

with col2:
    modo = st.radio("Selecciona los inductores a activar:", ["Inductor Magnético", "Inductor Eléctrico", "Ambos"])
    # Fase animada
    if "phase" not in st.session_state:
        st.session_state.phase = 0.0


# ========================== CONTROLES INDUCTOR 1 ==========================
with col1:
    if modo in ["Inductor Magnético", "Ambos"]:
        st.subheader("🔴 Inductor Magnético")
        x1 = st.slider("Posición X", 0.0, 10.0, 3.0, 0.1, key="x1")
        y1 = st.slider("Posición Y", -4.0, 4.0, 0.0, 0.1, key="y1")
        intensidad1 = st.slider("Intensidad campo", 0.0, 2.0, 1.0, 0.1)
        radio1 = st.slider("Radio de influencia", 1.0, 5.0, 2.0, 0.1)

# ========================== CONTROLES INDUCTOR 2 ==========================
with col3:

    if modo in ["Inductor Eléctrico", "Ambos"]:
        st.subheader("🔵 Inductor Eléctrico")
        x2 = st.slider("Posición X", 0.0, 10.0, 7.0, 0.1, key="x2")
        y2 = st.slider("Posición Y", -4.0, 4.0, 0.0, 0.1, key="y2")
        amp2 = st.slider("Amplitud señal 2", 0.0, 2.0, 1.0, 0.1)
        freq2 = st.slider("Frecuencia señal 2", 0.0, 5.0, 1.0, 0.1)

# ========================== GRAFICO EN EL CENTRO Y CONTROLES GLOBALES ==========================
with col2:
    
    st.subheader("Señal Base")
    amp_base = st.slider("Amplitud", 0.5, 3.0, 1.0)
    freq_base = st.slider("Frecuencia", 0.5, 5.0, 1.0)
    speed = st.slider("Velocidad", 0.01, 0.2, 0.05)

    x = np.linspace(0, 10, 1000)
    plot_area = st.empty()

    for _ in range(10):
        phase = st.session_state.phase
        y = amp_base * np.sin(2 * np.pi * freq_base * x - phase)

        if modo in ["Inductor Magnético", "Ambos"]:
            d1 = np.sqrt((x - x1)**2 + (0 - y1)**2)
            influence1 = intensidad1 * np.exp(-(d1 / radio1)**2)
            y *= (1 + influence1)

        if modo in ["Inductor Eléctrico", "Ambos"]:
            d2 = np.sqrt((x - x2)**2 + (0 - y2)**2)
            influence2 = amp2 * np.exp(-d2 * 3) * np.sin(2 * np.pi * freq2 * x - phase)
            y += influence2

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='cyan', width=3), name='Señal total'))
        fig.add_trace(go.Scatter(x=[0, 10], y=[0, 0], mode='lines', line=dict(color='gray', width=1), name='Cable'))

        if modo in ["Inductor Magnético", "Ambos"]:
            fig.add_trace(go.Scatter(x=[x1], y=[y1], mode='markers',
                                     marker=dict(size=14, color='red'), name='Inductor 1'))

        if modo in ["Inductor Eléctrico", "Ambos"]:
            fig.add_trace(go.Scatter(x=[x2], y=[y2], mode='markers',
                                     marker=dict(size=14, color='blue'), name='Inductor 2'))

        fig.update_layout(
            xaxis=dict(range=[0, 10]),
            yaxis=dict(range=[-5, 5]),
            showlegend=True,
            height=450,
            margin=dict(l=10, r=10, t=10, b=10)
        )

        plot_area.plotly_chart(fig, use_container_width=True)
        st.session_state.phase += speed
        time.sleep(0.05)
