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
from folium.plugins import MarkerCluster, FastMarkerCluster, Fullscreen
from streamlit_folium import st_folium, folium_static

st.set_page_config(layout="wide")

st.title("Panoramic Maps Collection")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/loc.svg", width = 30)
with col2:
    st.write("Exploring [Panoramic Maps Collection](https://www.loc.gov/collections/panoramic-maps/about-this-collection?loclr=blogmap) from [Library of Congress](https://www.loc.gov/collections/)")

 
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
df = gpd.read_file(panorama_url)

m = folium.Map(tiles ="cartodbpositron", location = [40.10629422187102, -98.53718356247916], zoom_start =3)
Fullscreen(                                                         
    position                = "topright",                                   
    title                   = "Open full-screen map",                       
    title_cancel            = "Close full-screen map",                      
    force_separate_button   = True,                                         
).add_to(m)             
cluster = MarkerCluster()
for id,title,date,address,thumbnail,division,division_url,latitude,longitude in \
zip(df.id, df.title, df.date, df.address, df.thumbnail, df.division, df.division_url, df.latitude, df.longitude):
    color = 'purple'
    icon=folium.Icon(color=color, icon='ok-circle')
    popContent = (
                '<b>(' + address + ',' + str(date) + ')</b>, ' + title + '<br>' +\
                '<center><img src="{}" alt="Image">'.format(thumbnail)+ '<br>'+              
                '<a href=' + id + ' target="_blank">' + title + '</a>' + '<br>'+\
                'Published in ' + date + '</center><br>'+\
                'Available from ' + '<a href=' + division_url  +  ' target="_blank">' + division + ', Library of Congress' + '</a>'
                )   
    iframe = folium.IFrame(popContent)
    popup = folium.Popup(iframe,
                        min_width=300,
                        max_width=400)   
    folium.Marker(location=[latitude, longitude], icon=icon, popup=popup).add_to(cluster)    
m.add_child(cluster)            
folium_static(m, width = 700)


# panorama_url = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/panorama.csv"
# panorama_gdp = gpd.read_file(panorama_url)
# panorama = json.loads(requests.get(panorama_url).text)
# m = folium.Map(tiles="cartodbpositron", location = [-28, 14], zoom_start = 2)


# popup = folium.GeoJsonPopup(
#     fields=["tile_id", "size_mb","tile_link"],
#     aliases=['Tile ID: ', 'Size(MB): ','Tile URL: '],
#     localize=True,
#     labels=True,
#     style=(
#         "background-color: white; color: #333333; font-family: arial; font-size: 12px; overflow: auto;"
#     ),
# )

# google_bbox = folium.GeoJson(panorama_gdp, style_function = style_function, highlight_function=highlight_function, popup=popup)
# google_bbox.add_to(m)

# st_folium(m, width=800,returned_objects=[])


