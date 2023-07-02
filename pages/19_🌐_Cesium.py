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
    Thang Quach: [BecaGIS Homepage](https://becagis.vn/?lang=en) | [GitHub Pages](https://thangqd.github.io)
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/quachdongthang) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

st.title("Cesium 3D Map")
html = "./data/html/saigon_buildings.html"
# leafmap.cesium_to_streamlit(html,width=800, height=600, responsive=True, scrolling=False)

HtmlFile = open(html, 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code,height = 500)
