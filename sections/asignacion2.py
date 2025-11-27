import streamlit as st
import numpy as np
from models.sir_model import solve_sir
from utils.plotter import plot_sir_comparison

def show():
    st.header("Asignación 2 – Propagación de un Rumor Académico")
    st.markdown("""
    **Curso:** Derecho Penal I – UNMSM  
    **Rumor:** Cancelación del examen final  
    """)

    st.subheader("Modelo Matemático Adaptado")
    st.latex(r"""
    \frac{dS}{dt} = -b S I \\
    \frac{dI}{dt} = b S I - k I R \\
    \frac{dR}{dt} = k I R
    """)
    st.markdown("""
    - **S(t)**: Alumnos que *no* creen el rumor (susceptibles)  
    - **I(t)**: Alumnos que *creen y propagan* el rumor  
    - **R(t)**: Docentes / alumnos *racionales* que desmienten el rumor  
    - **b**: Tasa de propagación del rumor  
    - **k**: Tasa de "desinfección" por contacto con racionales  
    """)

    st.subheader("Parámetros Interactivos")
    col1, col2 = st.columns(2)
    with col1:
        N = 266 + 8 + 1
        st.write(f"Población total: **{N}** (266 alumnos + 8 docentes + 1 rumorista)")
        I0 = st.slider("Propagadores iniciales (I₀)", 1, 20, 1)
        R0 = st.slider("Racionales iniciales (R₀)", 1, 30, 8)
    with col2:
        b = st.slider("Tasa de propagación (b)", 0.0, 0.01, 0.004, step=0.0005, format="%.4f")
        k = st.slider("Tasa de desinfección (k)", 0.0, 0.1, 0.01, step=0.001, format="%.3f")

    S0 = N - I0 - R0
    t_max = 15

    escenarios = [
        {"k": 0.01, "label": "k = 0.01 (poca persuasión racional)"},
        {"k": 0.02, "label": "k = 0.02 (alta persuasión racional)"}
    ]

    st.subheader("Simulación Comparativa")
    fig, data = plot_sir_comparison(N, I0, R0, b, escenarios, t_max)
    st.pyplot(fig)

    st.subheader("Resumen Cuantitativo (15 días)")
    rows = []
    for d in data:
        pico_dia = d["t"][np.argmax(d["I"])]
        pico_val = int(max(d["I"]))
        creidos = int(N - d["S"][-1])
        pct = f"{creidos / N * 100:.1f}%"
        rows.append([d["label"], pico_val, f"día {pico_dia:.1f}", creidos, pct])
    st.table(rows)

    st.subheader("Interpretación Sociológica")
    st.markdown("""
    - **k = 0.01**: El rumor alcanza a más del **35 %** de los alumnos; los docentes racionales tienen poco efecto.  
    - **k = 0.02**: Solo el **15 %** cree el rumor; la intervención racional es eficaz.  
    - **Conclusión**: Aumentar la **velocidad de respuesta racional** (k) reduce drásticamente la difusión del rumor.
    """)

    st.info("**Factor clave**: En redes pequeñas y cerradas (aula), la **intervención temprana** de pocos racionales puede evitar la saturación del rumor.")