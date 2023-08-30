import streamlit as st 
import pandas as pd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
import json
import gpxpy
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import geopy.distance
import numpy as np
from datetime import datetime, timedelta
import geopandas as gpd



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

def calculate_time(row):
    time = datetime.now() + timedelta(seconds=row["id"])
    return time


gpx_file_raw = st.file_uploader("📂 Upload your activity.gpx file", type=["gpx"], accept_multiple_files=False)
if gpx_file_raw is not None:

    gpx_file = gpxpy.parse(gpx_file_raw)    
    points = []
    i = 0
    track_name = gpx_file.tracks[0].name
    track_length = round(gpx_file.tracks[0].length_3d()*10**(-3),2)    
    # track_time = gpx_file.tracks[0].get_time_bounds().start_time
    # track_duration = gpx_file.tracks[0].get_duration()
    track_speed = gpx_file.tracks[0].get_moving_data().max_speed

    st.write(track_name,track_length,track_speed)
    for segment in gpx_file.tracks[0].segments:
        for p in segment.points:
            points.append({
                'id': i ,
                'time': p.time,
                'latitude': p.latitude,
                'longitude': p.longitude,
                'elevation': p.elevation,
            })
            i+=1
    df = pd.DataFrame.from_records(points)
    coords = [(p.latitude, p.longitude) for p in df.itertuples()]
    if df["time"].isnull().values.any():
        df["time"] = df.apply(calculate_time, axis=1)
    # df['distance'] = [0] + [geopy.distance.distance(from_, to).m for from_, to in zip(coords[:-1], coords[1:])]
    # df['cumulative_distance'] = df.distance.cumsum()
    # # Timing.
    # df['duration'] = df.time.diff().dt.total_seconds().fillna(0)
    # df['cumulative_duration'] = df.duration.cumsum()
    # df['pace_metric'] = pd.Series((df.duration / 60) / (df.distance / 1000)).bfill()
    df['name'] = track_name
    csv = df.to_csv("./data/strava/strava.csv")    
    gpx = pd.read_csv("./data/strava/strava.csv")
    st.write(gpx)
    geo_json = dict(type="FeatureCollection", features=[])
    for track in gpx.name.unique():
        feature = dict(type="Feature", geometry=None, properties=dict(name=str(track)))
        feature["geometry"] = dict(type="LineString", coordinates=gpx.loc[gpx.name==track, ["longitude", "latitude", "elevation", "time"]].to_records(index=False).tolist())
        geo_json["features"].append(feature)

    config_file = "./data/kepler/gpx_config.json"
    with open(config_file, "r",encoding="utf-8") as f:
        config = json.load(f)

    my_map = KeplerGl(data={"GPX": geo_json}, config = config, height=600)
    # my_map = KeplerGl(data= df, height=600)
    keplergl_static(my_map,  center_map=True)



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