import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium, folium_static
import streamlit as st
import json
from streamlit_image_select import image_select
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
import json
import json
from datetime import datetime, timedelta

st.set_page_config(layout="wide")

st.title("Strava Art")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/strava.png", width = 30)
with col2:
    st.write("[Lenny Maughan's Strava Art Collection](https://www.strava.com/athletes/7019519)")

with open("./data/images/strava/strava.json", "r",encoding="utf-8") as f:
    STRAVA = json.load(f)
total_picture = len(STRAVA)
# if "previous_strava_index" not in st.session_state:
#     st.session_state.update(STRAVA["Tiger"])
#     st.session_state["previous_strava_index"] = 0

def calculate_time(row):
    time = datetime.now() + timedelta(seconds=row["track_seg_point_id"])
    return time

def download_trackpoints(gdf, filename):
        geojson = gdf.to_json()  
        st.download_button(
            label="Download Track Points",
            mime="application/json",
            file_name= filename + '_points.geojson',
            data=geojson
        )
def download_track(json_string, filename):
        st.download_button(
            label="Download Track",
            mime="application/json",
            file_name= filename + '_track.geojson',
            data=json_string
        )
  

strava_image_pattern = "./data/images/strava/{}.png"
strava_image_fp = [
    strava_image_pattern.format(name) for name in list(STRAVA.keys())[:total_picture]
]

index_selected = image_select(
    label = "Choose a masterpiece",
    images=strava_image_fp,
    captions=list(STRAVA.keys())[:total_picture],
    use_container_width=False,
    return_value="index",
)
name_selected = list(STRAVA.keys())[index_selected]

try:
    img2 = image_select(
        label="",
        images=[],
        return_value="index",
        use_container_width = False
    )
except: st.write('')

gpx_file_raw  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/" + name_selected +  ".gpx"

gdf_point = gpd.read_file(gpx_file_raw, layer = 'track_points')
gdf_point.sort_values('track_seg_point_id', inplace=True)
gdf_point.reset_index(drop=True, inplace=True)
gdf_point = gdf_point[['track_seg_point_id', 'ele', 'time', 'geometry']].copy()
gdf_point['longitude'] = gdf_point.geometry.apply(lambda p: p.x)
gdf_point['latitude'] = gdf_point.geometry.apply(lambda p: p.y)
gdf_point['name'] = name_selected
if gdf_point["time"].isnull().values.any() :
    gdf_point["time"] = gdf_point.apply(calculate_time, axis=1)

gdf_point['time']=gdf_point['time'].astype(str)

    
track = dict(type="FeatureCollection", features=[])
for track_name in gdf_point.name.unique():
    feature = dict(type="Feature", geometry=None, properties=dict(name=str(track_name)))
    feature["geometry"] = dict(type="LineString", coordinates=gdf_point.loc[gdf_point.name==track_name, ["longitude", "latitude", "ele", "time"]].to_records(index=False).tolist())
    track["features"].append(feature)    
    
config_file = "./data/kepler/gpx_config.json"
with open(config_file, "r",encoding="utf-8") as f:
    config = json.load(f)

my_map = KeplerGl(data={"Track": track}, config = config, height=600)
keplergl_static(my_map, center_map=True)
track_string = json.dumps(track)
download_track(track_string,name_selected + ".geojson")
download_trackpoints(gdf_point,name_selected + ".geojson")  
########################################################################
# if index_selected != st.session_state["previous_strava_index"]:
#     name_selected = list(STRAVA.keys())[index_selected]
#     st.write(name_selected)
#     st.session_state.update(STRAVA[name_selected].copy())
#     st.session_state["previous_strava_index"] = index_selected

# m = KeplerGl(height=600)

# strava_timeseries  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/" + name_selected +  "_point.csv"
# df_timeseries = pd.read_csv(strava_timeseries)

# m.add_data(
#     data=df_timeseries, name="Track points"
# )  

# # strava_polyline  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/" + name_selected +  "_polyline.geojson"
# # with open("./data/strava/" + name_selected +  "_polyline.geojson", 'r') as f:
# #     df_polyline = f.read()
# # # st.write(df_polyline)
# # m.add_data(data=df_polyline, name='Tracks')

# keplergl_static(m, center_map=True)