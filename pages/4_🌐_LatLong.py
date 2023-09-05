import folium
from folium.plugins import Geocoder
from streamlit_folium import st_folium,folium_static
import streamlit as st
from lib import olc
from folium.plugins import Geocoder



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

st.title("LatLong Tools")
st.write('LatLong Tools')


@st.cache_data
def get_pos(lat,lng):
    return lat,lng

@st.cache_data
def pluscode(lat,lng):    
    return PlusCode(lat, lng).code


m = folium.Map(tiles="stamenterrain")
# m = folium.Map( tiles = 'https://grid.plus.codes/grid/tms/{z}/{x}/{y}.png', attr='Google Plus Code Grid')
markers = m.add_child(folium.ClickForMarker())
# folium.Rectangle([(28.6471948,76.9531796), (19.0821978,72.7411)]).add_to(m)
Geocoder(default_css = [('Control.Geocoder.css', './data/css/Control.Geocoder.css')]).add_to(m)


map = st_folium(m, width = 800)
# map = st_folium(m)

if map['last_clicked'] is not None:
    lat, lng = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
    st.write('Clicked point: ',lat, lng) 
    pluscode = olc.encode(lat, lng, 15)
    plusdecode = olc.decode(pluscode)
    st.write('Plus Code: ',pluscode) # from 10 to 15
    st.write('Plus Decode: ',plusdecode) # from 10 to 15


