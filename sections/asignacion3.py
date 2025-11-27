import streamlit as st
import numpy as np
from models.sir_model import solve_sir_extended
from utils.plotter import plot_sir_profesional

def show():
    st.header("Asignación 3 – Infecciones Ideológicas: Propagación de Sectas")
    st.markdown("""
    **Universidad Nacional Mayor de San Marcos**  
    Facultad de Ciencias Matemáticas  
    Curso: Técnicas de Modelamiento Matemático  
    """)

    st.subheader("Modelo SIR Extendido con Inmunización Preventiva")
    st.latex(r"""
    \frac{dS}{dt} = -\beta S I - \alpha S \\
    \frac{dI}{dt} = \beta S I - \gamma I \\
    \frac{dR}{dt} = \gamma I + \alpha S
    """)

    st.markdown("""
    - **S(t)**: Estudiantes vulnerables (susceptibles)  
    - **I(t)**: Miembros activos de la secta  
    - **R(t)**: Ex-miembros o inmunes (resistencia crítica)  
    - **β**: Tasa de reclutamiento ideológico  
    - **γ**: Tasa de abandono espontáneo  
    - **α**: Tasa de inmunización psicológica (vacuna social)  
    """)

    st.subheader("Parámetros Interactivos")
    col1, col2, col3 = st.columns(3)
    with col1:
        N = st.number_input("Población total (N)", min_value=1000, max_value=20000, value=7138)
        I0 = st.number_input("Miembros iniciales (I₀)", min_value=1, max_value=100, value=10)
    with col2:
        beta = st.slider("β (reclutamiento)", 0.0, 0.001, 1/7138, step=1e-6, format="%.6f")
        gamma = st.slider("γ (abandono)", 0.1, 1.0, 0.40, step=0.01)
    with col3:
        alpha = st.slider("α (inmunización)", 0.0, 0.2, 0.05, step=0.01)
        t_max = st.slider("Días de simulación", 30, 365, 40, step=5)

    S0 = N - I0
    R0 = 0

    S, I, R, t = solve_sir_extended(N, I0, R0, beta, gamma, alpha, t_max)

    st.subheader("Simulación Numérica")
    fig = plot_sir_profesional(S, I, R, t, title="Propagación de sectas en comunidad universitaria")
    st.pyplot(fig)

    st.subheader("Análisis del Comportamiento")
    pico_dia = t[np.argmax(I)]
    pico_val = int(max(I))
    final_infectados = int(I[-1])
    total_infectados = N - int(S[-1])
    R0_efectivo = beta * N / (gamma + alpha)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pico de miembros", f"{pico_val}", f"Día {pico_dia:.1f}")
    with col2:
        st.metric("Total reclutados", f"{total_infectados}")
    with col3:
        st.metric("R₀ efectivo", f"{R0_efectivo:.2f}")

    umbral = gamma / beta
    st.info(f"**Umbral crítico**: Cuando **S(t) < {umbral:.0f}**, la secta deja de crecer.")

    st.markdown(f"""
    - **¿Se apoderará la secta de toda la universidad?** No.  
    - **¿Por qué?** Porque cuando **S(t) < γ/β ≈ {umbral:.0f}**, el reclutamiento ya no supera el abandono.
    - **Miembros al final**: ≈ {final_infectados} (la secta desaparece).
    """)

    st.subheader("Conclusión Sociológica")
    st.markdown("""
    El modelo predice que la secta **crece rápidamente al inicio**, pero **desaparece al año** gracias a:
    - **Educación crítica** (α > 0)
    - **Abandono espontáneo** (γ > 0)
    - **Agotamiento del pool vulnerable**

    **Política pública**: Invertir en **alfabetización ideológica** (aumentar α) es más efectivo que prohibir la secta.
    """)