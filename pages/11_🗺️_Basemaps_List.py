import streamlit as st
import leafmap.leafmap as leafmap


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
st.title("Basemaps List")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map()  
        basemaps = list(leafmap.basemaps.keys())[0:20]
        for basemap in basemaps:
            m.add_basemap(basemap)  
m.to_streamlit(height=700)
