import streamlit as st
import leafmap
import streamlit.components.v1 as components

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
st.title("Cesium 3D Map")
html = "./data/html/saigon_buildings.html"
# html = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/html/saigon_buildings.html"
# leafmap.cesium_to_streamlit(html,width=800, height=600, responsive=True, scrolling=False)

with open(html, 'r', encoding='utf-8') as f: 
    html_data = f.read()

components.html(html_data,height = 500)
