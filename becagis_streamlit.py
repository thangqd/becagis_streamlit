import streamlit as st
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
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/quachdongthang) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

# Customize page title
st.title("BecaGIS on Streamlit")

m = leafmap.Map(minimap_control=True)
m.add_basemap("Stamen.Watercolor")
m.to_streamlit(height=500)
st.markdown(
    """
    BecaGIS Streamlit is inspired by [streamlit-geospatial](https://github.com/giswqs/streamlit-geospatial).
    """
)