import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import AntPath, Fullscreen, TimestampedGeoJson
import streamlit as st

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

st.title("Strava Art")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/strava.png", width = 30)
with col2:
    st.write("[Lenny Maughan's Strava Art](https://www.strava.com/athletes/7019519)")



lenny_maughan  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/lenny_maughan.geojson"

lenny_maughan_style = lambda x: {
  'color' :  'red',
  'opacity' : 1,
  'weight' : 2,
}



myMap = folium.Map(location=[37.76067887817949, -122.44104772133697], tiles="stamenterrain", width = 1200, height = 600, zoom_start=12)
Fullscreen(                                                         
        position                = "topright",                                   
        title                   = "Open full-screen map",                       
        title_cancel            = "Close full-screen map",                      
        force_separate_button   = True,                                         
    ).add_to(myMap) 


TimestampedGeoJson(lenny_maughan).add_to(myMap)


folium_static(myMap)
