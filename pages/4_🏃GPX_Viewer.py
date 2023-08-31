import streamlit as st 
import pandas as pd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
import json
import numpy as np
import numpy as np
from datetime import datetime, timedelta
import geopandas as gpd
from shapely.geometry import shape
import os 

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
st.title("GPX Viewer")
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pandas as pd
from pandas.io.json import json_normalize
import fiona

def calculate_time(row):
    time = datetime.now() + timedelta(seconds=row["track_seg_point_id"])
    return time
def save_uploadedfile(uploadedfile):
    with open(os.path.join(".\data\gpx", uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to Data".format(uploadedfile.name))

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
  
gpx_file_raw = st.file_uploader("📂 Upload your GPX file", type=["gpx"], accept_multiple_files=False)
if gpx_file_raw is not None: 
    # gdf_point = gpd.read_file(gpx_file_raw, layer = 'track_points')
    # gdf_track = gpd.read_file(gpx_file_raw, layer = 'tracks')
    gdf_point = gpd.read_file(gpx_file_raw, layer = 'track_points')
    gdf_point.sort_values('track_seg_point_id', inplace=True)
    gdf_point.reset_index(drop=True, inplace=True)
    gdf_point = gdf_point[['track_seg_point_id', 'ele', 'time', 'geometry']].copy()
    gdf_point['longitude'] = gdf_point.geometry.apply(lambda p: p.x)
    gdf_point['latitude'] = gdf_point.geometry.apply(lambda p: p.y)
    gdf_point['name'] = gpx_file_raw.name.split('.')[0]
    if gdf_point["time"].isnull().values.any() :
    # if pd.isna(gdf_point["time"]):
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

    # my_map = KeplerGl(data={"Track Points": track_points}, config = config, height=600)
    my_map = KeplerGl(data={"Track": track}, config = config, height=600)
    # my_map = KeplerGl(data={"Track": track_points}, height=600)
    # my_map.add_data(data=gdf_point,name='Track Points')
    keplergl_static(my_map, center_map=True)
    track_string = json.dumps(track)
    download_track(track_string,gpx_file_raw.name.split('.')[0])
    with st.expander("View Track in GeoJSON"):
    # st.write(track)        
        # st.json(track_string, expanded=True)
        st.write(track)   
    download_trackpoints(gdf_point,gpx_file_raw.name.split('.')[0])  
    with st.expander("View Track Points"):
        st.write(gdf_point)
    
####################################3
    # with open(os.path.join(".\data\gpx", gpx_file_raw.name), "wb") as f:
    #    f.write(gpx_file_raw.getbuffer())
    # with open(os.path.join(".\data\gpx",gpx_file_raw.name), "rb") as f:
    #     tracks_layer = fiona.open(f, layer='tracks')
    #     feature = tracks_layer[0]
    #     tracks_data = {'type': 'MultiLineString',
    #                 'coordinates': feature['geometry']['coordinates']}
    #     tracks_shape = shape(tracks_data)
    #     gdf_track = gpd.GeoDataFrame(index=[0], crs='epsg:4326', geometry=[tracks_shape])
    #     st.write(gdf_track)
############################3
# csv_file = st.file_uploader("📂 Upload your activity.csv file", type=["csv"], accept_multiple_files=False)
# if csv_file is not None:
#     df = pd.read_csv(csv_file)
#     geo_json = dict(type="FeatureCollection", features=[])
#     for track in df.name.unique():
#         feature = dict(type="Feature", geometry=None, properties=dict(name=str(track)))
#         feature["geometry"] = dict(type="LineString", coordinates=df.loc[df.name==track, ["lon", "lat", "ele", "time"]].to_records(index=False).tolist())
#         geo_json["features"].append(feature)

#     config_file = "./data/kepler/gpx_config.json"
#     with open(config_file, "r",encoding="utf-8") as f:
#         config = json.load(f)

#     my_map = KeplerGl(data={"GPX": geo_json}, config = config, height=600)
#     # my_map = KeplerGl(data= df, height=600)
#     keplergl_static(my_map,  center_map=True)

#######################################
    # st.write(geo_json)
    # gpx_file = gpxpy.parse(gpx_file_raw)    
    # points = []
    # track_name = gpx_file.tracks[0].name
    # track_length = round(gpx_file.tracks[0].length_3d()*10**(-3),2)    
    # track_time = gpx_file.tracks[0].get_time_bounds().start_time
    # track_duration = gpx_file.tracks[0].get_duration()
    # track_speed = gpx_file.tracks[0].get_moving_data().max_speed
    # st.write(track_name,track_length,track_speed)
    # for segment in gpx_file.tracks[0].segments:
    #     # for j, p in segment.points:
    #     for i, p in enumerate(segment.points):
    #         points.append({
    #             'id': i ,
    #             'time': p.time,
    #             'latitude': p.latitude,
    #             'longitude': p.longitude,
    #             'elevation': p.elevation,
    #             'speed': segment.get_speed(i)
    #         })
    
    # df = pd.DataFrame.from_records(points)
    # coords = [(p.latitude, p.longitude) for p in df.itertuples()]
    # if df["time"].isnull().values.any():
    #     df["time"] = df.apply(calculate_time, axis=1)
    # # df['distance'] = [0] + [geopy.distance.distance(from_, to).m for from_, to in zip(coords[:-1], coords[1:])]
    # # df['cumulative_distance'] = df.distance.cumsum()
    # # # Timing.
    # # df['duration'] = df.time.diff().dt.total_seconds().fillna(0)
    # # df['cumulative_duration'] = df.duration.cumsum()
    # # df['pace_metric'] = pd.Series((df.duration / 60) / (df.distance / 1000)).bfill()
    # df['name'] = track_name
    # csv = df.to_csv("./data/strava/strava.csv")    
    # gpx = pd.read_csv("./data/strava/strava.csv")
    # st.write(gpx)
    # geo_json = dict(type="FeatureCollection", features=[])
    # for track in gpx.name.unique():
    #     feature = dict(type="Feature", geometry=None, properties=dict(name=str(track)))
    #     feature["geometry"] = dict(type="LineString", coordinates=gpx.loc[gpx.name==track, ["longitude", "latitude", "elevation", "time"]].to_records(index=False).tolist())
    #     geo_json["features"].append(feature)
