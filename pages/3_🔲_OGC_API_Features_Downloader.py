import streamlit as st
import pandas as pd
import unicodedata
import leafmap.foliumap as leafmap
from urllib.request import urlopen  
import json
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

@st.cache_data
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


st.title("Download Open Data from OGC API Features Server")
st.markdown(
"""
Download Open Data from OGC API Features Server
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
df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/ogc.csv')
wfs_servers = df.server
with col1:
    selected_wfs = st.selectbox('Choose an OGC API Features Server',wfs_servers)
df_filter=df.loc[df['server'] == selected_wfs, ['server','url']].iloc[0]
with col2:
    selected_url = st.text_input('OGC API Features URL', df_filter.url)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def wfs_button(server, url):
    st.session_state.clicked = True
    url_collections = url +'/collections/?f=json'
    try:
        landingpage_response = urlopen(url)
        if (landingpage_response is not None):        
                server_json = json.loads(landingpage_response.read()) 
                server_title = server_json['title']
                server_abstract = server_json['description']
                if len(server_title)>0:
                    with col1:
                        st.write('Server Title: ', server_title)
                if len (server_abstract)>0:
                    with col1:
                        st.write('Server Abstract: ', server_abstract.replace('&#13;','')[:300])          
    except: pass
    collections_response = urlopen(url_collections)
    if collections_response is not None:
        # storing the JSON response from url in data     
            data_json = json.loads(collections_response.read())  
            collections = data_json['collections'] 
            # st.write(collections)
            list = []
            if len(collections) > 0:   
                i = 0
                for i in range (len(collections)):
                    try:
                        list.append( collections[i]['id'])
                    except:
                        list.append( collections[i]['name'])                     
                    
            with col2:
                layer_selected = st.selectbox('Choose an OGC API Features Layer',list)   
    uri_geojson = url + "/collections/"+ str(layer_selected).strip() + '/items?f=json'
    
    m = folium.Map(tiles="cartodbpositron", zoom_start = 2)
    geojson_layer = folium.GeoJson(uri_geojson)
    geojson_layer.add_to(m)
    m.fit_bounds(m.get_bounds(), padding=(30, 30))
    st_folium(m, width=1200,returned_objects=[])
    st.write('GeoJSON link: ', uri_geojson)


st.button('Load OGC API Feature Layers', on_click=wfs_button(selected_wfs, selected_url))

if st.session_state.clicked:
    # The message and nested widget will remain on the page
    pass