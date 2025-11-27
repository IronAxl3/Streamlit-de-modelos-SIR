import streamlit as st
import numpy as np
from models.sir_model import solve_sir
from utils.plotter import plot_sir

def local_css(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"⚠️ No se encontró el archivo de estilos: {file_name}")
    except UnicodeDecodeError:
        try:
            with open(file_name, 'r', encoding='latin-1') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al leer el archivo CSS: {e}")

def show():
    local_css("style_navy.css")
    
    # --- HEADER ELEGANTE ---
    st.markdown("""
    <div class="assignment-header">
        <div class="assignment-badge">🦠 Asignación 1</div>
        <h1 class="assignment-title">Modelo SIR Clásico: <span class="title-accent">Gripe Porcina en San Marcos</span></h1>
        <div class="assignment-subtitle">
            <strong>Universidad Nacional Mayor de San Marcos</strong><br>
            Facultad de Ciencias Matemáticas • Curso: Técnicas de Modelamiento Matemático
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- MODELO MATEMÁTICO CON TARJETA ELEGANTE ---
    st.markdown("""
    <div class="section-card">
        <h2 class="section-title">🔬 Modelo Matemático</h2>
        <div class="equation-container">
            <div class="latex-equation">
    """, unsafe_allow_html=True)
    
    st.latex(r"""
    \begin{aligned}
    \frac{dS}{dt} &= -\beta S I \\
    \frac{dI}{dt} &= \beta S I - k I \\
    \frac{dR}{dt} &= k I
    \end{aligned}
    """)
    
    st.markdown("""
            </div>
            <div class="variables-list">
                <div class="variable-item">
                    <span class="variable-symbol">S(t)</span>
                    <span class="variable-desc">Estudiantes susceptibles</span>
                </div>
                <div class="variable-item">
                    <span class="variable-symbol">I(t)</span>
                    <span class="variable-desc">Estudiantes infectados</span>
                </div>
                <div class="variable-item">
                    <span class="variable-symbol">R(t)</span>
                    <span class="variable-desc">Estudiantes recuperados (inmunes)</span>
                </div>
                <div class="variable-item">
                    <span class="variable-symbol">β</span>
                    <span class="variable-desc">Tasa de infección por contacto</span>
                </div>
                <div class="variable-item">
                    <span class="variable-symbol">k</span>
                    <span class="variable-desc">Tasa de recuperación por día</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- PARÁMETROS CON TARJETA INTERACTIVA ---
    st.markdown("""
    <div class="section-card">
        <h2 class="section-title">🎚️ Parámetros del Modelo</h2>
        <div class="parameters-grid">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        N = st.number_input(
            "👥 Población total (N)", 
            min_value=100, 
            max_value=20000, 
            value=7138,
            help="Población total de estudiantes en la facultad"
        )
        I0 = st.number_input(
            "🦠 Infectados iniciales (I₀)", 
            min_value=1, 
            max_value=100, 
            value=1,
            help="Número inicial de estudiantes infectados"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="parameter-group">', unsafe_allow_html=True)
        beta = st.slider(
            "📈 Tasa de infección (β)", 
            0.0, 0.001, 1/7138, 
            step=1e-6, 
            format="%.6f",
            help="Probabilidad de infección por contacto susceptible-infectado"
        )
        k = st.slider(
            "💊 Tasa de recuperación (k)", 
            0.1, 1.0, 0.40, 
            step=0.01,
            help="Tasa a la que los infectados se recuperan (1/días)"
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

    # --- SIMULACIÓN ---
    S0 = N - I0
    R0_init = 0
    t_max = 40

    try:
        S, I, R, t = solve_sir(N, I0, R0_init, beta, k, t_max)
        
        # --- GRÁFICO MEJORADO ---
        st.markdown("""
        <div class="section-card">
            <h2 class="section-title">📊 Simulación Numérica</h2>
        """, unsafe_allow_html=True)
        
        fig = plot_sir(S, I, R, t)
        st.pyplot(fig)
        st.markdown('</div>', unsafe_allow_html=True)

        # --- ANÁLISIS CON MÉTRICAS ELEGANTES ---
        st.markdown("""
        <div class="section-card">
            <h2 class="section-title">📈 Análisis del Comportamiento</h2>
            <div class="metrics-grid">
        """, unsafe_allow_html=True)
        
        pico_dia = t[np.argmax(I)]
        pico_infectados = int(max(I))
        final_susceptibles = int(S[-1])
        total_infectados = N - final_susceptibles
        R0_valor = beta * N / k
        porcentaje_infectados = (total_infectados / N) * 100

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">📅</div>
                <div class="metric-value">{pico_infectados}</div>
                <div class="metric-label">Pico de Infectados</div>
                <div class="metric-subtitle">Día {pico_dia:.1f}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-icon">🦠</div>
                <div class="metric-value">{total_infectados}</div>
                <div class="metric-label">Total Infectados</div>
                <div class="metric-subtitle">{porcentaje_infectados:.1f}% de la población</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            r0_color = "metric-r0-high" if R0_valor > 1.5 else "metric-r0-medium" if R0_valor > 1 else "metric-r0-low"
            st.markdown(f"""
            <div class="metric-card {r0_color}">
                <div class="metric-icon">🎯</div>
                <div class="metric-value">{R0_valor:.2f}</div>
                <div class="metric-label">R₀ (Número Básico)</div>
                <div class="metric-subtitle">{"Epidemia creciente" if R0_valor > 1 else "Epidemia controlada"}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # --- INTERPRETACIÓN ---
        st.markdown("""
        <div class="insights-container">
            <h3 class="insights-title">💡 Interpretación Epidemiológica</h3>
            <div class="insights-grid">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-icon">❓</div>
                <div class="insight-content">
                    <strong>¿Se infectará toda la población?</strong>
                    <p>No. Cuando <strong>S(t)</strong> cae por debajo de <strong>γ/β ≈ {k/beta:.0f}</strong>, el número reproductivo efectivo cae por debajo de 1 y la epidemia decae.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-icon">🛡️</div>
                <div class="insight-content">
                    <strong>Inmunidad de rebaño</strong>
                    <p>Aproximadamente <strong>{final_susceptibles}</strong> personas ({final_susceptibles/N*100:.1f}%) nunca se infectan debido a la inmunidad colectiva.</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)

        # --- CONCLUSIÓN ---
        st.markdown("""
        <div class="conclusion-card">
            <h3 class="conclusion-title">🎓 Conclusión</h3>
            <div class="conclusion-content">
                <p>El modelo SIR clásico predice que la gripe porcina se propaga rápidamente al inicio, alcanza un pico intermedio y luego decae conforme la población se agota de susceptibles.</p>
                <p>Aunque <strong>R₀ = {R0_valor:.2f} {'>' if R0_valor > 1 else '<'} 1</strong>, la infección <strong>no alcanza al 100%</strong> de la población, lo cual es consistente con brotes reales donde la inmunidad de rebaño limita la propagación.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error en la simulación: {e}")
        st.info("Por favor, ajusta los parámetros y vuelve a intentar.")

    # --- FOOTER ---
    st.markdown("""
    <div class="assignment-footer">
        <div class="footer-content">
            <strong>Proyecto Pirata</strong> • Modelos SIR • Facultad de Ciencias Matemáticas UNMSM
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()