import streamlit as st
import pandas as pd
import requests
import os
import re
import unicodedata
import leafmap.foliumap as leafmap
import urllib


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
Any = object()

@st.cache_data
def slugify(value: Any, allow_unicode: bool = False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


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

def wfs_button(server, url):
    st.session_state.clicked = True
    uri = url +'/wfs?request=GetCapabilities'
    wfs = requests.get(uri, stream=True, allow_redirects=True, verify = False)
    filename = slugify(server)+ ".xml"
    if  (wfs.status_code == 200):               
        f = open(filename, 'wb')                           
        for chunk in wfs.iter_content(chunk_size = 1024):
            if not chunk:
                break
            f.write(chunk)                                                            
        f.close()
    
    if wfs is not None:              
        getcapabilities = open(filename, 'r', encoding='UTF-8') 
        data = getcapabilities.read()
        # st.write(data)
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
            with col2:           
                layer_selected = st.selectbox('Choose a WFS Layer',layer_name)
            uri_geojson = url + "/wfs?request=GetFeature&format_options=CHARSET:UTF-8&typename="+ str(layer_selected).strip() + '&outputFormat=json'
            # geojson = urllib.request.urlretrieve(uri_geojson,slugify(layer_selected))
            m = leafmap.Map(tiles='stamenterrain',toolbar_control=False, layers_control=True)
            wms_url = url + '/ows'
            m.add_wms_layer(
                wms_url, layers=layer_selected, name=slugify(layer_selected), attribution="", transparent=True
            )
            # m.fit_bounds(m.get_bounds(), padding=(30, 30))
            m.to_streamlit(height=600)
            st.write('GeoJSON link: ', uri_geojson)
            # st.download_button(
            #                     label="Download WFS Layer as GeoJSON",
            #                     data=geojson,
            #                     file_name=slugify(layer_selected)+'.geojson',
            #                     mime='text/csv',
            #                 )

st.button('Load WFS Layers', on_click=wfs_button(selected_wfs, selected_url.strip()))

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    pass