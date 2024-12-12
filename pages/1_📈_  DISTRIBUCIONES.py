import streamlit as st
import pandas as pd
import altair as alt
from styles.css_functions import custom_title

st.set_page_config(page_title="HISTOGRAMAS", page_icon="📈", layout="wide")


def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Llama la función para cargar el CSS
load_css("styles/styles.css")


df_buildings = pd.read_csv(r"C:\Users\Darkos\Desktop\test\data\df_buildings.csv")
df_roads = pd.read_csv(r"C:\Users\Darkos\Desktop\test\data\df_roads.csv")

# Filtrar los datos para incluir solo distancias <= 3000
filtered_data = df_buildings[df_buildings['distance'] <= 3000]

filtered_roads = df_roads[(df_roads['distance_2'] > 100) & (df_roads['distance_2'] <= 3000)]




## HISTOGRAMA DISTANCIA - EDIFICIOS
custom_title(
    text="Distribución de distancia de edificios a cobertura de agua más cercana",
    size="2.5em",
    text_align="center"
)

st.markdown("<br>", unsafe_allow_html=True)

# Crear el histograma para edificios
histogram_buildings = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X(
        'distance:Q',
        #bin=alt.Bin(maxbins=bins_data),  # Usar bins dinámicos
        title='Distancia (m)',
        axis=alt.Axis(
            labelFontSize=18,
            titleFontSize=25,
            gridColor='lightgray',
            gridOpacity=0.1
        ),
        scale=alt.Scale(domain=[0, 3000])
    ),
    y=alt.Y(
        'count()',
        title='Frecuencia',
        axis=alt.Axis(
            labelFontSize=18,
            titleFontSize=25,
            gridColor='lightgray',
            gridOpacity=0.1
        )
    ),
    color=alt.Color(
        'distance:Q',
        scale=alt.Scale(
            domain=[0, 3000],
            range=['red', 'yellow']  # Gradiente de amarillo a naranja
        ),
        legend=alt.Legend(title="Distancia (m)")
    ),
    tooltip=[
        alt.Tooltip('distance:Q', title='Distance (binned)'),
        alt.Tooltip('count()', title='Frecuencia')
    ]
).properties(
    width=800,
    height=500
).configure_mark(
    opacity=0.1  # TRANSPARENCIA
)

st.altair_chart(histogram_buildings, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)



## HISTOGRAMA DISTANCIA - CARRETERAS

custom_title(
    text="Distribución de distancia de carreteras a cobertura de agua más cercana",
    size="2.5em",
    text_align="center"
)
st.markdown("<br>", unsafe_allow_html=True)

# Control deslizante para el número de bins
bins_roads = st.slider("Número de bins", min_value=10, max_value=200, value=80, step=10)

st.markdown("<br>", unsafe_allow_html=True)

# Histograma para carreteras
histogram_roads = alt.Chart(filtered_roads).mark_bar(color='orange').encode(
    x=alt.X(
        'distance_2:Q',
        bin=alt.Bin(maxbins=bins_roads),
        title='Distancia (m)',
        axis=alt.Axis(
            labelFontSize=18,
            titleFontSize=25,
            gridColor='lightgray',
            gridOpacity=0.1
        ),
        scale=alt.Scale(domain=[100, 3000])
    ),
    y=alt.Y(
        'count()',
        title='Frecuencia',
        axis=alt.Axis(
            labelFontSize=18,
            titleFontSize=25,
            gridColor='lightgray',
            gridOpacity=0.1
        )
    ),
    tooltip=[
        alt.Tooltip('distance_2:Q', title='Distance (binned)'),
        alt.Tooltip('count()', title='Frecuencia')
    ]
).properties(
    width=800,
    height=500
).configure_mark(
    opacity=0.3 
)

st.altair_chart(histogram_roads, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)


filtered_2 = df_roads[df_roads['distance_2'] < 100]

# Contar el número total de filas
frequency = filtered_2.shape[0]

col1 = st.columns(1)

with col1[0]:  # Columna única para mostrar el marcador
    st.markdown(
        f"""<div style='font-size: 2.3em; text-align: center;margin-right:80px'><b>Viviendas a menos de 100m</b><br>
        <span style='font-size: 2.5em;background-color: #154360; border-radius: 15px; padding: 8px;'>{frequency:,}</span></div>""",
        unsafe_allow_html=True,
    )

st.markdown("<br><br><br>", unsafe_allow_html=True)

## HISTOGRAMA DISTANCIA - EDIFICIOS
custom_title(
    text="Distribución de zonas afectadas por tipo de cobertura",
    size="2.5em",
    text_align="center"
)

data = pd.read_csv(r'C:\Users\Darkos\Desktop\Labs\Final_project\df_ground.csv')

# Calcular las frecuencias de la columna 'COBERTURA_DESC'
frequencies = data['COBERTURA_DESC'].value_counts().reset_index()
frequencies.columns = ['COBERTURA_DESC', 'Count']

# Chart tree
chart = alt.Chart(frequencies).mark_bar().encode(
    x=alt.X(
        'Count:Q',
        title='Frecuencia',
        sort='-y',
        axis=alt.Axis(
            labelFontSize=16, 
            titleFontSize=20   
        )
    ),
    y=alt.Y(
        'COBERTURA_DESC:N',
        title='Tipo de Cobertura',
        sort='-x',
        axis=alt.Axis(
            labelFontSize=16, 
            titleFontSize=20  
        )
    ),
    color=alt.Color(
        'Count:Q',
        scale=alt.Scale(
            range=['yellow', 'red']
        )
    ),
    tooltip=['COBERTURA_DESC', 'Count']
).properties(
    width=800,
    height=500
).configure_mark(
    opacity=0.9
)

st.altair_chart(chart, use_container_width=True)
