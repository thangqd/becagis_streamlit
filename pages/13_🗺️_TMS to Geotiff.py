import streamlit as st
import leafmap.leafmap as leafmap
import os
import leafmap
import torch
from samgeo import SamGeo, tms_to_geotiff

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
st.title(" Segment Anything Model (SAM)")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map(center=[29.676840, -95.369222], zoom=19)
        m.add_basemap('SATELLITE')
        if m.user_roi is not None:
            bbox = m.user_roi_bounds()
        else:
            bbox = [-122.5216, 37.733, -122.3661, 37.8095]
        leafmap.tms_to_geotiff('satellite.tif', bbox, zoom=13, source='Satellite')

m.to_streamlit(height=700)
