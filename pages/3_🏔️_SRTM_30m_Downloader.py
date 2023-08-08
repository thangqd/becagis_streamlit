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

# Reference: https://dwtkns.com/srtm30m/

st.title("Download 30m SRTM Data")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/nasa.png", width = 40)
with col2:
    st.write("Download 30-meter resolution elevation data (DEM) from the [Shuttle Radar Topography Mission](https://www2.jpl.nasa.gov/srtm/) | Reference: [Derek Watkins](https://dwtkns.com/srtm30m/)")
st.write( """
        You are requested to login to download SRTM data. If you do not have an account, please create one at [EARTHDATA](https://urs.earthdata.nasa.gov//users/new)
     """)

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

srtm_bbox_url = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/srtm_bbox.geojson"
srtm_bbox_gdp = gpd.read_file(srtm_bbox_url)
srtm_bbox = json.loads(requests.get(srtm_bbox_url).text)
# m = folium.Map(tiles="stamenterrain", location = [10.78418915150491, 106.70361262696979], zoom_start = 3)
m = folium.Map(tiles="stamenterrain", location = [-28, 14], zoom_start =2)
 

# featuregroup = folium.map.FeatureGroup(name='SRTM BBox').add_to(m)
# i =0
# for feature in srtm_bbox['features']:
#     while i < 10:
#         fea = folium.GeoJson(feature['geometry'],style_function = style_function, highlight_function=highlight_function)
#         fea.add_child(folium.Popup(['<a href="' + feature['properties']['dem'] + '" target="blank">DEM: </a>'+ '<br>' + '<a href=' + feature['properties']['image'] + '" target="blank">JPG: </a>'] ))
#         featuregroup.add_child(fea)
#     i+=1

popup = folium.GeoJsonPopup(
    fields=["dem_link", "image_link"],
    aliases=['Download DEM: ', 'Preview Image: '],
    localize=True,
    labels=True,
    style=(
        "background-color: white; color: #333333; font-family: arial; font-size: 12px; overflow: auto;"
    ),
)

srtm_bbox = folium.GeoJson(srtm_bbox_gdp, style_function = style_function, highlight_function=highlight_function, popup=popup)
srtm_bbox.add_to(m)

st_folium(m, width=800,returned_objects=[])