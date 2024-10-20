import pandas as pd
import geopandas as gpd
from shapely.geometry import shape

import streamlit as st

st.set_page_config(layout="wide")

st.title("Dowload Microsoft Building Footprints")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/ms_buildings.png", width = 30)
with col2:
    st.write("Download [Microsoft Building Footprints](https://github.com/microsoft/GlobalMLBuildingFootprints)")



@st.cache_data
def read_data():
    path = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/ms_buildings.csv"
    return   pd.read_csv(path)

df = read_data()


countries = df['Location'].drop_duplicates()
country = st.selectbox('', countries )
df_filter = df[df['Location'] == country]  # filter

def make_clickable(url, text):
    link = f'<a target="_blank" href="{url}">{text}</a>'
    # df = pd.read_json(url, lines=True)
    # df['geometry'] = df['geometry'].apply(shape)
    # gdf = gpd.GeoDataFrame(df, crs=4326)
    # gdf.to_file(f"ms_buildings.geojson", driver="GeoJSON")
    return link

df_filter['Url'] = df_filter['Url'].apply(make_clickable, args = ('Download',))
st.write(df_filter.to_html(escape = False), unsafe_allow_html = True)

# st.write(df_filter)