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
from folium.plugins import MarkerCluster, FastMarkerCluster, Fullscreen
import pandas as pd
import streamlit_ext as ste
import geopandas as gpd



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

st.title("BecaGIS LatLong Calculator")
st.write('BecaGIS LatLong Calculator is inspired by [Lat Lon Tools](https://plugins.qgis.org/plugins/latlontools/) ')

UTM_FORMATS = ['48N 686261 1192650', '686261,1192650,48N','686261mE,1192650mN,48N', '686261mE,1192650mN,48,N']

antipode_lat_column, antipode_lon_column = None, None
lat_column, lon_column = 'latitude', 'longitude'
col1, col2 = st.columns(2)

@st.cache_data
def get_pos(lat,lon):
    return lat,lon

@st.cache_data
def get_crs_list(): 
    crs_info_list = pyproj.database.query_crs_info(auth_name=None, pj_types=None) 
    crs_list = ["EPSG:" + info[1] + ' (' + info[2] + ') 'for info in crs_info_list] 
    return sorted(crs_list) 

@st.cache_data
def download_csv(df):  
    if not df.empty:
        csv = df.to_csv(encoding ='utf-8')        
        click = ste.download_button(
        label= "Download CSV ",
        data = csv,
        file_name= "becagis.csv",
        mime = "text/csv")        

@st.cache_data      
def download_geojson(df):
    if not df.empty:
        gdf = gpd.GeoDataFrame(
                    df, geometry=gpd.points_from_xy(df[lon_column], df[lat_column])
                )
        geojson = gdf.to_json()  
        ste.download_button(
            label="Download GeoJSON",
            file_name= "becagis.geojson",
            mime="application/json",
            data=geojson
        ) 


with col2:
        ####################################### Settings
    expander = st.expander("⚙️ Settings")
    tab_conversion, tab2 = expander.tabs(["🔁Coordinate Conversion", "Other Settings"])
    tab_conversion.subheader("🔁 Coordinate Conversion Settings")
    with tab_conversion:
        with st.form("Settings"):
            crs_list = get_crs_list()
            target_CRS_text = st.selectbox('🌐Default target CRS/ Projection', crs_list,index = 10080)
            target_CRS = crs_list.index(target_CRS_text)   

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
            if submitted:
                st.caption(":blue[Settings saved sucessfully!]") 

@st.cache_data
def DMS(row):    
    # st.write(row[lat])
    # st.write(lon[lon])
    DMS = formatDmsString(row[lat_column], row[lon_column], dms_mode=0, prec=conversion_settings['DMS_ss_precision'], order=0, delimiter=conversion_settings['DDMMSS_delimeter'], useDmsSpace=conversion_settings['space_DMS_option'], padZeros=conversion_settings['pad_option'], nsewInFront=conversion_settings['NSEW_option'])
    return DMS

@st.cache_data
def DMMM(row):
    D_M_MM = formatDmsString(row[lat_column], row[lon_column], dms_mode=2, prec=conversion_settings['DM_mm_precision'], order=0, delimiter=conversion_settings['DDMMSS_delimeter'], useDmsSpace=conversion_settings['space_DMS_option'], padZeros=conversion_settings['pad_option'], nsewInFront=conversion_settings['NSEW_option'])
    return   D_M_MM   

@st.cache_data
def DDMMSS(row):
    DDMMSS = formatDmsString(row[lat_column], row[lon_column], dms_mode=1, prec=conversion_settings['DMS_ss_precision'], order=0, delimiter=conversion_settings['DDMMSS_delimeter'], useDmsSpace=conversion_settings['space_DMS_option'], padZeros=conversion_settings['pad_option'], nsewInFront=conversion_settings['NSEW_option'])
    return  DDMMSS

@st.cache_data
def UTM(row):
    UTM = utm.latLon2Utm(row[lat_column], row[lon_column], conversion_settings['UTM_precision'], conversion_settings['UTM_format'])
    return UTM

@st.cache_data
def MGRS(row):
    MGRS = mgrs.toMgrs(row[lat_column], row[lon_column], conversion_settings['MGRS_precision'])
    MGRS = formatMgrsString(MGRS, conversion_settings['space_MGRS_option'])
    return MGRS

@st.cache_data
def pluscode(row):
    pluscode = olc.encode(row[lat_column], row[lon_column], conversion_settings['Plus_code_length'])
    return pluscode

@st.cache_data
def geohash_code(row):
    geohash_code = geohash.encode(row[lat_column], row[lon_column], conversion_settings['Geohash_precision'])
    return geohash_code

@st.cache_data
def maidenhead_code(row):
    maidenhead_code = maidenhead.toMaiden(row[lat_column], row[lon_column], conversion_settings['Maidenhead_grid_precision'])
    return maidenhead_code   

@st.cache_data
def georef_code(row):
    georef_code = georef.encode(row[lat_column], row[lon_column], conversion_settings['GEOREF_precision'])
    return georef_code   

@st.cache_data
def w3w(row):
    geocoder = what3words.Geocoder("0HQQGEX8")
    w3w = geocoder.convert_to_3wa(what3words.Coordinates(row[lat_column], row[lon_column]),language = 'vi')
    return w3w['words']      


@st.cache_data
def antipodes(row):
    antipode_lat = - row[lat_column]
    if row[lon_column]< 0:
        antipode_lng = row[lon_column] + 180 
    else: antipode_lng = row[lon_column] - 180  
    return antipode_lat,antipode_lng

@st.cache_data
def transform(row,crs_source, crs_target):
   transformer = Transformer.from_crs(crs_source, crs_target)
   y, x = transformer.transform(row[lat_column],row[lon_column])
   return y, x

with col1:
    url = st.text_input(
        "Enter a CSV URL with Latitude and Longitude Columns",
        'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/us_cities.csv'
    )
    uploaded_file = st.file_uploader("Or upload a CSV file with Latitude and Longitude Columns")
    lat_column_index, lon_column_index = 0,0     
    if url:   
        df = pd.read_csv(url,skiprows=[1],encoding = "UTF-8")                
    if uploaded_file:        
        df = pd.read_csv(uploaded_file,skiprows=[1],encoding = "UTF-8")
    
    for column in df.columns:
            if (column.lower() == 'y' or column.lower().startswith("lat") or column.lower().startswith("n")):
                lat_column_index=df.columns.get_loc(column)
            if (column.lower() == 'x' or column.lower().startswith("ln") or column.lower().startswith("lon") or column.lower().startswith("e") ):
                lon_column_index=df.columns.get_loc(column)
    col1_1, col1_2 = col1.columns(2)
    with col1_1:
        lat_column = col1_1.selectbox('Latitude Column', df.columns, index = lat_column_index)
    with col1_2:
        lon_column = col1_2.selectbox('Longitude Column',df.columns, index = lon_column_index)  

    form = st.form(key="latlon_calculator")
    with form:                          
        # options = ['DMS', 'DMMM', 'DDMMSS' ,'UTM', 'MGRS', 'pluscode', 'geohash', 'maidenhead', 'georef', 'w3w']
        options = ['DMS', 'DMMM', 'DDMMSS' ,'UTM', 'MGRS', 'pluscode', 'geohash_code', 'maidenhead_code', 'georef_code', 'Antipodes', 'Coordinate Transformation']
        check_boxes = [st.checkbox(option, key=option) for option in options]         
        target_CRS_selected = st.selectbox('🌐 Choose a target CRS to transform', crs_list, index = conversion_settings['target_CRS']).split()[0]
        crs_4326 = CRS.from_epsg(4326)         
        submitted = st.form_submit_button("Calculate LatLong")        
        if submitted:
            for option, checked in zip(options, check_boxes):
                if option != 'Antipodes'and option != 'Coordinate Transformation' and checked:
                    if option not in df.columns:
                        df.insert(len(df.columns), option, None)  
                    df[option] = df.apply(locals()[option], axis=1)

                elif option == 'Antipodes'and checked:
                    if 'antipodal_y' and 'antipodal_x' not in df.columns:
                        df.insert(len(df.columns), 'antipodal_y', None)
                        df.insert(len(df.columns), 'antipodal_x', None)
                    df[['antipodal_y','antipodal_x']] = df.apply(antipodes, axis=1, result_type = 'expand')
                
                elif option == 'Coordinate Transformation'and checked:                    
                    if 'transform_y' and 'transform_x' not in df.columns:
                        df.insert(len(df.columns), 'transform_y', None)
                        df.insert(len(df.columns), 'transform_x', None)                                       
                    df[['transform_y','transform_x']] = df.apply(lambda row: transform(row, crs_4326, target_CRS_selected), axis=1, result_type = 'expand')
           
            st.write(df)
            maen_lat_column =  df[lat_column].mean()    
            maen_lon_column =  df[lon_column].mean()
            m = folium.Map(tiles="stamenterrain", location = [maen_lat_column,maen_lon_column], zoom_start =4)
            Fullscreen(                                                         
                position                = "topright",                                   
                title                   = "Open full-screen map",                       
                title_cancel            = "Close full-screen map",                      
                force_separate_button   = True,                                         
            ).add_to(m)             
            cluster = MarkerCluster()
            for i, j in df.iterrows():
                icon=folium.Icon(color='purple', icon='ok-circle')
                # iframe = folium.IFrame(popContent)
                # popup = folium.Popup(popContent,min_width=200,max_width=200) 
                popup = j.to_frame().to_html()
                folium.Marker(location=[df.loc[i,lat_column], df.loc[i, lon_column]], icon=icon, popup=popup).add_to(cluster)
                                                                                                                     
            m.add_child(cluster)            
            folium_static(m, width = 600)
            download_csv(df)
            download_geojson(df)


        
        
    





