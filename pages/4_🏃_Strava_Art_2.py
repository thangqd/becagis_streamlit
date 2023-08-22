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
center_lat = -2.548828 #37.76067887817949
center_lon = 51.467697 #-122.44104772133697
myMap = folium.Map(location=[center_lat,center_lon], tiles="stamenterrain", width = 1200, height = 600, zoom_start=1)
Fullscreen(                                                         
        position                = "topright",                                   
        title                   = "Open full-screen map",                       
        title_cancel            = "Close full-screen map",                      
        force_separate_button   = True,                                         
    ).add_to(myMap) 


polygon = {
    'type': 'Feature',
    'geometry': {
        'type': 'MultiPolygon',
       'coordinates': [((
             (-2.548828, 51.467697),
             (-0.087891, 51.536086),
             (-1.516113, 53.800651),
             (-6.240234, 53.383328),
        ),)],
    },
    'properties': {
        'style': {
            'color': 'blue',
        },
        'times': ['2015-07-22T00:00:00', '2015-08-22T00:00:00', '2015-09-22T00:00:00']
    }
}


TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': [polygon]},
    period='P1M',
    duration='P1M',
    auto_play=False,
    loop=False,
    loop_button=True,
    # date_options='DD/MM/YYYY',
    date_options='YYYY/MM/DD'
).add_to(myMap)


# folium.GeoJson(lenny_maughan, style_function=lenny_maughan_style, name="Lenny Maughan's Strava Art").add_to(myMap)

# folium_static(myMap)
st_folium(myMap)
