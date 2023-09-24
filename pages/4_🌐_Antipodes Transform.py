import folium
from streamlit_folium import st_folium,folium_static
import streamlit as st
from becalib.latlong import parseDMSString, formatDmsString, formatMgrsString 
from pyproj.database import query_utm_crs_info
from folium.plugins import MarkerCluster, FastMarkerCluster, Fullscreen
import pandas as pd
import streamlit_ext as ste
import geopandas as gpd
import fiona, os
import leafmap
from shapely.geometry import Point, LineString, Polygon


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

st.title("BecaGIS Antipodes Transform")
st.write('BecaGIS Antipodes Transform')
col1, col2 = st.columns(2)    

def download_geojson(gdf, layer_name):
    if not gdf.empty:        
        geojson = gdf.to_json()  
        with col2:
            ste.download_button(
                label="Download GeoJSON",
                file_name= 'antipodes_' + layer_name+ '.geojson',
                mime="application/json",
                data=geojson
            ) 

def antipodes(lon, lat):
    antipode_lat = -lat
    if lon< 0:
        antipode_lon = lon + 180 
    else: antipode_lon = lon - 180  
    return antipode_lon, antipode_lat

def antipode_lon(lon):
    if lon< 0:
        antipode_lon = lon + 180 
    else: antipode_lon = lon - 180  
    return antipode_lon

def antipode_lat(lat):
    antipode_lat = -lat
    return antipode_lat


def antipode_line(p):
    coords = list(p.coords)
    coords = [Point(antipode_lon(p[0]), antipode_lat(p[1])) for p in coords] 
    return LineString(coords)

def antipode_polygon(p):
    coords = list(p.exterior.coords)
    coords = [Point(antipode_lon(p[0]), antipode_lat(p[1])) for p in coords] 
    return Polygon(coords)

def antipodes_transform(source): 
    if (source.geometry.type == 'Point').all():
        geometry = [Point(antipodes(lon, lat)) for lon, lat in zip(source.geometry.x, source.geometry.y)]
        target = gpd.GeoDataFrame(source, geometry=geometry)        
        return target
    elif (source.geometry.type == 'MultiPoint').all():
        source = source.explode(index_parts=False)
        geometry = [Point(antipodes(lon, lat)) for lon, lat in zip(source.geometry.x, source.geometry.y)]
        target = gpd.GeoDataFrame(source, geometry=geometry) 
        target = target.dissolve(by = target.index)  
        return target
    
    elif (source.geometry.type == 'LineString').all():
        source['points'] = gdf.apply(lambda x: [y for y in x['geometry'].coords], axis=1)
        source.to_dict('records')     
        target = source
        target['geometry'] = target.geometry.map(antipode_line) 
        target = target.drop(['points'], axis=1)        
        return target    
    elif (source.geometry.type == 'MultiLineString').all():
        source = source.explode(index_parts=False)
        source['points'] = gdf.apply(lambda x: [y for y in x['geometry'].geoms[0].coords], axis=1)
        source.to_dict('records')      
        target = source
        target['geometry'] = target.geometry.map(antipode_line) 
        target = target.drop(['points'], axis=1)
        target = target.dissolve(by = target.index)
        return target
    
    elif (source.geometry.type == 'Polygon').all():
        source['points'] = source.geometry.apply(lambda x: list(x.exterior.coords))
        target = source
        target['geometry'] = target.geometry.map(antipode_polygon) 
        target = target.drop(['points'], axis=1)
        return target  

    elif (source.geometry.type == 'MultiPolygon').all():
        source = source.explode(index_parts=False)
        source['points'] = source.geometry.apply(lambda x: list(x.exterior.coords))
        target = source
        target['geometry'] = target.geometry.map(antipode_polygon) 
        target = target.drop(['points'], axis=1)
        target = target.dissolve(by = target.index)
        return target  
    
    else:
        st.warning('Cannot create Antipodes!')
        return source

@st.cache_data
def save_uploaded_file(file_content, file_name):
    """
    Save the uploaded file to a temporary directory
    """
    import tempfile
    import os
    import uuid

    _, file_extension = os.path.splitext(file_name)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(tempfile.gettempdir(), f"{file_id}{file_extension}")

    with open(file_path, "wb") as file:
        file.write(file_content.getbuffer())

    return file_path

form = st.form(key="latlon_calculator")
with form:   
    url = st.text_input(
            "Enter a URL to a vector dataset",
            "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/vn_cities.geojson",
        )

    uploaded_file = st.file_uploader(
            "Upload a vector dataset", type=["geojson", "kml", "zip", "tab"]
        )

    if  url or uploaded_file:
        if url:
            file_path = url
            layer_name = url.split("/")[-1].split(".")[0]
        if uploaded_file:
            file_path = save_uploaded_file(uploaded_file, uploaded_file.name)
            layer_name = os.path.splitext(uploaded_file.name)[0]    

        if file_path.lower().endswith(".kml"):
            fiona.drvsupport.supported_drivers["KML"] = "rw"
            gdf = gpd.read_file(file_path, driver="KML")
        else:
            gdf = gpd.read_file(file_path)
        
        center = gdf.dissolve().centroid
        center_lon, center_lat = center.x, center.y
          
        with col1:   
            fields = [ column for column in gdf.columns if column not in gdf.select_dtypes('geometry')]
            m = folium.Map(tiles='stamenterrain', location = [center_lat, center_lon], zoom_start=4)           
            folium.GeoJson(gdf, name = layer_name,  
                            popup = folium.GeoJsonPopup(
                            fields = fields
                            )).add_to(m)
            m.fit_bounds(m.get_bounds(), padding=(30, 30))
            folium_static(m, width = 600)
        
        submitted = st.form_submit_button("Antipodes Transform")        
        if submitted:
            target = antipodes_transform(gdf)
            with col2:
                if not target.empty: 
                    center = target.dissolve().centroid
                    center_lon, center_lat = center.x, center.y             
                    fields = [ column for column in target.columns if column not in target.select_dtypes('geometry')]
                    m = folium.Map(tiles='stamentoner', location = [center_lat, center_lon], zoom_start=4)
                    folium.GeoJson(target,                            
                                   popup = folium.GeoJsonPopup(
                                   fields = fields
                                    )).add_to(m)
   
                    m.fit_bounds(m.get_bounds(), padding=(30, 30))
                    folium_static(m, width = 600)         
                    download_geojson(target, layer_name)   