import streamlit as st
from styles.css_functions import custom_title

st.set_page_config(page_title="Plataforma de Evaluación de Impacto Ambiental", page_icon="🌍", layout="wide")

# PERSONALIZACION CON CSS DEL SIDEBAR
custom_css = """
    <style>
    /* Sidebar Buttons */
    .button-container {
        display: flex;
        gap: 15px;
        margin-top: 5px;
    }

    .social-button {
        display: flex;
        align-items: center;
        padding: 0.4rem 1rem;
        font-size: 18px;
        color: white;
        background-color:  #24292e; /* GitHub Dark */
        border: none;
        border-radius: 5px;
        text-decoration: none;
        cursor: pointer;
        text-align: left;
        transition: background-color 0.3s ease;
    }

    .social-button img {
        width: 32px;
        height: 32px;
        margin-right: 10px;
    }

    .github-button:hover {
        background-color: #444;
    }

    .linkedin-button:hover {
        background-color: #005582;
    }

    /* Form Styles */
    .form-container {
        width: 100%;
        background: linear-gradient(#212121, #212121) padding-box,
                    linear-gradient(145deg, transparent 35%,#e81cff, #40c9ff) border-box;
        border: 2px solid transparent;
        padding: 32px 24px;
        font-size: 14px;
        font-family: inherit;
        color: white;
        display: flex;
        flex-direction: column;
        gap: 20px;
        box-sizing: border-box;
        border-radius: 16px;
        margin-top: 30px;
    }

    .form-container .form-group {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .form-container .form-group label {
        color: #717171;
        font-weight: 600;
        font-size: 12px;
    }

    .form-container .form-group input,
    .form-container .form-group textarea {
        width: 100%;
        padding: 12px 16px;
        border-radius: 8px;
        color: #fff;
        font-family: inherit;
        background-color: transparent;
        border: 1px solid #414141;
    }

    .form-container .form-group input:focus,
    .form-container .form-group textarea:focus {
        outline: none;
        border-color: #e81cff;
    }

    .form-container .form-submit-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        color: #717171;
        font-weight: 600;
        width: 100%;
        background: #313131;
        border: 1px solid #414141;
        padding: 12px 16px;
        font-size: inherit;
        border-radius: 6px;
        cursor: pointer;
    }

    .form-container .form-submit-btn:hover {
        background-color: #fff;
        border-color: #fff;
        color: #000;
    }
    </style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# CONTENIDO SIDEBAR
st.sidebar.header("Redes sociales")

# BOTONES REDES SOCIALES
button_html = """
    <div class="button-container">
        <a href="https://github.com/MDM3" target="_blank" class="social-button github-button">
            <img src="https://img.icons8.com/nolan/64/github.png" alt="GitHub Logo"/>
            GitHub
        </a>
        <a href="https://www.linkedin.com/in/marcos-duran-marquez-6a4b23234/" target="_blank" class="social-button linkedin-button">
            <img src="https://img.icons8.com/doodle/64/linkedin--v2.png" alt="LinkedIn Logo"/>
            LinkedIn
        </a>
    </div>
"""
st.sidebar.markdown(button_html, unsafe_allow_html=True)

# Form Section
form_html = """
    <div class="form-container">
        <form>
            <div class="form-group">
                <label for="name">Nombre</label>
                <input type="text" id="name" placeholder="Tu nombre aquí">
            </div>
            <div class="form-group">
                <label for="email">Correo Electrónico</label>
                <input type="email" id="email" placeholder="Tu correo electrónico">
            </div>
            <div class="form-group">
                <label for="message">Mensaje</label>
                <textarea id="message" placeholder="Escribe tu mensaje aquí"></textarea>
            </div>
            <button type="submit" class="form-submit-btn">Enviar</button>
        </form>
    </div>
"""
st.sidebar.markdown(form_html, unsafe_allow_html=True)

# CONTENIDO PRINCIPAL
col1, col2 = st.columns([1, 5])
with col1:
    st.image("data/logo.png", width=250)

with col2:
    custom_title(
        text="Plataforma de Evaluación de Impactos<br> Medio Ambientales",
        size="3.5em",
        text_align="center",
        margin_left="0px",
        margin_right="120px",
    )

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
    <p style="font-size: 2.25em; text-align: center; margin-top: 20px;">
        Bienvenido a la plataforma diseñada para evaluar y visualizar el impacto ambiental ante catástrofes. 
        Descubre herramientas interactivas para el análisis y toma de decisiones basadas en datos.
    </p>
    """,
    unsafe_allow_html=True,
)


st.markdown("<br>", unsafe_allow_html=True)

# Contenedores creados con CSS para el manejo. Ademas se implementa un estilo visual para el paso del raton.
st.markdown(
    """
    <!-- Contenedor centrado para el título -->
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
        <div style="display: inline-block; background-color: #154360; padding: 10px 20px; border-radius: 15px;">
            <h2 style="text-align: center; font-size: 2.5em; color: white; margin: 0;">
                Objetivos de la Plataforma
            </h2>
        </div>
    </div><br><br>

    <!-- Párrafos centrados debajo del título -->
    <div style="text-align: center; margin-top: 30px;">
        <div style="margin-bottom: 30px;">
            <h3 style="font-size: 2em; color: white; margin: 0; padding: 10px; transition: background-color 0.3s ease; border-radius: 15px;">
                Visualización
            </h3>
            <p style="font-size: 1.5em; line-height: 1.8; margin: 10px 0; color: white;">
                Proporcionar visualizaciones interactivas para monitorear las áreas afectadas por catástrofes.
            </p>
        </div>
        <div style="margin-bottom: 30px;">
            <h3 style="font-size: 2em; color: white; margin: 0; padding: 10px; transition: background-color 0.3s ease; border-radius: 15px;">
                Análisis de Datos
            </h3>
            <p style="font-size: 1.5em; line-height: 1.8; margin: 10px 0; color: white;">
                Facilitar el análisis de datos espaciales y ambientales para identificar patrones y tendencias.
            </p>
        </div>
        <div style="margin-bottom: 30px;">
            <h3 style="font-size: 2em; color: white; margin: 0; padding: 10px; transition: background-color 0.3s ease; border-radius: 15px;">
                Evaluación de Impactos
            </h3>
            <p style="font-size: 1.5em; line-height: 1.8; margin: 10px 0; color: white;">
                Estimar los daños a infraestructuras, ecosistemas y comunidades locales.
            </p>
        </div>
        <div style="margin-bottom: 30px;">
            <h3 style="font-size: 2em; color: white; margin: 0; padding: 10px; transition: background-color 0.3s ease; border-radius: 15px;">
                Toma de Decisiones
            </h3>
            <p style="font-size: 1.5em; line-height: 1.8; margin: 10px 0; color: white;">
                Ayudar a los responsables de la toma de decisiones a priorizar acciones y recursos.
            </p>
        </div>
        <div style="margin-bottom: 30px;">
            <h3 style="font-size: 2em; color: white; margin: 0; padding: 10px; transition: background-color 0.3s ease; border-radius: 15px;">
                Prevención
            </h3>
            <p style="font-size: 1.5em; line-height: 1.8; margin: 10px 0; color: white;">
                Ofrecer información clave para mitigar riesgos futuros y fortalecer la resiliencia ambiental.
            </p>
        </div>
    </div>

    <!-- CSS para efecto hover -->
    <style>
        h3:hover {
            background-color: #154360; /* Color del fondo */
        }
    </style>
    """,
    unsafe_allow_html=True
)

