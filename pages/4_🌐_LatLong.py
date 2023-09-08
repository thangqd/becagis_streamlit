import folium
from folium.plugins import Geocoder
from streamlit_folium import st_folium,folium_static
import streamlit as st
from becalib.latlong import parseDMSString, formatDmsString, formatMgrsString 
import pyproj
from pyproj import CRS, Transformer
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info
import what3words
from  becalib import olc, mgrs, geohash, maidenhead, georef, utm


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

UTM_FORMATS = ['48N 686261 1192650', '686261,1192650,48N','686261mE,1192650mN,48N', '686261mE,1192650mN,48,N']
COORDINATE_ODERS = ('Lat,Lon (Y,X) Googlemaps Order', 'Lon,Lat (X,Y) Order')

@st.cache_data
def get_pos(lat,lng):
    return lat,lng

@st.cache_data
def get_crs_list(): 
    crs_info_list = pyproj.database.query_crs_info(auth_name=None, pj_types=None) 
    crs_list = ["EPSG:" + info[1] + ' (' + info[2] + ') 'for info in crs_info_list] 
    return sorted(crs_list) 

@st.cache_data
def antipodes(lat,lng):
    antipode_lat = - lat
    if lng< 0:
        antipode_lng = lng + 180 
    else: antipode_lng = lng - 180  
    return antipode_lat,antipode_lng


antipode_lat = None
antipode_lng = None

col1, col2 = st.columns(2)
with col1: 
    m = folium.Map(tiles="stamenterrain", location = [10.77588,106.70388], zoom_start =15)
    # m = folium.Map( tiles = 'https://grid.plus.codes/grid/tms/{z}/{x}/{y}.png', attr='Google Plus Code Grid')
    markers = m.add_child(folium.ClickForMarker())
    # folium.Rectangle([(28.6471948,76.9531796), (19.0821978,72.7411)]).add_to(m)
    # Geocoder(default_css = [('Control.Geocoder.css', 'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/css/Control.Geocoder.css')]).add_to(m)

    map = st_folium(m, width = 800, height = 450)
    # map = st_folium(m)
with col2:
        ####################################### Settings
    expander = st.expander("⚙️ Settings")
    tab_conversion, tab2 = expander.tabs(["🔁Coordinate Conversion", "🗃 Data"])
    tab_conversion.subheader("🔁 Coordinate Conversion Settings")
    with tab_conversion:
        with st.form("Settings"):
            crs_list = get_crs_list()
            target_CRS_text = st.selectbox('🌐Default target CRS/ Projection', crs_list,index = 10080)
            target_CRS = crs_list.index(target_CRS_text)        

            coordinate_order_selected= st.selectbox('Coordinate order for decimal or and DMS notations', COORDINATE_ODERS)
            coordinate_order = COORDINATE_ODERS.index(coordinate_order_selected)

            st.divider()
            tab_conversion_col1, tab_conversion_col2 = st.columns(2)
            with tab_conversion_col1: 
                epsg_4326_precision = st.number_input(
                        "EPSG:4326 Decimal degree precision",
                        min_value=0,
                        value = 8,
                        max_value=32,
                        key="epsg_4326_precision",
                    )
                DMS_ss_precision = st.number_input(
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

            with tab_conversion_col2:                
                other_precision = st.number_input(
                        "Other Decimal degree precision",
                        min_value=0,
                        value = 4,
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
                UTM_format_selected = st.selectbox('UTM Format', UTM_FORMATS)
                UTM_format = UTM_FORMATS.index(UTM_format_selected)


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
                    value = ', '    ,        
                    key="DDMMSS_delimeter",
                )
            st.divider()
            space_DMS_option = st.checkbox('Add space between DMS.ss and DM.mm numbers', value=True)
            pad_option = st.checkbox('Pad DMS.ss and DM.mm output coordinates with leading zeroes', value=False)
            NSEW_option = st.checkbox('Format DMS coordinates with NSEW at the beginning', value=False)
            space_MGRS_option = st.checkbox('Add spaces to MGRS coordinates', value=False)
            conversion_settings = {
                            "target_CRS": target_CRS,
                            "coordinate_order": coordinate_order,
                            "epsg_4326_precision": epsg_4326_precision,
                            "DMS_ss_precision": DMS_ss_precision,
                            "UTM_precision": UTM_precision,
                            "MGRS_precision": MGRS_precision,
                            "Geohash_precision": Geohash_precision,
                            "GEOREF_precision":GEOREF_precision ,
                            "Delimeter_coordinates": Delimeter_coordinates,
                            "other_precision": other_precision,
                            "DM_mm_precision": DM_mm_precision,
                            "UTM_format": UTM_format,
                            "Plus_code_length": Plus_code_length,
                            "Maidenhead_grid_precision": Maidenhead_grid_precision,
                            "DDMMSS_delimeter": DDMMSS_delimeter,
                            "space_DMS_option": space_DMS_option,
                            "pad_option": pad_option,
                            "NSEW_option": NSEW_option,
                            "space_MGRS_option": space_MGRS_option                           
                            }
            submitted = st.form_submit_button("Submit")
            # if submitted:
            #     st.write("conversion_settings", conversion_settings)

    if map['last_clicked'] is not None:
        lat, lng = get_pos(map['last_clicked']['lat'],map['last_clicked']['lng'])
        if conversion_settings['coordinate_order']== 0:
            wgs84_coordinates = '{:.{prec}f}{}{:.{prec}f}'.format(lat, conversion_settings['DDMMSS_delimeter'], lng, prec=conversion_settings['epsg_4326_precision'])
        elif conversion_settings['coordinate_order'] == 1:
            wgs84_coordinates = '{:.{prec}f}{}{:.{prec}f}'.format(lng, conversion_settings['DDMMSS_delimeter'], lat, prec=conversion_settings['epsg_4326_precision'])
        st.caption(":red[Clicked point (WGS84 CRS): ]") 
        st.code(wgs84_coordinates)
        
        DMS = formatDmsString(lat, lng, dms_mode=0, prec=conversion_settings['DMS_ss_precision'], order=conversion_settings['coordinate_order'], delimiter=conversion_settings['DDMMSS_delimeter'], useDmsSpace=conversion_settings['space_DMS_option'], padZeros=conversion_settings['pad_option'], nsewInFront=conversion_settings['NSEW_option'])
        st.caption("➝ :blue[D M S.ss: ]") 
        st.code(DMS) 
    
        D_M_MM = formatDmsString(lat, lng, dms_mode=2, prec=conversion_settings['DM_mm_precision'], order=conversion_settings['coordinate_order'], delimiter=conversion_settings['DDMMSS_delimeter'], useDmsSpace=conversion_settings['space_DMS_option'], padZeros=conversion_settings['pad_option'], nsewInFront=conversion_settings['NSEW_option'])
        st.caption("➝ :blue[D M.mm: ]")
        st.code(D_M_MM)

        DDMMSS = formatDmsString(lat, lng, dms_mode=1, prec=conversion_settings['DMS_ss_precision'], order=conversion_settings['coordinate_order'], delimiter=conversion_settings['DDMMSS_delimeter'], useDmsSpace=conversion_settings['space_DMS_option'], padZeros=conversion_settings['pad_option'], nsewInFront=conversion_settings['NSEW_option'])
        st.caption("➝ :blue[DDMMSS: ]") 
        st.code(DDMMSS)

        # st.write(pyproj.pj_list)
        # st.write(pyproj.get_codes('EPSG', 'CRS'))
        target_CRS_selected = st.selectbox('🌐 Choose a target CRS', crs_list, index = conversion_settings['target_CRS']).split()[0]
        crs_4326 = CRS.from_epsg(4326)
        try: 
            crs_target = CRS.from_user_input(target_CRS_selected)
            # st.code(crs_target)
            # st.code(crs_target.to_wkt(pretty=True))
            transformer = Transformer.from_crs(crs_4326, crs_target)
            y,x = transformer.transform(lat,lng)
            if conversion_settings['coordinate_order']== 0:
                target_crs_coordinates = '{:.{prec}f}{}{:.{prec}f}'.format(y, conversion_settings['DDMMSS_delimeter'], x, prec=conversion_settings['other_precision'])
            elif conversion_settings['coordinate_order'] == 1:
                target_crs_coordinates = '{:.{prec}f}{}{:.{prec}f}'.format(x, conversion_settings['DDMMSS_delimeter'], y, prec=conversion_settings['other_precision'])
            st.caption("➝ :blue[Coordinates in chosen target CRS:]") 
            st.code(target_crs_coordinates)
            # st.write(target_CRS_selected,': ', y, x)        
        except:
            st.warning('⚠️ No transform available between EPSG:4326 and the chosen target CRS')
        
        # UTM = utm.latLon2Utm(lat, lng, conversion_settings['UTM_precision'], conversion_settings['UTM_format'])
        UTM = utm.latLon2Utm(lat, lng, conversion_settings['UTM_precision'], conversion_settings['UTM_format'])
        st.caption("➝ :blue[Standard UTM: ]") 
        st.code(UTM)

        try:
            MGRS = mgrs.toMgrs(lat, lng, conversion_settings['MGRS_precision'])
            MGRS = formatMgrsString(MGRS, conversion_settings['space_MGRS_option'])
            st.caption("➝ :blue[MGRS:]") 
            st.code(MGRS)
        except:
            st.warning('⚠️ MGRS transformation error!')

        try:
            pluscode = olc.encode(lat, lng, conversion_settings['Plus_code_length'])
            # plusdecode = olc.decode(pluscode)
            st.caption("➝ :blue[Plus Code: ]")
            st.code(pluscode)
        except:
            st.warning('⚠️ Pluscode transformation error!')
        
        try:
            geohash_code = geohash.encode(lat, lng, conversion_settings['Geohash_precision'])
            st.caption("➝ :blue[Geohash: ]")
            st.code(geohash_code)
        except:
            st.warning('⚠️ Geohash transformation error!')
        
        try:
            maidenhead_code = maidenhead.toMaiden(lat, lng, conversion_settings['Maidenhead_grid_precision'])
            st.caption("➝ :blue[Maidenhead Grid: ]")
            st.code(maidenhead_code)
        except:
            st.warning('⚠️ Maidenhead transformation error!')
        
        try:
            georef_code = georef.encode(lat, lng, conversion_settings['GEOREF_precision'])
            st.caption("➝ :blue[GEOREF: ]")
            st.code(georef_code)
        except Exception:
            st.warning('⚠️ GEOREF transformation error!')
        

        try:
            geocoder = what3words.Geocoder("0HQQGEX8")
            w3w = geocoder.convert_to_3wa(what3words.Coordinates(lat, lng),language = 'vi')
            st.caption("➝ :blue[What3words: ]")
            st.code(w3w['words'])
        except Exception:
            st.warning('⚠️ What3words transformation error!')     
     
        with col1:            
            antipode_lat,antipode_lng = antipodes(lat,lng)     
            if conversion_settings['coordinate_order']== 0:
                antipodal_coordinates = '{:.{prec}f}{}{:.{prec}f}'.format(antipode_lat, conversion_settings['DDMMSS_delimeter'], antipode_lng, prec=conversion_settings['other_precision'])
            elif conversion_settings['coordinate_order'] == 1:
                antipodal_coordinates = '{:.{prec}f}{}{:.{prec}f}'.format(antipode_lng, conversion_settings['DDMMSS_delimeter'], antipode_lat, prec=conversion_settings['other_precision'])
            st.caption("➝ :blue[Antipodal Coordinates:]") 
            st.code(antipodal_coordinates)

            antipodal_m = folium.Map(tiles="stamenterrain",zoom_start = 12) 
            if antipode_lat is not None:
                folium.Marker(location=[antipode_lat, antipode_lng], popup='Latitude: '+ str('{:.4f}'.format(antipode_lat)) + '\nLongitude: ' + str('{:.4f}'.format(antipode_lng))
                        ).add_to(antipodal_m)  

            antipodal_map = folium_static(antipodal_m, width = 510, height = 450) 
            
        
    





