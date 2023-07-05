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
    [GitHub](https://github.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)
st.title("Pydeck Column Layer")


DATA_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/cali_earthquakes.csv"
df = pd.read_csv(DATA_URL)

# view = pdk.data_utils.compute_view(df[["longitude", "latitude"]])
# view.pitch = 45
# view.bearing = 0

view_state = pdk.ViewState(latitude=36.06408069950445, longitude=-119.26794393426914, bearing=0, pitch=50, zoom=8)

column_layer = pdk.Layer(
    "ColumnLayer",
    data=df,
    get_position=["lon", "lat"],
    get_elevation="y",
    elevation_scale=1000,
    radius=50,
    get_fill_color=["y * 200", "y", "y * 2", 140],
    pickable=True,
    auto_highlight=True,
)

tooltip = {
    "html": "Earquake Magnitude: <b>{y}</b> ",
    "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}

r = pdk.Deck(
    column_layer,
    initial_view_state=view_state,
    tooltip=tooltip,
    map_provider="mapbox",
    # map_style=pdk.map_styles.SATELLITE,
    map_style=None,
)

st.pydeck_chart(r)
