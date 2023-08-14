import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests

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


@st.cache_data
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


st.title("Web Feature Service (WFS)")
st.markdown(
"""
This app is a demonstration of loading Web Feature Service (WFS) layers. Simply enter the URL of the WFS service 
in the text box below and press Enter to retrieve the layers.
"""
)
col1, col2 = st.columns(2)
df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/wfs.csv')
wfs_servers = df.server
with col1:
    selected_wfs = st.selectbox('Choose a WFS Server',wfs_servers)
df_filter=df.loc[df['server'] == selected_wfs, ['server','url']].iloc[0]
with col2:
    selected_url = st.text_input('WFS URL', df_filter.url)


if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def wfs_button(url):
    st.session_state.clicked = True
   

st.button('Load WFS Layers', on_click=wfs_button(selected_url))

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    uri = df_filter.url +'/wfs?request=GetCapabilities'
    wfs = requests.get(uri, stream=True, allow_redirects=True, verify = False)
    st.write(wfs)