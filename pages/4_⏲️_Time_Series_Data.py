import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import AntPath, Fullscreen
import streamlit as st
import json
from streamlit_image_select import image_select
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
from pandas.io.json import json_normalize
import json
from folium import plugins


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

st.title("Strava Art")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/strava.png", width = 30)
with col2:
    st.write("[Lenny Maughan's Strava Art Collection](https://www.strava.com/athletes/7019519)")

fp = "./data/csv/trip.csv"
nyc = pd.read_csv(fp)
nyc['starttime'] = nyc['starttime'].str[:-5]
nyc['stoptime'] = nyc['stoptime'].str[:-5]
nyc['starttime'] = pd.to_datetime(nyc['starttime'])
nyc['stoptime'] = pd.to_datetime(nyc['stoptime'])


# Define the startime as index and create a new column
nyc = nyc.set_index('starttime')
nyc['type'] = 'station'



st.write (nyc.head(1))
