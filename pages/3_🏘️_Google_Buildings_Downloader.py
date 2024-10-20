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

st.title("Download Google Open Buildings")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/google.png", width = 30)
with col2:
    st.write("Download [Google Open Buildings](https://sites.research.google/open-buildings/)")

# with st.expander("See source code"):
#     with st.echo():
# The user credentials that will be used to authenticate access to the data
 
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

google_buildings_url = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/google_buildings.geojson"
google_buildings_gdp = gpd.read_file(google_buildings_url)
google_buildings = json.loads(requests.get(google_buildings_url).text)
m = folium.Map(tiles="cartodbpositron", location = [-28, 14], zoom_start = 2)


popup = folium.GeoJsonPopup(
    fields=["tile_id", "size_mb","tile_link"],
    aliases=['Tile ID: ', 'Size(MB): ','Tile URL: '],
    localize=True,
    labels=True,
    style=(
        "background-color: white; color: #333333; font-family: arial; font-size: 12px; overflow: auto;"
    ),
)

google_bbox = folium.GeoJson(google_buildings_gdp, style_function = style_function, highlight_function=highlight_function, popup=popup)
google_bbox.add_to(m)

st_folium(m, width=800,returned_objects=[])