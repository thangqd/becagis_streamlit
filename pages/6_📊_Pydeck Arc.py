import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

st.set_page_config(layout="wide")

st.title("Pydeck Arc")

# DATA_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airlines_vn.csv"
AIRLINES_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/airlines.csv"

airlines_df = pd.read_csv(AIRLINES_URL)
# st.write (df)
WHITE_RGB = [255, 255, 255, 40]
GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

air_lines = pdk.Layer(
    "ArcLayer",
    data=airlines_df,
    get_width=0.2,
    get_source_position=["src_lon", "src_lat"],
    get_target_position=["dest_lon", "dest_lat"],
    # get_source_position=["residence_lng", "residence_lat"],
    # get_target_position=["workplace_lng", "workplace_lat"],
    get_tilt=15,
    get_source_color=GREEN_RGB,
    get_target_color=RED_RGB,
    pickable=True,
    auto_highlight=True,
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
    map_style='light_no_labels', # 'light', 'dark', 'road', 'satellite','dark_no_labels', 'light_no_labels'
    map_provider='carto', #'carto', 'mapbox','google_maps'
    tooltip=TOOLTIP_TEXT
))


