import streamlit as st
import numpy as np
from models.sir_model import solve_sir_extended
from utils.plotter import plot_sir_profesional

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
        <h1>👥 Modelo SIR - Propagación de Sectas</h1>
        <p>Simulación de reclutamiento ideológico en comunidad universitaria</p>
    </div>
    """, unsafe_allow_html=True)

    # Modelo matemático
    st.markdown("""
    <div class="simple-card">
        <h2>📈 Modelo con Inmunización Preventiva</h2>
    """, unsafe_allow_html=True)
    
    st.latex(r"""
    \begin{aligned}
    \frac{dS}{dt} &= -\beta S I - \alpha S \\
    \frac{dI}{dt} &= \beta S I - \gamma I \\
    \frac{dR}{dt} &= \gamma I + \alpha S
    \end{aligned}
    """)
    
    st.markdown("""
    - **S**: Estudiantes vulnerables
    - **I**: Miembros activos de la secta  
    - **R**: Ex-miembros o inmunes
    - **β**: Tasa de reclutamiento
    - **γ**: Tasa de abandono
    - **α**: Tasa de inmunización (vacuna social)
    </div>
    """, unsafe_allow_html=True)

    # Parámetros
    st.markdown("""
    <div class="simple-card">
        <h2>🎚️ Parámetros de Simulación</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        N = st.number_input("Población total", min_value=1000, max_value=20000, value=7138)
        I0 = st.number_input("Miembros iniciales", min_value=1, max_value=100, value=10)
        t_max = st.slider("Días de simulación", 30, 365, 40)
    
    with col2:
        beta = st.slider("Tasa de reclutamiento (β)", 0.00001, 0.001, 0.00014, step=0.00001, format="%.5f")
        gamma = st.slider("Tasa de abandono (γ)", 0.1, 1.0, 0.40, step=0.05)
        alpha = st.slider("Tasa de inmunización (α)", 0.0, 0.2, 0.05, step=0.01)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Simulación
    try:
        S0 = N - I0
        R0 = 0

        S, I, R, t = solve_sir_extended(N, I0, R0, beta, gamma, alpha, t_max)

        # Gráfico
        st.markdown("""
        <div class="simple-card">
            <h2>📊 Evolución de la Secta</h2>
        """, unsafe_allow_html=True)
        
        fig = plot_sir_profesional(S, I, R, t, title="Propagación de sectas en comunidad universitaria")
        st.pyplot(fig)
        
        # Métricas
        pico_dia = t[np.argmax(I)]
        pico_val = int(max(I))
        final_miembros = int(I[-1])
        total_reclutados = N - int(S[-1])
        R0_efectivo = beta * N / (gamma + alpha)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pico de miembros", f"{pico_val}", f"Día {pico_dia:.1f}")
        with col2:
            st.metric("Total reclutados", f"{total_reclutados}")
        with col3:
            st.metric("R₀ efectivo", f"{R0_efectivo:.2f}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Análisis
        st.markdown("""
        <div class="simple-card">
            <h2>💡 Análisis del Reclutamiento</h2>
        """, unsafe_allow_html=True)
        
        umbral = gamma / beta
        st.markdown(f"""
        **Umbral crítico:** Cuando hay menos de **{umbral:.0f}** estudiantes vulnerables, la secta deja de crecer.
        
        **Resultados:**
        - Miembros al final: **{final_miembros}** (la secta {'desaparece' if final_miembros < 10 else 'persiste'})
        - R₀ efectivo: **{R0_efectivo:.2f}** ({'crece' if R0_efectivo > 1 else 'decae'})
        - Efecto de la inmunización: **{alpha/(gamma + alpha)*100:.1f}%** de reducción en el crecimiento
        """)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Conclusión
        st.markdown("""
        <div class="simple-card">
            <h2>🎓 Conclusión</h2>
            <p><strong>La educación crítica (α) es clave:</strong> Invertir en alfabetización ideológica es más efectivo que prohibir la secta.</p>
            <p><strong>Predicción:</strong> La secta crece rápidamente al inicio pero desaparece gracias a la inmunización social y el abandono espontáneo.</p>
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