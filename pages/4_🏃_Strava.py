import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import AntPath
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

st.title("Strava Route")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/strava.png", width = 30)
with col2:
    st.write("[Lenny Maughan's Strava Route GADM](https://www.strava.com/athletes/7019519)")



tiger  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/tiger.csv"
df = pd.read_csv(tiger)
points = df[["lat", "lon"]]
center_lat = points["lat"].mean()
center_lon = points["lon"].mean()

myMap = folium.Map(location=[center_lat,center_lon], tiles="stamenterrain", width = 600, zoom_start=12)
folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(myMap)

# ant_path = AntPath(
#     locations=points,
#     dash_array=[1, 10],
#     delay=1000,
#     color='#7590ba',
#     pulse_color='#3f6fba'
# ).add_to(myMap)


folium_static(myMap)