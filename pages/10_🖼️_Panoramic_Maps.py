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

st.sidebar.info(
    """
    - Web: [BecaGIS Streamlit](https://becagis.streamlit.app)
    - GitHub: [BecaGIS Streamlit](https://github.com/thangqd/becagis_streamlit) 
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Thang Quach: [BecaGIS Homepage](https://becagis.vn/?lang=en) | [My Homepage](https://thangqd.github.io) | [GitHub](https://github.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

st.title("Panoramic Map Collection")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/google.png", width = 30)
with col2:
    st.write("Exploring [Panoramic Map Collection](https://www.loc.gov/collections/panoramic-maps/about-this-collection?loclr=blogmap) from [Library of Congress](https://www.loc.gov/collections/)")

 
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

panorama_url = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/panorama.csv"
panorama_gdp = gpd.read_file(panorama_url)
panorama = json.loads(requests.get(panorama_url).text)
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

google_bbox = folium.GeoJson(panorama_gdp, style_function = style_function, highlight_function=highlight_function, popup=popup)
google_bbox.add_to(m)

st_folium(m, width=800,returned_objects=[])


