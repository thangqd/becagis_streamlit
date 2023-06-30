import streamlit as st
import leafmap.deck as leafmap
import geopandas as gpd
from gadm import GADMDownloader


# st.set_page_config(
#     page_title="prettymapp", page_icon="🖼️", initial_sidebar_state="collapsed"
# )
st.set_page_config(layout="wide",page_icon="🖼️")

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


downloader = GADMDownloader(version="4.0")

country_name = "Vietnam"
ad_level = 0
gdf = downloader.get_shape_data_by_country_name(country_name=country_name, ad_level=ad_level)
m = leafmap.Map()
m.add_gdf(gdf)
st.pydeck_chart(m)
