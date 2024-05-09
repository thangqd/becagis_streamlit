import streamlit as st
import urllib.request, urllib.parse
from http.cookiejar import CookieJar
import webbrowser
import  leafmap.foliumap as leafmap
from streamlit_folium import st_folium
import folium
from folium import FeatureGroup
from folium.plugins import MarkerCluster
import geopandas as gpd
import pandas as pd
from folium import plugins
import json
import requests

st.set_page_config(layout="wide")

# Reference: https://dwtkns.com/srtm30m/

st.title("Download 90m SRTM Data")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/cgiar.png", width = 30)
with col2:
    st.write("Download 90-meter resolution elevation data (DEM) from [CGIAR-CSI)](https://srtm.csi.cgiar.org/)")
    tile_size = st.selectbox(
            "Select a tile size", [ "30 x 30 degree", "5 x 5 degree",], index=0
        )

    if tile_size == "30 x 30 degree":
        srtm_url = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/srtm_30.geojson"
    elif tile_size == "5 x 5 degree":
        srtm_url = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/srtm_5.geojson"

srtm_gdp = gpd.read_file(srtm_url)
srtm = json.loads(requests.get(srtm_url).text)
m = folium.Map(tiles="cartodbpositron", location = [-28, 14], zoom_start =2)

 
def style_function(feature):
    return {
        'fillColor': '#ffaf00',
        'fillOpacity': 0.3,
        'color': 'blue',
        'weight': 0.2,
        'dashArray': '5, 5'
    }

def highlight_function(feature):
    return {
        'fillColor': '#ffaf00',
        'fillOpacity': 0.5,
        'color': 'magenta',
        'weight': 3,
        'dashArray': '5, 5'
    }

popup = folium.GeoJsonPopup(
    fields=["dem_link"],
    aliases=['Download DEM: '],
    localize=True,
    labels=True,
    style=(
        "background-color: white; color: #333333; font-family: arial; font-size: 12px; overflow: auto;"
    ),
)

srtm_bbox = folium.GeoJson(srtm_gdp, style_function = style_function, highlight_function=highlight_function, popup=popup)
srtm_bbox.add_to(m)

st_folium(m, width=800,returned_objects=[])