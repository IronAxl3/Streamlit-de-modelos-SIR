import streamlit as st
from PIL import Image
import os
import base64

# --- Configuración y Utilidades ---
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

def get_image_base64(image_path):
    """Convierte imagen a base64 para mejor rendimiento"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

def show():
    local_css("style_navy.css")

    # --- 1. SECCIÓN ENCABEZADO ---
    col_text, col_logo = st.columns([3, 1])
    
    with col_text:
        st.markdown(
            """
            <div class="header-container">
                <div class="project-badge">✦ Proyecto Pirata</div>
                <h1 class="main-title">Modelos <span class="title-accent">SIR</span></h1>
                <p class="header-desc">
                    Una aplicación interactiva de la <b class="highlight">Facultad de Ciencias Matemáticas</b> 
                    de la Universidad Nacional Mayor de San Marcos.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    with col_logo:
        logo_paths = ["assets/sanmarcos.jpg", "assets/sanmarcos.jpg"]
        logo_found = False
        for logo_path in logo_paths:
            if os.path.exists(logo_path):
                st.image(logo_path, use_container_width=True)
                logo_found = True
                break
        
        if not logo_found:
            st.markdown('<div class="logo-placeholder">UNMSM</div>', unsafe_allow_html=True)

    # --- 2. SECCIÓN INTEGRANTES CON EFECTOS ESPECIALES ---
    st.markdown('<div class="section-title">🎓 Integrantes del Proyecto</div>', unsafe_allow_html=True)

    integrantes = [
        {
            "nombre": "Iron Axl Ortega Yucra", 
            "rol": "Estudiante FCM", 
            "foto": "assets/yo.jpeg",
            "destacado": True,
            "badge": "🌟 Líder del Proyecto",
            "tipo": "gold"
        },
        {
            "nombre": "Juan Chipana Bellido", 
            "rol": "Estudiante FCM", 
            "foto": "assets/juancook.jpeg",
            "destacado": True,
            "badge": "🚀 Coolider ",
            "tipo": "gold"
        },
        {
            "nombre": "Dylan Lucar Jaimes", 
            "rol": "Estudiante FCM", 
            "foto": "assets/licuar.jpeg",
            "destacado": False,
            "badge": "",
            "tipo": "normal"
        },
        {
            "nombre": "Marcela Ventura Castillo", 
            "rol": "Estudiante FCM", 
            "foto": "assets/marcela.jpeg",
            "destacado": True,
            "badge": "📚 Especialista en LaTeX",
            "tipo": "emerald"
        },
        {
            "nombre": "Jan Mancinelli Vite", 
            "rol": "Estudiante FCM", 
            "foto": "assets/osito.jpeg",
            "destacado": False,
            "badge": "",
            "tipo": "normal"
        },
    ]

    # Grid de integrantes
    cols = st.columns(2)
    for idx, miembro in enumerate(integrantes):
        with cols[idx % 2]:
            if os.path.exists(miembro["foto"]):
                img_base64 = get_image_base64(miembro["foto"])
                if img_base64:
                    if miembro["destacado"] and miembro["tipo"] == "gold":
                        # TARJETA DORADA CON LÁMPARA DE LAVA
                        st.markdown(
                            f"""
                            <div class="member-card-gold">
                                <div class="lava-lamp-animation">
                                    <div class="lava-bubble bubble-1"></div>
                                    <div class="lava-bubble bubble-2"></div>
                                    <div class="lava-bubble bubble-3"></div>
                                    <div class="lava-bubble bubble-4"></div>
                                    <div class="gold-sparkle sparkle-1">✨</div>
                                    <div class="gold-sparkle sparkle-2">✨</div>
                                    <div class="gold-sparkle sparkle-3">✨</div>
                                </div>
                                <div class="member-avatar-gold">
                                    <img src="data:image/jpeg;base64,{img_base64}" alt="{miembro['nombre']}">
                                    <div class="crown"></div>
                                </div>
                                <div class="member-content-gold">
                                    <div class="gold-badge">{miembro['badge']}</div>
                                    <h3 class="member-name-gold">{miembro['nombre']}</h3>
                                    <p class="member-role-gold">{miembro['rol']}</p>
                                    <div class="gold-particles">
                                        <div class="particle"></div>
                                        <div class="particle"></div>
                                        <div class="particle"></div>
                                        <div class="particle"></div>
                                    </div>
                                </div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    elif miembro["destacado"] and miembro["tipo"] == "emerald":
                        # TARJETA ESMERALDA CON LÁMPARA DE LAVA VERDE
                        st.markdown(
                            f"""
                            <div class="member-card-emerald">
                                <div class="emerald-lava-animation">
                                    <div class="emerald-bubble bubble-1"></div>
                                    <div class="emerald-bubble bubble-2"></div>
                                    <div class="emerald-bubble bubble-3"></div>
                                    <div class="emerald-bubble bubble-4"></div>
                                    <div class="emerald-sparkle sparkle-1">💚</div>
                                    <div class="emerald-sparkle sparkle-2">📖</div>
                                    <div class="emerald-sparkle sparkle-3">✨</div>
                                </div>
                                <div class="member-avatar-emerald">
                                    <img src="data:image/jpeg;base64,{img_base64}" alt="{miembro['nombre']}">
                                    <div class="latex-symbol">𝜤</div>
                                </div>
                                <div class="member-content-emerald">
                                    <div class="emerald-badge">{miembro['badge']}</div>
                                    <h3 class="member-name-emerald">{miembro['nombre']}</h3>
                                    <p class="member-role-emerald">{miembro['rol']}</p>
                                    <div class="emerald-particles">
                                        <div class="particle"></div>
                                        <div class="particle"></div>
                                        <div class="particle"></div>
                                        <div class="particle"></div>
                                    </div>
                                </div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    else:
                        # Tarjeta normal
                        st.markdown(
                            f"""
                            <div class="member-card-large">
                                <div class="member-avatar-large">
                                    <img src="data:image/jpeg;base64,{img_base64}" alt="{miembro['nombre']}">
                                </div>
                                <div class="member-content-large">
                                    <h3 class="member-name-large">{miembro['nombre']}</h3>
                                    <p class="member-role-large">{miembro['rol']}</p>
                                </div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )

    # --- 3. SECCIÓN EXPLORAR ---
    st.markdown('<div class="section-title">🔍 ¿Qué podrás explorar?</div>', unsafe_allow_html=True)
    
    col_exp_text, col_exp_img = st.columns([1.5, 1])
    
    with col_exp_text:
        st.markdown("""
            <div class="explore-container">
                <div class="explore-item"><span class="explore-icon">🔬</span><strong>Simular brotes epidémicos</strong> y fenómenos sociales</div>
                <div class="explore-item"><span class="explore-icon">📊</span><strong>Visualizar curvas S-I-R</strong> en tiempo real</div>
                <div class="explore-item"><span class="explore-icon">🎚️</span><strong>Ajustar parámetros</strong> y ver cambios inmediatos</div>
            </div>
        """, unsafe_allow_html=True)

    with col_exp_img:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/SIR_Model.svg/1200px-SIR_Model.svg.png", 
                 use_container_width=True)

    # --- 4. SECCIÓN RESUMEN ---
    st.markdown('<div class="section-title">📚 Modelos en Acción</div>', unsafe_allow_html=True)

    summaries = [
        {"title": "Gripe Porcina", "desc": "Modelo SIR clásico en población estudiantil", "icon": "🦠"},
        {"title": "Rumor Académico", "desc": "Difusión de información con persuasión", "icon": "🗣️"},
        {"title": "Sectas", "desc": "Reclutamiento con inmunización preventiva", "icon": "👥"},
    ]

    cols_summary = st.columns(3)
    for col, item in zip(cols_summary, summaries):
        with col:
            st.markdown(f"""
                <div class="summary-card-elegant">
                    <div class="summary-icon">{item['icon']}</div>
                    <div class="summary-title-elegant">{item['title']}</div>
                    <div class="summary-text-elegant">{item['desc']}</div>
                </div>
            """, unsafe_allow_html=True)

    # --- Footer ---
    st.markdown("""
        <div class="footer-elegant">
            <div class="footer-content">
                <div class="footer-logo">UNMSM</div>
                <div class="footer-info">© 2025 – Universidad Nacional Mayor de San Marcos | Equipo 04</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()