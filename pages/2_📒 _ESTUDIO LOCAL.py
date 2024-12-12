import streamlit as st
from styles.css_functions import custom_title


st.set_page_config(page_title="Estudio Local", page_icon="📒", layout="wide")

def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("styles/styles.css")

def titulo_imagen(title, image_path):
    
    st.markdown(f"<h2 style='text-align: center;'>{title}</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(image_path, use_column_width=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)

titulo_imagen("Modelo Digital de Elevaciones (MDT)", "data/mdt.png")
titulo_imagen("Hillshade", "data/hillshade.png")
titulo_imagen("Modelo Digital + Hillshade", "data/mdt-hillshade.png")
titulo_imagen("Edificaciones", "data/mdt-parcelario.png")
titulo_imagen("Rios", "data/mdt-rios.png")
titulo_imagen("Situación edificios", "data/parcelario-inundacion.png")
titulo_imagen("Situación carreteras", "data/carreteras.png")
titulo_imagen("Situación ferrocarril", "data/ferrocarril.png")
