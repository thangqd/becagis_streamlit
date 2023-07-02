import streamlit as st
import leafmap.leafmap as leafmap
import os
import leafmap
import torch
from samgeo import SamGeo, tms_to_geotiff

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


st.title(" Download OSM Data")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map(toolbar_control=False, layers_control=True)
        # try: 
            # gdf = leafmap.osm_gdf_from_place("New York City", tags={"amenity": "bar"})
            # m.add_gdf(gdf, layer_name='New York City')
        m.add_osm_from_point(
                        center_point=(46.7808, -96.0156),
                        tags={"natural": "water"},
                        dist=10000,
                        layer_name="Lakes",
                    )
        # except: 
        #     pass
        m
# m.to_streamlit(height=700)

