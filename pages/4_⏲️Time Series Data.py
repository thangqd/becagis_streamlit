import streamlit as st 
import pandas as pd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static
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

st.title("Time Series Data")


config_file = "./data/kepler/strava_config.json"
with open(config_file, "r",encoding="utf-8") as f:
    config = json.load(f)

geolenny_maughan_json = pd.read_json('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/lenny_maughan.geojson')
lenny_maughan_map = KeplerGl(data={"trip_data": geolenny_maughan_json}, config = config, height=600)
keplergl_static(lenny_maughan_map,  center_map=True)

# df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/lenny_maughan.csv')
# config_file = "./data/kepler/strava_config.json"
# # df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/nyc.csv')
# # config_file = "./data/kepler/nyc_config.json"

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

# # st.write(geo_json)


# my_map = KeplerGl(data={"trip_data": geo_json}, config = config, height=600)
# # my_map = KeplerGl(data= geo_json, height=600)
# keplergl_static(my_map,  center_map=True)

