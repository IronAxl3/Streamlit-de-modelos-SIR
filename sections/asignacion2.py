import streamlit as st
import numpy as np
from models.sir_model import solve_sir
from utils.plotter import plot_sir_comparison

def local_css(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass

def show():
    local_css("style_navy.css")
    
    # Header simple
    st.markdown("""
    <div class="simple-header">
        <h1>🗣️ Modelo SIR - Propagación de Rumores</h1>
        <p>Simulación de rumor académico: "Cancelación del examen final"</p>
    </div>
    """, unsafe_allow_html=True)

    # Modelo matemático
    st.markdown("""
    <div class="simple-card">
        <h2>📈 Modelo Matemático Adaptado</h2>
    """, unsafe_allow_html=True)
    
    st.latex(r"""
    \begin{aligned}
    \frac{dS}{dt} &= -b S I \\
    \frac{dI}{dt} &= b S I - k I R \\
    \frac{dR}{dt} &= k I R
    \end{aligned}
    """)
    
    st.markdown("""
    - **S**: Alumnos que NO creen el rumor
    - **I**: Alumnos que creen y propagan  
    - **R**: Docentes/alumnos racionales que desmienten
    - **b**: Tasa de propagación del rumor
    - **k**: Tasa de "desinfección" por contacto racional
    </div>
    """, unsafe_allow_html=True)

    # Parámetros
    st.markdown("""
    <div class="simple-card">
        <h2>🎚️ Parámetros de Simulación</h2>
    """, unsafe_allow_html=True)
    
    # Población fija
    N = 266 + 8 + 1
    st.markdown(f"**Población total:** {N} personas (266 alumnos + 8 docentes + 1 rumorista)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        I0 = st.slider("Propagadores iniciales (I₀)", 1, 20, 1)
        R0 = st.slider("Racionales iniciales (R₀)", 1, 30, 8)
    
    with col2:
        b = st.slider("Tasa de propagación (b)", 0.0001, 0.01, 0.004, step=0.0005, format="%.4f")
        k = st.slider("Tasa de desinfección (k)", 0.001, 0.1, 0.01, step=0.001, format="%.3f")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Simulación
    try:
        S0 = N - I0 - R0
        t_max = 15

        # Dos escenarios para comparar
        escenarios = [
            {"k": k, "label": f"k = {k:.3f} (persuasión actual)"},
            {"k": k * 2, "label": f"k = {k*2:.3f} (doble persuasión)"}
        ]
        
        # Gráfico
        st.markdown("""
        <div class="simple-card">
            <h2>📊 Comparación de Escenarios</h2>
        """, unsafe_allow_html=True)
        
        fig, data = plot_sir_comparison(N, I0, R0, b, escenarios, t_max)
        st.pyplot(fig)
        
        # Resultados
        st.markdown("""
        <div class="simple-card">
            <h2>📈 Resultados a 15 Días</h2>
        """, unsafe_allow_html=True)
        
        for i, d in enumerate(data):
            pico_dia = d["t"][np.argmax(d["I"])]
            pico_val = int(max(d["I"]))
            total_creyentes = int(N - d["S"][-1])
            porcentaje = (total_creyentes / N) * 100
            
            st.markdown(f"""
            **{d['label']}:**
            - Pico: **{pico_val}** creyentes (día {pico_dia:.1f})
            - Total que creyó: **{total_creyentes}** personas ({porcentaje:.1f}%)
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Análisis
        st.markdown("""
        <div class="simple-card">
            <h2>💡 Interpretación</h2>
            <p><strong>Factor clave:</strong> La velocidad de respuesta racional (k) determina cuántas personas creen el rumor.</p>
            <p><strong>Conclusión:</strong> En redes cerradas como un aula, la intervención temprana de personas racionales puede reducir drásticamente la propagación de rumores.</p>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error en la simulación: {e}")

    # Footer
    st.markdown("""
    <div class="simple-footer">
        <p>Proyecto Pirata • UNMSM • Facultad de Ciencias Matemáticas</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()