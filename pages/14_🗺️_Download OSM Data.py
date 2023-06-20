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
st.title(" Download OSM Data")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map(toolbar_control=False, layers_control=True)
        # m.add_osm_from_geocode("New York City", layer_name='NYC')        
        m = leafmap.Map(toolbar_control=False, layers_control=True)
        # m.add_osm_from_geocode("Chicago, Illinois", layer_name='Chicago, IL')
        gdf = leafmap.osm_gdf_from_place("New York City", tags={"amenity": "bar"})
st.write(gdf)        
m.to_streamlit(height=700)

