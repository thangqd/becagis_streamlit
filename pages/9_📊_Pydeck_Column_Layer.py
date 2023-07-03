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


DATA_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/wqi.csv"
df = pd.read_csv(DATA_URL)

# view = pdk.data_utils.compute_view(df[["longitude", "latitude"]])
# view.pitch = 45
# view.bearing = 0

view_state = pdk.ViewState(latitude=10.045180, longitude=105.78841, bearing=0, pitch=50, zoom=10)


column_layer = pdk.Layer(
    "ColumnLayer",
    data=df,
    get_position=["lon", "lat"],
    get_elevation="wqi",
    elevation_scale=100,
    radius=50,
    get_fill_color=["wqi * 5", "wqi", "wqi * 2", 140],
    pickable=True,
    auto_highlight=True,
)

tooltip = {
    "html": "Water Quality Index: <b>{wqi}</b> ",
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
