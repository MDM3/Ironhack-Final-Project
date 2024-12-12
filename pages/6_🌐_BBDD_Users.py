import streamlit as st
import pandas as pd
import pymysql
from styles.css_functions import custom_title

st.set_page_config(page_title="SQL Predefinido", page_icon="🌐", layout="wide")

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
        cursorclass=pymysql.cursors.DictCursor  # Para devolver los resultados como diccionarios
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

# Página con botones predefinidos
def pagina_consultas_predefinidas():
    # Título principal de la página
    custom_title(
        text="Consultas Predefinidas",
        size="3em",
        text_align="center",
        margin_left="20px",
        margin_right="20px"
    )

    
    st.markdown(
    """
    <p style="font-size: 1.5em; text-align: left; margin-top: 20px;">
        Seleccione una de las consultas predefinidas a continuación:
    </p>
    """,
    unsafe_allow_html=True,
)
    

    
    st.markdown("<br>",unsafe_allow_html=True )
    # Consulta 1: Mostrar las primeras 10 filas de 'df_buildings'
    if st.button("Los 5 rios con mayor distancia promedio de edificios ubicados cerca de ellos."):
        query = """SELECT nom_rio AS River_Name, AVG(distance) AS Average_Distance
        FROM df_buildings
        WHERE distance > 0
        GROUP BY nom_rio
        ORDER BY Average_Distance DESC
        LIMIT 5;"""
        result_df = run_query(query)
        if result_df is not None and not result_df.empty:
            st.write("### Resultados de la consulta")
            st.dataframe(result_df, use_container_width=True)

    # Consulta 2: Contar el total de registros en 'df_buildings'
    if st.button("Area media de edificios por municipio"):
        query = """
        SELECT layer AS Municipality, AVG(area) AS Average_Area 
        FROM df_buildings 
        GROUP BY layer 
        ORDER BY Average_Area DESC;"""

        result_df = run_query(query)
        if result_df is not None and not result_df.empty:
            st.write("### Resultados de la consulta")
            st.dataframe(result_df, use_container_width=True)

    # Consulta 3: Mostrar los edificios más altos
    if st.button("Area total de edificios con una distancia de hasta 500m, por rio."):
        query = """
        SELECT nom_rio AS River_Name, SUM(area) AS Total_Area
        FROM df_buildings
        WHERE distance <= 500
        GROUP BY nom_rio
        ORDER BY Total_Area DESC;
        """
        result_df = run_query(query)
        if result_df is not None and not result_df.empty:
            st.write("### Resultados de la consulta")
            st.dataframe(result_df, use_container_width=True)

    # Consulta 4: Contar registros por categoría
    if st.button("Los 10 municipios con el mayor numero de parcelas por rio"):
        query = """
        SELECT layer AS Municipality, nom_rio AS River_Name, COUNT(parcela) AS Parcels_Count
        FROM df_buildings
        GROUP BY layer, nom_rio
        ORDER BY Parcels_Count DESC
        LIMIT 10;
        """
        result_df = run_query(query)
        if result_df is not None and not result_df.empty:
            st.write("### Resultados de la consulta")
            st.dataframe(result_df, use_container_width=True)

        # Consulta 4: Contar registros por categoría
    if st.button("Numero total de edificios afectados y no afectados por municipio"):
        query = """
        SELECT layer AS Municipality, nom_rio AS River_Name, COUNT(parcela) AS Parcels_Count
        FROM df_buildings
        GROUP BY layer, nom_rio
        ORDER BY Parcels_Count DESC
        LIMIT 10;
        """
        result_df = run_query(query)
        if result_df is not None and not result_df.empty:
            st.write("### Resultados de la consulta")
            st.dataframe(result_df, use_container_width=True)

# Ejecutar la página sin login
if __name__ == "__main__":
    pagina_consultas_predefinidas()
