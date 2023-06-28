import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web: <https://becagis.streamlit.app/>
    - GitHub: <https://github.com/thangqd/becagis_streamlit>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Thang Quach: <https://thangqd.github.io>
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

DATA_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airlines_vn.csv"
# DATA_URL = "https://raw.githubusercontent.com/ajduberstein/sf_public_data/master/bay_area_commute_routes.csv"
df = pd.read_csv(DATA_URL)
st.write (df)

GREEN_RGB = [0, 255, 0, 40]
RED_RGB = [240, 100, 0, 40]

arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_width="id*2",
    # get_width=2,
    get_source_position=["lon_f", "lat_f"],
    get_target_position=["lon_t", "lat_t"],
    # get_source_position=["lng_h", "lat_h"],
    # get_target_position=["lng_w", "lat_w"],
    get_tilt=15,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True
)

view_state = pdk.ViewState(latitude=10.045180, longitude=105.78841, bearing=45, pitch=50, zoom=8)
# view_state = pdk.ViewState(latitude=37.7576171, longitude=-122.5776844, bearing=45, pitch=50, zoom=8)


# TOOLTIP_TEXT = {"html": "{id} jobs <br /> Home of commuter in red; work location in green"}
# r = pdk.Deck(arc_layer, initial_view_state=view_state, tooltip=TOOLTIP_TEXT)

st.pydeck_chart(pdk.Deck(
    arc_layer,
    initial_view_state=view_state
    # layers=[hexagon,scatterplot,heatmap]
    # tooltip=TOOLTIP_TEXT
))
