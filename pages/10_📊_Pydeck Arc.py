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
    Thang Quach: [BecaGIS Homepage](https://becagis.vn/?lang=en) | [GitHub Pages](https://thangqd.github.io)
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/quachdongthang) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

# DATA_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airlines_vn.csv"
AIRLINES_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airlines_vn.csv"

airlines_df = pd.read_csv(AIRLINES_URL)
# st.write (df)
WHITE_RGB = [255, 255, 255, 40]
GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

air_lines = pdk.Layer(
    "ArcLayer",
    data=airlines_df,
    get_width=2,
    get_source_position=["src_lon", "src_lat"],
    get_target_position=["dest_lon", "dest_lat"],
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
    "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airports.csv"  
)

air_ports = pdk.Layer(
    'ScatterplotLayer',     # Change the `type` positional argument here
    ARIPORTS_URL,
    get_position=["longitude", "latitude"],
    auto_highlight=True,
    get_radius=2000,          # Radius is given in meters
    get_fill_color=[180, 0, 200, 140],  # Set an RGBA value for fill
    pickable=True)

# pdk.settings.custom_libraries = [
#     {
#         "libraryName": "MyTileLayerLibrary",
#         "resourceUri": "https://cdn.jsdelivr.net/gh/agressin/pydeck_myTileLayer@master/dist/bundle.js",
#     }
# ]

# DATA_URL = 'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png'
# custom_layers = pdk.Layer(
#     "MyTileLayer",
#     DATA_URL
# )
# r = pdk.Deck(custom_layers, initial_view_state=view_state,map_provider=None)
# st.components.v1.html(r.to_html(as_string=True), width=800, height=600)

st.pydeck_chart(pdk.Deck(
    layers=[air_lines,air_ports],
    initial_view_state=view_state,
    map_style=None,
    tooltip=TOOLTIP_TEXT
))


