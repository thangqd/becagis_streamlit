import folium
from folium.plugins import Geocoder
from streamlit_folium import st_folium,folium_static
import streamlit as st
from lib import olc
from lib.latlong import parseDMSString, formatDmsString, formatMgrsString 
from folium.plugins import Geocoder
import pyproj
from pyproj import CRS, Transformer
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info
import what3words


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
def get_crs_list(): 
    crs_info_list = pyproj.database.query_crs_info(auth_name=None, pj_types=None) 
    # st.write(crs_info_list)
    crs_list = ["EPSG:" + info[1] + ' (' + info[2] + ') ' + info[5][4] for info in crs_info_list] 
    # print(crs_list) 
    return sorted(crs_list) 



m = folium.Map(tiles="stamenterrain", location = [10.77588,106.70388], zoom_start =15)
# m = folium.Map( tiles = 'https://grid.plus.codes/grid/tms/{z}/{x}/{y}.png', attr='Google Plus Code Grid')
markers = m.add_child(folium.ClickForMarker())
# folium.Rectangle([(28.6471948,76.9531796), (19.0821978,72.7411)]).add_to(m)
Geocoder(default_css = [('Control.Geocoder.css', 'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/css/Control.Geocoder.css')]).add_to(m)


map = st_folium(m, width = 800)
# map = st_folium(m)

if map['last_clicked'] is not None:
    lat, lng = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
    st.write('Clicked point: ',lat, lng) 
    pluscode = olc.encode(lat, lng, 15)
    plusdecode = olc.decode(pluscode)
    st.write('Plus Code: ',pluscode) # from 10 to 15
    st.write('Plus Decode: ',plusdecode) 
    DMS = formatDmsString(lat, lng, dms_mode=0, prec=2, order=0, delimiter=', ', useDmsSpace=True, padZeros=False, nsewInFront=False)
    st.write("D M' S: ",DMS) 
    D_M_MM = formatDmsString(lat, lng, dms_mode=2, prec=2, order=0, delimiter=', ', useDmsSpace=True, padZeros=False, nsewInFront=False)
    st.write("D M.MM",D_M_MM) 
    DDMMSS = formatDmsString(lat, lng, dms_mode=1, prec=2, order=0, delimiter=', ', useDmsSpace=True, padZeros=False, nsewInFront=False)
    st.write("DDMMSS",DDMMSS) 
    # st.write(pyproj.pj_list)
    # st.write(pyproj.get_codes('EPSG', 'CRS'))
    crs = CRS.from_epsg(9210)
    st.write(crs)
    st.write(crs.to_wkt(pretty=True))
    crs_4326 = CRS.from_epsg(4326)
    crs_9210 = CRS.from_epsg(9210)
    transformer = Transformer.from_crs(crs_4326, crs_9210)
    y,x = transformer.transform(lat,lng)
    st.write("EPSG:9210",y, x)
    crs_list = get_crs_list()
    selected_EPSG = st.selectbox('Select an EPSG Code', crs_list,index = 10080)
    st.write(selected_EPSG, crs_list.index(selected_EPSG))
    geocoder = what3words.Geocoder("0HQQGEX8")
    w3w = geocoder.convert_to_3wa(what3words.Coordinates(lat, lng),language = 'vi')
    st.write("What3words: ",w3w['words'])

