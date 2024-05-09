import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")

st.title("Pydeck TripLayer")


TRIPS_LAYER_DATA = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/trip.json"  # noqa

df = pd.read_json(TRIPS_LAYER_DATA)

# df["coordinates"] = df["waypoints"].apply(lambda f: [item["coordinates"] for item in f])
# df["timestamps"] = df["waypoints"].apply(lambda f: [item["timestamp"] - 1554772579000 for item in f])

# df.drop(["waypoints"], axis=1, inplace=True)

layer = pdk.Layer(
    "TripsLayer",
    df,
    get_path="path",
    get_timestamps="timestamps",
    get_color=[253, 128, 93],
    opacity=0.8,
    width_min_pixels=5,
    rounded=True,
    trail_length=600,
    current_time=500,
)

view_state = pdk.ViewState(latitude=40.692425048772414,  longitude=-73.97129537711257, zoom=11, bearing=0, pitch=45)

# Render
# r = pdk.Deck(layers=[layer], initial_view_state=view_state)
# r.to_html("trips_layer.html")

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state
    ))