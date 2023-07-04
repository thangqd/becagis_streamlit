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
    Thang Quach: [BecaGIS Homepage](https://becagis.vn/?lang=en) | [GitHub Pages](https://thangqd.github.io)
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/quachdongthang) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

# Reference: https://dwtkns.com/srtm30m/

st.title("Open Google Street View")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/streetview.png",width = 30)
with col2:
    st.write("Open Google Street View")

m = folium.Map(tiles='Stamen Toner')
df = pd.read_csv("https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/cali_earthquakes.csv")
fc= FeatureGroup(name="Cities",overlay=True)
cf_cluster = MarkerCluster(name="Cities").add_to(m)

for i,row in df.iterrows():
    lat = df.at[i, 'lat']  #latitude
    lon = df.at[i, 'lon']  #longitude
    popup = str(df.at[i,'depth']) +'<br>' + str(df.at[i, 'y']) + '<br>' + '<a href="https://www.google.com/maps?layer=c&cbll=' + str(df.at[i, 'lat']) + ',' + str(df.at[i, 'lon']) + '" target="blank">GOOGLE STREET VIEW</a>'
    cf_marker = folium.Marker(location=[lat,lon], popup=popup, icon = folium.Icon(color='green', icon='glyphicon-calendar'))
    cf_cluster.add_child(cf_marker)

# st_folium(m, width=800,returned_objects=[])
st_folium(m, width=800)