import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

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
st.title("Pydeck TripLayer")

import pydeck as pdk
import pandas as pd

TRIPS_LAYER_DATA = "https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/sf.trips.json"  # noqa

df = pd.read_json(TRIPS_LAYER_DATA)

df["coordinates"] = df["waypoints"].apply(lambda f: [item["coordinates"] for item in f])
df["timestamps"] = df["waypoints"].apply(lambda f: [item["timestamp"] - 1554772579000 for item in f])

df.drop(["waypoints"], axis=1, inplace=True)

layer = pdk.Layer(
    "TripsLayer",
    df,
    get_path="coordinates",
    get_timestamps="timestamps",
    get_color=[253, 128, 93],
    opacity=0.8,
    width_min_pixels=5,
    rounded=True,
    trail_length=600,
    current_time=500,
)

view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=11, bearing=0, pitch=45)

# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state)
r.to_html("trips_layer.html")

)


view_state = pdk.ViewState(latitude=20, longitude=10, bearing=0, pitch=20, zoom=1)

TOOLTIP_TEXT = {"html": "{src} to {dest} "}
# r = pdk.Deck(arc_layer, initial_view_state=view_state)

ARIPORTS_URL = (
    "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/airports.csv"  
)

air_ports = pdk.Layer(
    'ScatterplotLayer',     # Change the `type` positional argument here
    ARIPORTS_URL,
    get_position=["lon", "lat"],
    auto_highlight=True,
    get_radius=2000,          # Radius is given in meters
    get_fill_color=[180, 0, 200, 140],  # Set an RGBA value for fill
    pickable=True)

st.pydeck_chart(pdk.Deck(
    layers=[air_lines,air_ports],
    initial_view_state=view_state,
    map_style=None,
    tooltip=TOOLTIP_TEXT
))


