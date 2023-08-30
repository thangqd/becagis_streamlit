import json 
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/lenny_maughan.csv')
geo_json = dict(type="FeatureCollection", features=[])
geo_json["features"]

for trip in df.trip_id.unique():
    feature = dict(type="Feature", geometry=None, properties=dict(trip_id=str(trip)))
    feature["geometry"] = dict(type="LineString", coordinates=df.loc[df.trip_id==trip, ["lon", "lat", "ele", "time"]].to_records(index=False).tolist())
    geo_json["features"].append(feature)

geo_json["features"].append(feature)

with open('lenny_maughan.geojson', 'w') as f:
    json.dump(geo_json, f)
