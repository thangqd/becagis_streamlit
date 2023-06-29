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

DATA_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airlines_vn.csv"
# DATA_URL = "./data/airlines_vn.csv"
# DATA_URL = "https://raw.githubusercontent.com/ajduberstein/sf_public_data/master/bay_area_commute_routes.csv"
df = pd.read_csv(DATA_URL)
# st.write (df)

GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_width="2",
    # get_width=2,
    get_source_position=["lon_f", "lat_f"],
    get_target_position=["lon_t", "lat_t"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(latitude=10.045180, longitude=105.78841, bearing=0, pitch=20, zoom=1)

TOOLTIP_TEXT = {"html": "{src} to {dst} "}
r = pdk.Deck(arc_layer, initial_view_state=view_state)


st.pydeck_chart(pdk.Deck(
    layers=[arc_layer],
    initial_view_state=view_state,
    map_style=None,
    tooltip=TOOLTIP_TEXT
))
