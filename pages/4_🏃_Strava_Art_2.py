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



tiger  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/tiger.csv"
tiger_polyline  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/tiger.geojson"

tiger_style = lambda x: {
  'color' :  'red',
  'opacity' : 1,
  'weight' : 2,
}


df = pd.read_csv(tiger)
points = df[["lat", "lon"]]
center_lat = points["lat"].mean()
center_lon = points["lon"].mean()

myMap = folium.Map(location=[center_lat,center_lon], tiles="stamenterrain", width = 1200, height = 600, zoom_start=12)
Fullscreen(                                                         
        position                = "topright",                                   
        title                   = "Open full-screen map",                       
        title_cancel            = "Close full-screen map",                      
        force_separate_button   = True,                                         
    ).add_to(myMap) 


TimestampedGeoJson({
    'type': 'FeatureCollection',
    'features': [
        {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': [[-46.687754, -23.579782]],
            },
            'properties': {
                'icon': 'marker',
                'iconstyle': {
                    'iconSize': [20, 20],
                    'iconUrl':
                        'https://img.icons8.com/ios-filled/50/000000/online-store.png'
                },
                'id': 'house',
                'popup': 1,
                'times': [1633046400000.0]
            }
        }, {
            'type': 'Feature',
            'geometry': {
                'type': 'LineString',
                'coordinates': [[-46.887754, -23.579782]],
            },
            'properties': {
                'icon': 'marker',
                'iconstyle': {
                    'iconSize': [20, 20],
                    'iconUrl':
                        'https://img.icons8.com/ios-filled/50/000000/online-store.png'
                },
                'id': 'house',
                'popup': 1,
                'times': [1635046400000.0]
            }
        }
    ]
}).add_to(myMap)


folium_static(myMap)
