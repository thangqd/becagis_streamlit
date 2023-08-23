import folium
import folium.plugins
from streamlit_folium import st_folium
import streamlit as st

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

col1, col2 = st.columns([1,1])

# dualmap= folium.plugins.DualMap(tiles="stamenterrain")
# markers = dualmap.m1.add_child(folium.ClickForMarker())
# map = st_folium(dualmap)

# if dualmap.m1['last_clicked'] is not None:
#     lat, lng = get_pos(dualmap.m1['last_clicked']['lat'],dualmap.m1['last_clicked']['lng'])
#     st.write('Clicked point: ',lat, lng)        


with col1:
    m = folium.Map(tiles="stamenterrain")
    markers = m.add_child(folium.ClickForMarker())
    map = st_folium(m, width=500, height = 500)
    if map['last_clicked'] is not None:
        lat, lng = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
        st.write('Clicked point: ',lat, lng)        

with col2:
    antipodal_m = folium.Map(tiles="stamenterrain") 
    antipodal_map = st_folium(antipodal_m,width=500, height = 500)   
    if map['last_clicked'] is not None:
        antipode_lat,antipode_lng = antipodes(lat,lng)
        folium.Marker(location=[antipode_lat, antipode_lng]
              ).add_to(antipodal_m)        
        st.write('Antipodal point: ', antipode_lat,antipode_lng)

