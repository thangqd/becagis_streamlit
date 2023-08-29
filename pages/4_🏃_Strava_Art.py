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
import json


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

df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/lenny_maughan.csv')
config_file = "./data/kepler/strava_config.json"
with open(config_file, "r",encoding="utf-8") as f:
    config = json.load(f)
geo_json = dict(type="FeatureCollection", features=[])
geo_json["features"]

for trip in df.trip_id.unique():
    feature = dict(type="Feature", geometry=None, properties=dict(trip_id=str(trip)))
    feature["geometry"] = dict(type="LineString", coordinates=df.loc[df.trip_id==trip, ["lon", "lat", "ele", "time"]].to_records(index=False).tolist())
    geo_json["features"].append(feature)

geo_json["features"].append(feature)

with open('aaa.json', 'w') as f:
    json.dump(geo_json, f)


maughan_map = KeplerGl(data={"trip_data": geo_json}, config = config, height=600)
# my_map = KeplerGl(data= geo_json, height=600)
keplergl_static(maughan_map,  center_map=True)


with open("./data/images/strava/strava.json", "r",encoding="utf-8") as f:
    STRAVA = json.load(f)
total_picture = len(STRAVA)
# if "previous_strava_index" not in st.session_state:
#     st.session_state.update(STRAVA["Tiger"])
#     st.session_state["previous_strava_index"] = 0

strava_image_pattern = "./data/images/strava/{}.png"
strava_image_fp = [
    strava_image_pattern.format(name.lower()) for name in list(STRAVA.keys())[:total_picture]
]

index_selected = image_select(
    label = "Choose a masterpiece",
    images=strava_image_fp,
    captions=list(STRAVA.keys())[:total_picture],
    use_container_width=False,
    return_value="index",
)
name_selected = list(STRAVA.keys())[index_selected].lower()

try:
    img2 = image_select(
        label="",
        images=[],
        return_value="index",
        use_container_width = False
    )
except: st.write('')
# if index_selected != st.session_state["previous_strava_index"]:
#     name_selected = list(STRAVA.keys())[index_selected]
#     st.write(name_selected)
#     st.session_state.update(STRAVA[name_selected].copy())
#     st.session_state["previous_strava_index"] = index_selected

m = KeplerGl(height=600)

strava_timeseries  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/" + name_selected +  "_point.csv"
df_timeseries = pd.read_csv(strava_timeseries)

m.add_data(
    data=df_timeseries, name="Track points"
)  

strava_polyline  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/" + name_selected +  "_polyline.geojson"
with open("./data/strava/" + name_selected +  "_polyline.geojson", 'r') as f:
    df_polyline = f.read()
# st.write(df_polyline)
m.add_data(data=df_polyline, name='Tracks')

keplergl_static(m, center_map=True)