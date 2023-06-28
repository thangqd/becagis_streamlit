import streamlit as st
import leafmap.foliumap as leafmap

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

# Customize page title
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image("./data/becagis.png", width = 90)
with col2:
    st.title("BecaGIS on Streamlit")

m = leafmap.Map(minimap_control=True,tiles=None)
m.add_basemap("Stamen.Watercolor")
m.to_streamlit(height=500)
st.markdown(
    """
    BecaGIS Streamlit is inspired by [streamlit-geospatial](https://github.com/giswqs/streamlit-geospatial).
    """
)