import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web: <https://becagis.streamlit.app/>
    - GitHub: <https://github.com/thangqd/becagis_streamlit>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Thang Quach: <https://thangqd.github.io>
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

input = "./data/watersupply_mekong.geojson"
GeoJSON_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/vn_provinces.geojson"



geojson = pdk.Layer(
    "GeoJsonLayer",
    GeoJSON_URL,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation="properties.area",
    get_fill_color="[255, 0, properties.area / 255]",   
    get_line_color=[255, 255, 255],
)

SCATTERPLOT_URL = (
    "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airports.csv"  
)

HEXAGON_URL = (
    "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airports.csv"  
)
HEATMAP_URL = (
    "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airports.csv"  
    
)

heatmap = pdk.Layer(
    "HeatmapLayer",
    HEATMAP_URL,
    opacity=0.9,
    get_position=["longitude", "latitude"],
    # aggregation=str('MEAN'),
    get_weight="id")

# Define a layer to display on a map
hexagon = pdk.Layer(
    "HexagonLayer",
    HEXAGON_URL,
    get_position=["longitude", "latitude"],
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0, 3000],
    extruded=True,
    coverage=1,
)

scatterplot = pdk.Layer(
    'ScatterplotLayer',     # Change the `type` positional argument here
    SCATTERPLOT_URL,
    get_position=["longitude", "latitude"],
    auto_highlight=True,
    get_radius=20000,          # Radius is given in meters
    get_fill_color=[180, 0, 200, 140],  # Set an RGBA value for fill
    pickable=True)


# Set the viewport location
view_state = pdk.ViewState(
    # latitude=10.045180, longitude=105.78841, zoom=6, max_zoom=20, pitch=40.5
    latitude=10.045180, longitude= 105.78841, zoom=4, max_zoom=20, pitch=20
)

# Render
# pdk.Deck(layers=[layer], initial_view_state=view_state)
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=view_state,
    # layers=[hexagon,scatterplot,heatmap]
    layers=[hexagon,scatterplot]

))
