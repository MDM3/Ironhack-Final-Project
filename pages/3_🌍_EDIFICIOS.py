import streamlit as st
import geopandas as gpd
import pandas as pd
import pydeck as pdk
import altair as alt
from shapely.geometry import Polygon, MultiPolygon
from styles.css_functions import custom_title



# Configuración de la página
st.set_page_config(page_title="Interactive Map and Chart", page_icon="🌍", layout="wide")

custom_title(
    text="Mapa interactivo e histogramas",
    size="3em",
    text_align="center"
)

# Estilo CSS personalizado para la barra lateral
css = """
[data-testid="stSidebarNav"] a[data-testid="stSidebarNavLink"] span:last-child {
    font-size: 18px !important;
}
"""
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.sidebar.markdown("## Layers")

# Ruta del shapefile
shapefile_path = r"C:\\Users\\Darkos\\Desktop\\Labs\\Final_project\\Data\\Shapefiles\\parcelario_compress.shp"

# Función para cargar y procesar el shapefile

@st.cache_data
def load_shapefile(path):
    gdf = gpd.read_file(path)


    # Asegurar que el CRS esté definido correctamente
    if gdf.crs is None or gdf.crs.to_string() != "EPSG:25830":
        gdf = gdf.set_crs("EPSG:25830")
    # Calcular el área en metros cuadrados antes de transformar
    gdf['area_m2'] = gdf.geometry.area
    # Transformar al CRS estándar (WGS84 - EPSG:4326)
    gdf = gdf.to_crs(epsg=4326)
    # Verificar geometrías válidas
    gdf = gdf[gdf.is_valid]
    # Normalizar valores de 'estado'
    gdf['estado'] = gdf['estado'].fillna('Desconocido').str.strip().str.lower()
    # Normalizar nombres de ríos y municipios
    gdf['nom_rio'] = gdf['nom_rio'].fillna('Desconocido').str.strip().str.lower()
    gdf['nom_muni'] = gdf['nom_muni'].fillna('Desconocido').str.strip().str.lower()
    return gdf

gdf = load_shapefile(shapefile_path)


# Selección de municipio
municipio_options = gdf['nom_muni'].unique()
municipio_options_sorted = sorted(municipio_options)
municipio_filter = st.selectbox("Selecciona un municipio:", municipio_options_sorted)
gdf_filtrado = gdf[gdf['nom_muni'] == municipio_filter]

st.subheader(f'Municipio: {municipio_filter.title()}')

def geometry_to_pydeck_polygon(geom):
    """
    Convierte geometrías de GeoPandas a listas de coordenadas para Pydeck.
    """
    if geom.geom_type == 'LineString':
        return [list(coord) for coord in geom.coords]
    elif geom.geom_type == 'MultiLineString':
        # Combina todas las LineStrings en una lista de coordenadas
        return [list(coord) for geom_part in geom for coord in geom_part.coords]
    elif geom.geom_type == 'Polygon':
        return [list(coord) for coord in geom.exterior.coords]
    elif geom.geom_type == 'MultiPolygon':
        # Combina todas las Polygons en una lista de coordenadas
        return [list(coord) for poly in geom for coord in poly.exterior.coords]
    else:
        return None

def get_color(estado):
    """
    Asigna colores basados en el estado.
    """
    if estado == "affected":
        return [255, 125, 0, 150]  # Naranja
    elif estado == "not affected":
        return [0, 0, 255, 100]    # Azul
    else:
        return [128, 128, 128, 100]  # Gris

if not gdf_filtrado.empty:
    # Crear dataframe para pydeck
    data = []
    for _, row in gdf_filtrado.iterrows():
        coords = geometry_to_pydeck_polygon(row['geometry'])
        if coords:
            data.append({
                "polygon": coords,
                "estado": row['estado'],
                "refcat": row['refcat'],
                "distancia": row['distance'],
                "color": get_color(row['estado'])
            })
    df_pydeck = pd.DataFrame(data)

    # Asegurar que no hay columna 'geometry'
    if 'geometry' in df_pydeck.columns:
        df_pydeck = df_pydeck.drop(columns=['geometry'])

    # Calcular el centro del mapa
    bounds = gdf_filtrado.total_bounds  # [minx, miny, maxx, maxy]
    center_lat = (bounds[1] + bounds[3]) / 2
    center_lon = (bounds[0] + bounds[2]) / 2

    # Definir capa de polígonos
    polygon_layer = pdk.Layer(
        "PolygonLayer",
        data=df_pydeck,
        get_polygon="polygon",
        get_fill_color="color",
        get_line_color=[255, 255, 255],
        get_line_width=0.25,
        pickable=True,
        extruded=False
    )

    # Selección de capas en la barra lateral
    layers_to_show = st.sidebar.multiselect("Capas a mostrar", ["Parcelas"], default=["Parcelas"])

    # Controla la leyenda
    st.sidebar.markdown("""
<div style="
  background-color: #0E1117; 
  padding: 10px;
  border-radius: 5px;
  font-size: 14px;
  line-height: 1.5;
  color: white;
  margin-top: 10px;">

  <div style="font-weight: bold; margin-bottom: 8px;">Leyenda</div>

  <div style="display: flex; align-items: center; margin-bottom: 5px;">
    <div style="width: 15px; height: 15px; background: rgba(255,165,0,0.5); margin-right: 8px; border: 1px solid #ccc;"></div>
    Afectado
  </div>

  <div style="display: flex; align-items: center; margin-bottom: 5px;">
    <div style="width: 15px; height: 15px; background: rgba(0,0,255,0.5); margin-right: 8px; border: 1px solid #ccc;"></div>
    No afectado
  </div>

</div>
""", unsafe_allow_html=True)

    layers = []
    if "Parcelas" in layers_to_show:
        layers.append(polygon_layer)

    # Crear la vista inicial
    view_state = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=12)

    # Crear el objeto Deck
    r = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/satellite-streets-v11',
        tooltip={
            "html": "<b>Referencia Catastral:</b> {refcat}<br><b>Distancia:</b> {distancia} m<br><b>Estado:</b> {estado}",
            "style": {"backgroundColor": "steelblue", "color": "white"}
        }
    )

    # Mostrar el mapa
    st.pydeck_chart(r)

    st.markdown("<br><br>", unsafe_allow_html=True)

## MARCADORES 

    # Contenedores para mostrar resultados
    col1, col2 = st.columns(2)

    # Calcular métricas
    # 1. Área media (m²)
    if not gdf_filtrado.empty:
        area_mean = int(round(gdf_filtrado['area_m2'].mean()))
    else:
        area_mean = 0

    # 2. Distancia media a ríos de los edificios (m)

    # Ruta del archivo CSV de edificios
    file_path = r"C:\\Users\\Darkos\\Desktop\\Labs\\Final_project\\df_buildings.csv"

    # Función para cargar el CSV
    @st.cache_data
    def load_csv(path):
        return pd.read_csv(path)

    try:
        df_buildings = load_csv(file_path)

        # Filtrar edificios por municipio seleccionado
        df_buildings_filtered = df_buildings[df_buildings['nom_muni'].str.lower() == municipio_filter.lower()]

        # Calcular la distancia media a ríos de los edificios
        if not df_buildings_filtered.empty:
            distance_mean = int(round(df_buildings_filtered["distance"].mean()))
        else:
            distance_mean = 0

        # Mostrar las métricas en los contenedores
        with col1:
            st.markdown(
                f"""<div style='font-size: 2em; text-align: center;'><b>Área media (m²)</b><br>
                <span style='font-size: 2.5em;background-color: #154360; border-radius: 15px; padding: 8px;'>{area_mean:,}</span></div>""",
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""<div style='font-size: 2em; text-align: center;margin-left:-300px'><b>Distancia media a ríos de los edificios (m)</b><br>
                <span style='font-size: 2.5em;background-color: #154360; border-radius: 15px; padding: 8px;'>{distance_mean:,}</span></div>""",
                unsafe_allow_html=True,
            )

        st.markdown("<br><br>", unsafe_allow_html=True)



        ##BUBBLE CHART 


        # Filtrar solo las áreas afectadas
        df_affected = df_buildings[df_buildings['estado'].str.lower() == 'affected']

        if df_affected.empty:
            st.error("No hay datos con estado 'Affected' en el archivo proporcionado.")
        else:
            # Calcular el área total afectada por municipio
            df_affected_area = df_affected.groupby('nom_muni')['area'].sum().reset_index()
            df_affected_area.rename(columns={'area': 'affected_area'}, inplace=True)

            # Calcular el área total afectada
            total_affected_area = df_affected_area['affected_area'].sum()

            # Calcular la proporción de área afectada por municipio
            if total_affected_area > 0:
                df_affected_area['proportion_affected'] = (df_affected_area['affected_area'] / total_affected_area) * 100
            else:
                df_affected_area['proportion_affected'] = 0

            df_affected_area.fillna(0, inplace=True)

            # Convertir 'nom_muni' a título para mejor presentación
            df_affected_area['nom_muni'] = df_affected_area['nom_muni'].str.title()

            # Crear un Bubble Chart
            bubble_chart = alt.Chart(df_affected_area).mark_circle(size=400).encode(
                x=alt.X(
                    'nom_muni:N',
                    title='Municipio',
                    sort='-y',
                    axis=alt.Axis(
                        labelFontSize=18,  # Tamaño de las etiquetas de los municipios
                        titleFontSize=25   # Tamaño del título del eje X
                    )
                ),
                y=alt.Y(
                    'proportion_affected:Q',
                    title='Proporción del Área Afectada (%)',
                    axis=alt.Axis(titleFontSize=22, labelFontSize=20)  # Etiquetas y títulos más grandes
                ),
                size=alt.Size(
                    'affected_area:Q',
                    scale=alt.Scale(range=[200, 1300]),  # Ajustar tamaño de burbujas
                    legend=None  # Eliminar la leyenda de tamaño
                ),
                color=alt.Color(
                    'proportion_affected:Q',
                    scale=alt.Scale(scheme='reds'),
                    title='Proporción Afectada (%)',
                    legend=alt.Legend(labelFontSize=14, titleFontSize=16)  # Leyenda más grande
                ),
                tooltip=[
                    alt.Tooltip('nom_muni:N', title="Municipio", format=""),
                    alt.Tooltip('affected_area:Q', title="Área Afectada"),
                    alt.Tooltip('proportion_affected:Q', title="Proporción (%)", format=".2f")
                ]
            ).properties(
                width=1000,
                height=600
            )

            # Mostrar el título centrado
            st.markdown(
                """
                <h1 style='text-align: center; margin-left:-150px; font-size: 30px; font-family: Roboto, sans-serif;'>
                    Porcentaje de viviendas afectadas en relación al total de áreas afectadas por municipio<br>
                </h1>
                """,
                unsafe_allow_html=True
            )

            # Mostrar el Bubble Chart en Streamlit
            st.altair_chart(bubble_chart, use_container_width=True)


        ## HISTOGRAMAS


        st.markdown("<br><br>", unsafe_allow_html=True)

        # Convertir GeoDataFrame a DataFrame
        df = gdf.drop(columns='geometry')

        df['nom_rio'] = df['nom_rio'].str.strip().str.lower()
        df['nom_muni'] = df['nom_muni'].str.strip().str.lower()

        # Calcular los Top 10 nombres de ríos por frecuencia
        top10_rio = df['nom_rio'].value_counts().nlargest(10).index.tolist()
        df_rio_top10 = df[df['nom_rio'].isin(top10_rio)]

        # Calcular los Top 10 nombres de municipios por frecuencia
        top10_muni = df['nom_muni'].value_counts().nlargest(10).index.tolist()
        df_muni_top10 = df[df['nom_muni'].isin(top10_muni)]

        st.markdown("<br>", unsafe_allow_html=True)

        # Histograma agrupado por nombre de río
        st.markdown(
            """
            <h1 style='text-align: center; font-size: 40px; font-family: Roboto, sans-serif;'>
                Afecciones por nombre de río (Top 10)<br>
            </h1>
            """,
            unsafe_allow_html=True
        )

        # Capitalizar los nombres para una mejor presentación
        df_rio_top10['nom_rio'] = df_rio_top10['nom_rio'].str.title()

        # Eliminar la columna 'geometry' si existe
        if 'geometry' in df_rio_top10.columns:
            df_rio_top10 = df_rio_top10.drop(columns=['geometry'])

        hist_rio = alt.Chart(df_rio_top10).mark_bar().encode(
            alt.X(
                'nom_rio:N',
                title="Nombre del Río",
                axis=alt.Axis(labelFontSize=18, titleFontSize=25),
                sort=alt.EncodingSortField(field="count()", op="count", order="descending")  # Ordenar por frecuencia
            ),
            alt.Y(
                'count():Q',
                title="Frecuencia",
                axis=alt.Axis(labelFontSize=20, titleFontSize=22)
            ),
            color=alt.Color(
                'estado:N',
                legend=alt.Legend(
                    title="Estado",
                    labelFontSize=18,  # Tamaño de las etiquetas de la leyenda
                    titleFontSize=22   # Tamaño del título de la leyenda
                ),
                scale=alt.Scale(
                    domain=["affected", "not affected"],
                    range=["#e67e22", "#276994"]
                )
            ),
            tooltip=['nom_rio:N', 'estado:N', 'count():Q']
        ).interactive().properties(
            height=700  # Ajuste de la altura para hacerlo más visible
        )

        st.altair_chart(hist_rio, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)


        # Histograma agrupado por nombre de municipio
        st.markdown(
            """
            <h1 style='text-align: center; font-size: 40px; font-family: Roboto, sans-serif;'>
                Distribución de Afectados y No Afectados por Municipio (Top 10)<br>
            </h1>
            """,
            unsafe_allow_html=True
        )

        # Capitalizar los nombres para una mejor presentación
        df_muni_top10['nom_muni'] = df_muni_top10['nom_muni'].str.title()

        # Eliminar la columna 'geometry' si existe
        if 'geometry' in df_muni_top10.columns:
            df_muni_top10 = df_muni_top10.drop(columns=['geometry'])

        hist_muni = alt.Chart(df_muni_top10).mark_bar().encode(
            alt.X(
                'nom_muni:N',
                title="Nombre del Municipio",
                axis=alt.Axis(labelFontSize=20,titleFontSize=22),
                sort=alt.EncodingSortField(field="count()", op="count", order="descending")  # Ordenar por frecuencia
            ),
            alt.Y(
                'count():Q',
                title="Frecuencia",
                axis=alt.Axis(labelFontSize=20, titleFontSize=22)
            ),
            color=alt.Color(
                'estado:N',
                legend=alt.Legend(
                    title="Estado",
                    labelFontSize=18,  # Tamaño de las etiquetas de la leyenda
                    titleFontSize=22   # Tamaño del título de la leyenda
                ),
                scale=alt.Scale(
                    domain=["affected", "not affected"],
                    range=["#e67e22", "#276994"]
                )
            ),
            tooltip=['nom_muni:N', 'estado:N', 'count():Q']
        ).interactive().properties(
            height=700  # Ajuste de la altura para hacerlo más visible
        )

        st.altair_chart(hist_muni, use_container_width=True)

    except FileNotFoundError:
        st.error(f"No se pudo encontrar el archivo en la ruta: {file_path}")

else:
    # Si gdf_filtrado está vacío, muestra mensaje
    st.write("Por favor, selecciona un municipio válido para ver los datos.")
