import streamlit as st
import geopandas as gpd
import pydeck as pdk
from shapely.geometry import Polygon, MultiPolygon
from styles.css_functions import custom_title

st.set_page_config(page_title="Roads", page_icon="🛣️", layout="wide")

def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llama la función para cargar el CSS
load_css("styles/styles.css")

shapefile_path = r"C:\\Users\\Darkos\\Desktop\\Labs\\Final_project\\Data\\Shapefiles\\carreteras_dist_5.shp"
gdf = gpd.read_file(shapefile_path)

# Verifico que el CRS esta definido correctamente
if gdf.crs is None or gdf.crs.to_string() != "EPSG:25830":
    gdf = gdf.set_crs("EPSG:25830")

# Transformo al CRS estándar (WGS84 - EPSG:4326)
gdf = gdf.to_crs(epsg=4326)

# Verifico geometrías válidas
gdf = gdf[gdf.is_valid]

# Calculo el centroide para centrar el mapa
centroid = gdf.geometry.centroid.unary_union
if centroid.geom_type == "MultiPoint":
    centroid = list(centroid.geoms)[0]  # Tomar el primer punto del MultiPoint
elif centroid.geom_type == "Point":
    pass  
else:
    raise ValueError("No se pudo calcular un centroide válido.")

map_center = [centroid.y, centroid.x]

#Funcion que controla el estilo del titulo
custom_title(
    text="Vías afectadas por la DANA",
    size="3em",
    text_align="center",
    margin_left="20px",
    margin_right="20px"
)

# Selector de filtros por 'clased'
clased_options = ["Todas"] + sorted(gdf["clased"].unique())
selected_clased = st.sidebar.selectbox("Tipo de via:", clased_options)

# Filtrar los datos según la selección
if selected_clased != "Todas":
    filtered_gdf = gdf[gdf["clased"] == selected_clased]
else:
    filtered_gdf = gdf

# Selector de filtros anidados por 'rio'
rio_options = ["Todos"] + sorted(filtered_gdf["nom_rio"].unique())
selected_rio = st.sidebar.selectbox("Filtrar por Río:", rio_options)

# Filtrar según el río seleccionado
if selected_rio != "Todos":
    filtered_gdf = filtered_gdf[filtered_gdf["nom_rio"] == selected_rio]

# Recalcular el centroide basado en los filtros actuales
if not filtered_gdf.empty:
    filtered_centroid = filtered_gdf.geometry.unary_union.centroid
    map_center = [filtered_centroid.y, filtered_centroid.x]
else:
    map_center = [centroid.y, centroid.x]  # Volver al centro inicial si no hay datos

# Función para convertir geometrias a formato pydeck
def geometry_to_pydeck_polygon(geom):
    if geom.geom_type == 'LineString':
        return [list(coord) for coord in geom.coords]
    elif geom.geom_type == 'MultiLineString':
        return [list(coord) for coord in list(geom)[0].coords]
    elif geom.geom_type == 'Polygon':
        return [list(coord) for coord in geom.exterior.coords]
    elif geom.geom_type == 'MultiPolygon':
        return [list(coord) for coord in list(geom)[0].exterior.coords]
    else:
        return None

# Convertir las geometrias a formato pydeck
filtered_gdf["pydeck_geometry"] = filtered_gdf.geometry.apply(geometry_to_pydeck_polygon)

# Crear una capa para PyDeck
layer = pdk.Layer(
    "PathLayer",  # Usamos PathLayer para líneas
    data=filtered_gdf,
    get_path="pydeck_geometry",
    get_color=[255, 0, 0, 100],  # Color rojo
    width_scale=1,
    width_min_pixels=1,
    get_line_width=0.5,
    pickable=True,
)

# Configuración del mapa
view_state = pdk.ViewState(
    latitude=map_center[0],
    longitude=map_center[1],
    zoom=12 if selected_clased != "Todas" or selected_rio != "Todos" else 10,
    pitch=0,
)

# Mapa de PyDeck con base satelital
r = pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v11",
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>Carretera</b><br> <b>Calle: </b> {nombre} <br><b>Tipo de via: </b> {clased}<br><b>Longitud de via: </b> {length} m",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }
)

# Mostrar el mapa en Streamlit
st.pydeck_chart(r)


# Espacio entre el mapa y los contenedores
st.markdown("<br><br>", unsafe_allow_html=True)

# Contenedores para mostrar resultados
col1, col2 = st.columns(2)

# Calcular y mostrar la suma de la longitud y la distancia media
total_length_km = filtered_gdf.geometry.length.sum() * 1000  # Convertir a km
distance_mean = filtered_gdf["distance_2"].mean()


with col1:
    st.markdown(
        f"""<div style='font-size: 2em; text-align: center;'><b>Longitud total (km)</b><br>
        <span style='font-size: 2.5em;background-color: #154360; border-radius: 15px; padding: 8px;'>{total_length_km:,.2f}</span></div>""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""<div style='font-size: 2em; text-align: center;'><b>Distancia media a ríos (m)</b><br>
        <span style='font-size: 2.5em;background-color: #154360; border-radius: 15px; padding: 8px;'>{distance_mean:,.2f}</span></div>""",
        unsafe_allow_html=True,
    )
