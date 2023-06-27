import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import sys, os
import leafmap.foliumap as leafmap


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

with st.expander("See source code"):
    with st.echo():
        laz = './data/pentagon.laz'   
leafmap.view_lidar(laz, cmap='terrain', backend='pyvista')
   