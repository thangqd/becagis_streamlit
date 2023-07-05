import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import FeatureGroup
from folium.plugins import MarkerCluster
import geopandas as gpd
import pandas as pd


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

st.title("Google Street View")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/streetview.png",width = 30)
with col2:
    st.write("Open Google Street View")

us_cities = pd.read_csv("https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/us_cities.csv")
# us_cities = us_cities.dropna().reset_index()
Minot_city_long = us_cities[us_cities["city"] == "Minot"].lon.values[0]
Minot_city_lat = us_cities[us_cities["city"] == "Minot"].lat.values[0]
m = folium.Map(tiles='Stamen Toner', location=[Minot_city_lat, Minot_city_long], zoom_start=3)

# fc= FeatureGroup(name="US Cities",overlay=True)
cities_cluster = MarkerCluster(name="US Cities").add_to(m)

for i,row in us_cities.iterrows():
    lat = us_cities.at[i, 'lat']  #latitude
    lon = us_cities.at[i, 'lon']  #longitude
    popup = us_cities.at[i,'city'] +'<br>' + us_cities.at[i,'state'] +'<br>' + str(us_cities.at[i, 'pop']) + '<br>' + '<a href="https://www.google.com/maps?layer=c&cbll=' + str(us_cities.at[i, 'lat']) + ',' + str(us_cities.at[i, 'lon']) + '" target="blank">GOOGLE STREET VIEW</a>'
    cities_marker = folium.Marker(location=[lat,lon], popup=popup, icon = folium.Icon(color='orange', icon='glyphicon-facetime-video'))
    cities_cluster.add_child(cities_marker)

# st_folium(m, width=800,returned_objects=[])
st_folium(m, height=500,width=800,returned_objects=[])