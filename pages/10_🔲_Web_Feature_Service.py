import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import requests
import os
import re

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
    uri = url +'/wfs?request=GetCapabilities'
    wfs = requests.get(uri, stream=True, allow_redirects=True, verify = False)
    filename = "wfs.xml"  
    if  (wfs.status_code == 200):               
        f = open(filename, 'wb')                           
        for chunk in wfs.iter_content(chunk_size = 1024):
            if not chunk:
                break
            f.write(chunk)                                                            
        f.close()
    if wfs is not None:              
        getcapabilities = open(filename, 'r') 
        data = getcapabilities.read()
        getcapabilities.close()
        os.remove(filename)
        server_title_regex = r'<ows:Title>(.+?)</ows:Title>|<ows:Title/>'
        
        server_abstract_regex = r'<ows:Abstract>(.+?)</ows:Abstract>|<ows:Abstract/>'
        
        server_title = re.findall(server_title_regex,data,re.DOTALL)
        server_abstract = re.findall(server_abstract_regex,data,re.DOTALL)

        layer_name_regex = r'<Name>(.+?)</Name>'
        layer_title_regex = r'<Title>(.+?)</Title>|<Title/>'


        layer_name = re.findall(layer_name_regex,data,re.DOTALL)
        layer_title = re.findall(layer_title_regex,data,re.DOTALL)

        if len(server_title)>0:
            with col1:
                st.write('Server Title: ', server_title[0])

        if len (server_abstract)>0:
            with col1:
                st.write('Server Abstract: ', server_abstract[0].replace('&#13;',''))
        
        if len(layer_name)>0:
            st.write(layer_name)
        if len(layer_title)>0:
            st.write(layer_title)
        


st.button('Load WFS Layers', on_click=wfs_button(selected_url))

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    pass