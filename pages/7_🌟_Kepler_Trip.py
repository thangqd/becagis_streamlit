import streamlit as st 
import pandas as pd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
import json


st.set_page_config(layout="wide")

st.title("Kepler Trip")


config_file = "./data/kepler/lenny_maughan_config.json"
with open(config_file, "r",encoding="utf-8") as f:
    config = json.load(f)

# geolenny_maughan_json = "./data/strava/lenny_maughan.geojson"
# with open(geolenny_maughan_json) as project_file:    
#     data = json.load(project_file)  
# df = pd.DataFrame(data['body'])
# st.write(df)

# df = pd.DataFrame(data["result"])


lenny_maughan_json = pd.read_json('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/lenny_maughan.geojson')
# lenny_maughan_json = pd.read_json("./data/strava/lenny_maughan.geojson")

lenny_maughan_map = KeplerGl(data={"Track": lenny_maughan_json}, config = config, height=600)

keplergl_static(lenny_maughan_map,  center_map=True)

# df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/lenny_maughan.csv')
# config_file = "./data/kepler/gpx_config.json"
# with open(config_file, "r",encoding="utf-8") as f:
#      config = json.load(f)

# geo_json = dict(type="FeatureCollection", features=[])

# for trip in df.name.unique():
#     feature = dict(type="Feature", geometry=None, properties=dict(name=str(trip)))
#     feature["geometry"] = dict(type="LineString", coordinates=df.loc[df.name==trip, ["lon", "lat", "ele", "time"]].to_records(index=False).tolist())
#     geo_json["features"].append(feature)

# my_map = KeplerGl(data={"Track": geo_json}, config = config, height=600)
# # my_map = KeplerGl(data= geo_json, height=600)
# keplergl_static(my_map,  center_map=True)


#############################################
# df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/nyc.csv')
# config_file = "./data/kepler/nyc_config.json"

# with open(config_file, "r",encoding="utf-8") as f:
#      config = json.load(f)

# df["elevation"] = 0
# geo_json = dict(type="FeatureCollection", features=[])
# geo_json["features"]

# for trip in df.VendorID.unique():
#     feature = dict(type="Feature", geometry=None, properties=dict(VendorID=str(trip)))
#     feature["geometry"] = dict(type="LineString", coordinates=df.loc[df.VendorID==trip, ["pickup_longitude", "pickup_latitude", "elevation", "tpep_pickup_datetime"]].to_records(index=False).tolist())
#     geo_json["features"].append(feature)

# geo_json["features"].append(feature)

# my_map = KeplerGl(data={"trip_data": geo_json}, config = config, height=600)
# # my_map = KeplerGl(data= geo_json, height=600)
# keplergl_static(my_map,  center_map=True)
