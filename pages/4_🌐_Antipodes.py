import folium
from folium.plugins import Geocoder
from streamlit_folium import st_folium,folium_static
import streamlit as st

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

st.title("Antipodes")
st.write('Aptiodal Point')


@st.cache_data
def get_pos(lat,lng):
    return lat,lng

@st.cache_data
def antipodes(lat,lng):
    antipode_lat = - lat
    if lng< 0:
        antipode_lng = lng + 180 
    else: antipode_lng = lng - 180  
    return antipode_lat,antipode_lng

col1, col2 = st.columns(2)

# dualmap= folium.plugins.DualMap(tiles="stamenterrain")
# markers = dualmap.m1.add_child(folium.ClickForMarker())
# map = st_folium(dualmap)

# if dualmap.m1['last_clicked'] is not None:
#     lat, lng = get_pos(dualmap.m1['last_clicked']['lat'],dualmap.m1['last_clicked']['lng'])
#     st.write('Clicked point: ',lat, lng)        

antipode_lat = None
antipode_lng = None
zoom = 1
with col1:
    m = folium.Map(tiles="stamenterrain")
    markers = m.add_child(folium.ClickForMarker())
    map = st_folium(m, width = 500, height = 410)
    # map = st_folium(m)
    zoom = map['zoom']
    if map['last_clicked'] is not None:
        lat, lng = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
        st.write('Clicked point: ',lat, lng) 
        antipode_lat,antipode_lng = antipodes(lat,lng)       

with col2:
    antipodal_m = folium.Map(tiles="stamenterrain",zoom_start = zoom) 
    if antipode_lat is not None:
        folium.Marker(location=[antipode_lat, antipode_lng], popup='Latitude: '+ str('{:.4f}'.format(antipode_lat)) + '\nLongitude: ' + str('{:.4f}'.format(antipode_lng))
                ).add_to(antipodal_m)  
      
    antipodal_map = st_folium(antipodal_m,width = 500, height = 400) 
    # antipodal_map = st_folium(antipodal_m,width=600, height = 500) 
    # antipodal_map = folium_static(antipodal_m) 
    st.write('Antipodal point: ', antipode_lat,antipode_lng)
      
