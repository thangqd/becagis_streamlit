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
import pyperclip


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

UTM_format = ['15N 755631 4283168', '755631,4283168,15N','755631mE,4283168mN,15N', '755631mE,4283168mN,15,N']

@st.cache_data
def get_pos(lat,lng):
    return lat,lng

@st.cache_data
def get_crs_list(): 
    crs_info_list = pyproj.database.query_crs_info(auth_name=None, pj_types=None) 
    crs_list = ["EPSG:" + info[1] + ' (' + info[2] + ') 'for info in crs_info_list] 
    return sorted(crs_list) 

col1, col2 = st.columns(2)
with col1: 
    m = folium.Map(tiles="stamenterrain", location = [10.77588,106.70388], zoom_start =15)
    # m = folium.Map( tiles = 'https://grid.plus.codes/grid/tms/{z}/{x}/{y}.png', attr='Google Plus Code Grid')
    markers = m.add_child(folium.ClickForMarker())
    # folium.Rectangle([(28.6471948,76.9531796), (19.0821978,72.7411)]).add_to(m)
    Geocoder(default_css = [('Control.Geocoder.css', 'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/css/Control.Geocoder.css')]).add_to(m)

    map = st_folium(m, height = 400)
    # map = st_folium(m)

with col2:
    if map['last_clicked'] is not None:
        lat, lng = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
        st.write('Clicked point: ',lat, lng) 
        pluscode = olc.encode(lat, lng, 15)
        plusdecode = olc.decode(pluscode)
        c1, c2= st.columns(2) 
        c1.caption('Plus Code: ') 
        c2.code(pluscode, language='markdown')        
        # a=st.text_input('Plus Code: ', pluscode, disabled=True)
        # if st.button('Copy'):
        #     pyperclip.copy(a)
        #     st.success('Text copied successfully!')

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
        st.code(crs)
        st.code(crs.to_wkt(pretty=True))
        crs_4326 = CRS.from_epsg(4326)
        crs_9210 = CRS.from_epsg(9210)
        transformer = Transformer.from_crs(crs_4326, crs_9210)
        y,x = transformer.transform(lat,lng)
        st.write("EPSG:9210",y, x)
        
        
        geocoder = what3words.Geocoder("0HQQGEX8")
        w3w = geocoder.convert_to_3wa(what3words.Coordinates(lat, lng),language = 'vi')
        st.write("What3words: ",w3w['words'])

    expander = st.expander("⚙️ Settings")
    tab_convert, tab2 = expander.tabs(["🔁Coordinate Conversion", "🗃 Data"])
    tab_convert.subheader("🔁 Coordinate Conversion Settings")
    with tab_convert:
        crs_list = get_crs_list()
        target_CRS = st.selectbox('🌐Default target CRS/ Projection', crs_list,index = 10080)
        coordinate_order= st.selectbox('Coordinate order for decimal or and DMS notations', ['Lat,Lon (Y,X) Googlemaps Order', 'Lon,Lat (X,Y) Order'])
        tab_convert_col1, tab_convert_col2 = st.columns(2)
        with tab_convert_col1: 
            epsg_4326_precision = st.number_input(
                    "EPSG:4326 Decimal degree precision",
                    min_value=0,
                    value = 8,
                    max_value=32,
                    key="epsg_4326_precision",
                )
            DMS_ss_seconds_precision = st.number_input(
                "DMS.ss seconds precision",
                min_value=0,
                value = 0,
                max_value=16,
                key="DMS_ss_seconds_precision",
            )
            UTM_precision = st.number_input(
                "UTM precision",
                min_value=0,
                value = 0,
                max_value=16,
                key="UTM_precision",
            )
            MGRS_precision = st.number_input(
                "MGRS precision",
                min_value=0,
                value = 5,
                max_value=5,
                key="MGRS_precision",
            )
            Geohash_precision = st.number_input(
                "Geohash precision",
                min_value=1,
                value = 12,
                max_value=30,
                key="Geohash_precision",
            )
            GEOREF_precision = st.number_input(
                "GEOREF precision",
                min_value=0,
                value = 5,
                max_value=10,
                key="GEOREF_precision",
            )

            Delimeter_coordinates = st.text_input(
                "Delimeter between coordinate pairs",    
                value = ','    ,        
                key="Delimeter_coordinates",
            )

        with tab_convert_col2: 
            other_precision = st.number_input(
                    "Other Decimal degree precision",
                    min_value=0,
                    value = 2,
                    max_value=32,
                    key="other_precision",
                )           
            DM_mm_precision = st.number_input(
                    "DM.mm precision",
                    min_value=0,
                    value = 4,
                    max_value=16,
                    key="DM_mm_precision",
                )        
            UTM_format = st.selectbox('UTM Format', UTM_format)
            Plus_code_length = st.number_input(
                "Google Plus code length",
                min_value=10,
                value = 13,
                max_value=15,
                key="Plus_code_length",
            )
            Maidenhead_grid_precision = st.number_input(
                "Maiden head grid precision",
                min_value=1,
                value = 3,
                max_value=4,
                key="Maidenhead_grid_precision",
            )
            DDMMSS_delimeter = st.text_input(
                "DDMMSS Delimeter",    
                value = ','    ,        
                key="DDMMSS_delimeter",
            )
        space_DMS_option = st.checkbox('Add space between DMS.ss and DM.mm numbers', value=True)
        pad_option = st.checkbox('Pad DMS.ss and DM.mm output coordinates with leading zeroes', value=False)
        NSEW_option = st.checkbox('Format DMS coordinates with NSEW at the beginning', value=False)
        space_MGRS_option = st.checkbox('Add spaces to MGRS coordinates', value=False)
        
    





