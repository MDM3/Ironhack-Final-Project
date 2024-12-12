import streamlit as st

def custom_title(text, size="2.5em", text_align="center", margin_left=None, margin_right=None,margin_top=None):
    """
    Genera un título con estilos personalizados en Streamlit.
    
    Parámetros:
    - text (str): El texto del título.
    - size (str): Tamaño del texto (por defecto "2.5em").
    - text_align (str): Alineación del texto (por defecto "center").
    - margin_left (str): Margen izquierdo opcional (ejemplo: "10px").
    - margin_right (str): Margen derecho opcional (ejemplo: "10px").
    """
    # Crear dinámicamente el CSS
    margins = ""
    if margin_left:
        margins += f"margin-left: {margin_left};"
    if margin_right:
        margins += f"margin-right: {margin_right};"
    
    # Generar el bloque de estilo
    st.markdown(
        f"""
        <style>
        .custom-title {{
            text-align: {text_align};
            font-size: {size};
            font-weight: bold;
            {margins}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Insertar el título
    st.markdown(f'<div class="custom-title">{text}</div>', unsafe_allow_html=True)
