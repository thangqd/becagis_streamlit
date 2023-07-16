import streamlit as st
import pandas as pd
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
st.title("Pydeck Polygon")

DATA_URL = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/vn_districts.geojson"
view_state = pdk.ViewState(
    # latitude=10.045180, longitude=105.78841, zoom=6, max_zoom=20, pitch=40.5
    latitude=15.873434435958258, longitude= 107.84285586747781, zoom=4, max_zoom=20, pitch=20
)

geojson = pdk.Layer(
    'GeoJsonLayer',
    DATA_URL,
    opacity=0.8,
    stroked=False,
    filled=True,
    extruded=True,
    wireframe=True,
    get_elevation='properties.pop_dens',
    get_fill_color='[properties.pop_dens,255, 125]',
    get_line_color=[255, 255, 255],
    elevation_scale=2,
    auto_highlight=True,
    pickable=True
)

tooltip = {
    "html": "District: <b>{name}</b> </br> Population Density: <b>{pop_dens}</b> ",
    # "text": "Population Density: {pop_den}"
     "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"},
}



r = pdk.Deck(
    layers=[geojson],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_provider="mapbox",
    # map_style=pdk.map_styles.SATELLITE,
    map_style=None,
)

st.pydeck_chart(r)
