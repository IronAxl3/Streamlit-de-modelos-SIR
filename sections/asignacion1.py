import streamlit as st
import numpy as np
from models.sir_model import solve_sir
from utils.plotter import plot_sir

def local_css(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except:
        pass  # Si falla el CSS, continuar sin estilos

def show():
    local_css("style_navy.css")
    
    # Header simple
    st.markdown("""
    <div class="simple-header">
        <h1>🦠 Modelo SIR - Gripe Porcina</h1>
        <p>Simulación de brote epidémico en población estudiantil UNMSM</p>
    </div>
    """, unsafe_allow_html=True)

    # Modelo matemático
    st.markdown("""
    <div class="simple-card">
        <h2>📈 Modelo Matemático</h2>
    """, unsafe_allow_html=True)
    
    st.latex(r"""
    \begin{aligned}
    \frac{dS}{dt} &= -\beta S I \\
    \frac{dI}{dt} &= \beta S I - k I \\
    \frac{dR}{dt} &= k I
    \end{aligned}
    """)
    
    st.markdown("""
    - **S**: Susceptibles
    - **I**: Infectados  
    - **R**: Recuperados
    - **β**: Tasa de infección
    - **k**: Tasa de recuperación
    </div>
    """, unsafe_allow_html=True)

    # Parámetros - CORREGIDOS
    st.markdown("""
    <div class="simple-card">
        <h2>🎚️ Parámetros de Simulación</h2>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        N = st.number_input("Población total", min_value=100, max_value=20000, value=7138)
        I0 = st.number_input("Infectados iniciales", min_value=1, max_value=100, value=1)
    
    with col2:
        # SLIDER CORREGIDO - rango más amplio y paso más grande
        beta = st.slider(
            "Tasa de infección (β)", 
            min_value=0.000001,    # 1e-6 en lugar de 0
            max_value=0.0005,      # Más amplio
            value=0.00014,         # Valor por defecto más razonable
            step=0.00001,          # Paso más grande
            format="%.6f"
        )
        k = st.slider("Tasa de recuperación (k)", 0.1, 1.0, 0.40, step=0.05)
    
    # Mostrar valores actuales para debug
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
        <strong>Valores actuales:</strong><br>
        β = {beta:.6f} | k = {k:.2f} | Población = {N}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Simulación
    try:
        S0 = N - I0
        R0 = 0
        t_max = 40
        
        S, I, R, t = solve_sir(N, I0, R0, beta, k, t_max)
        
        # Gráfico
        st.markdown("""
        <div class="simple-card">
            <h2>📊 Resultados de la Simulación</h2>
        """, unsafe_allow_html=True)
        
        fig = plot_sir(S, I, R, t)
        st.pyplot(fig)
        
        # Métricas
        pico_dia = t[np.argmax(I)]
        pico_infectados = int(max(I))
        total_infectados = N - int(S[-1])
        R0_valor = beta * N / k
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pico de infectados", f"{pico_infectados}", f"Día {pico_dia:.1f}")
        with col2:
            st.metric("Total infectados", f"{total_infectados}")
        with col3:
            st.metric("R₀ básico", f"{R0_valor:.2f}")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Análisis
        st.markdown("""
        <div class="simple-card">
            <h2>💡 Análisis del Brote</h2>
            <p><strong>R₀ = {:.2f}</strong> - La epidemia {}se propaga</p>
            <p><strong>{:.1f}%</strong> de la población se infecta</p>
            <p>Pico máximo: <strong>{}</strong> infectados simultáneos</p>
        </div>
        """.format(
            R0_valor, 
            "no " if R0_valor <= 1 else "",
            (total_infectados/N*100),
            pico_infectados
        ), unsafe_allow_html=True)
        
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