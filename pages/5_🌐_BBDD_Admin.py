import streamlit as st
import pandas as pd
import pymysql
from styles.css_functions import custom_title

st.set_page_config(page_title="SQL", page_icon="🌐", layout="wide")

css = """
[data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"] span:last-child {
    font-size: 18px !important;
}
"""

st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


# Imagen en la cabecera del sidebar
st.sidebar.image(
    "https://img.icons8.com/color/144/mysql-logo.png",
    use_column_width=True
)

# Conexión a la base de datos MySQL usando PyMySQL
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',        
        user='root',             
        password='admin',        
        database='geodatabase',  
        cursorclass=pymysql.cursors.DictCursor  
    )
    return connection

# Función para ejecutar una consulta SQL y devolver los resultados como un DataFrame
def run_query(query):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query)  # Ejecuta la consulta SQL
            result = cursor.fetchall()  # Obtiene todos los resultados
            column_names = [desc[0] for desc in cursor.description]  # Obtiene los nombres de las columnas
        connection.close()
        return pd.DataFrame(result, columns=column_names)  # Devuelve los resultados como un DataFrame de pandas
    except pymysql.MySQLError as err:
        st.error(f"Error de SQL: {err}")
        return None

# Función de la página "Consultas"
def pagina_consultas():

    # Título principal de la página
    custom_title(
        text="Consultas SQL",
        size="3em",
        text_align="center",
        margin_left="20px",
        margin_right="20px"
    )

    # Área de texto para que el usuario ingrese una consulta SQL
    query = st.text_area("Escribe tu consulta SQL", 
        value="SELECT * FROM df_buildings LIMIT 10;", height=100)
    
    # Botón para ejecutar la consulta
    if st.button("Ejecutar consulta"):
        if query.strip() != "":
            # Validar si la consulta contiene palabras clave peligrosas
            if any(keyword in query.upper() for keyword in ["DROP", "DELETE", "UPDATE", "TRUNCATE"]):
                st.error("Esta aplicación no permite consultas que modifiquen datos (DROP, DELETE, etc.).")
            else:
                # Ejecutar la consulta
                result_df = run_query(query)

                if result_df is not None and not result_df.empty:
                    st.write("### Resultados de la consulta")
                    st.dataframe(result_df, use_container_width=True)
                    st.write(f"Resultados: {result_df.shape[0]} filas y {result_df.shape[1]} columnas.")
                else:
                    st.write("No se encontraron resultados o la consulta es incorrecta.")
        else:
            st.write("Por favor, ingresa una consulta SQL.")

# Lógica para el inicio de sesión
PASSWORD = "admin"  # Contraseña de acceso

def login_protector():
    if "access_granted" not in st.session_state:
        st.session_state.access_granted = False

    if not st.session_state.access_granted:
        # Simulación de un pop-up
        with st.form("login_form"):
            st.subheader("Acceso restringido")
            st.write("Ponte en contacto con tu supervisor.")
            password_input = st.text_input("Introduce la contraseña:", type="password")
            submit_button = st.form_submit_button("Entrar")

            if submit_button:
                if password_input == PASSWORD:
                    st.session_state.access_granted = True
                    st.success("¡Acceso concedido!")
                else:
                    st.error("Contraseña incorrecta.")
        return False
    return True

# Llamar a la función protegida
if __name__ == "__main__":
    if login_protector():
        pagina_consultas()
