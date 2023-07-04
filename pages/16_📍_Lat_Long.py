import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.plugins import MiniMap,Geocoder
from pluscodes import PlusCode, Area, Point


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

# Reference: https://dwtkns.com/srtm30m/

st.title("Lat Long")
# m = folium.Map()
# m.add_child(folium.LatLngPopup())
# st_folium(m, height=500,width=800,returned_objects=[])

def get_pos(lat, lng):
    return lat, lng

m = folium.Map(tiles="stamenterrain", location = [10.78418915150491, 106.70361262696979], zoom_start = 3)

m.add_child(folium.LatLngPopup())
m.add_child(MiniMap(toggle_display=True))
m.add_child(Geocoder(add_marker=True))


map = st_folium(m, width=800)

point = None
if map.get("last_clicked"):
    point = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])
    googleplex = PlusCode(point)

if point is not None:
    st.write(point) # Writes to the app
    st.write(googleplex.code)
    print(point) # Writes to terminal
    print(googleplex.code) # Writes to terminal

