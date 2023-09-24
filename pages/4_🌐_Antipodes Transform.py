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

def download_geojson(gdf):
    if not gdf.empty:        
        geojson = gdf.to_json()  
        with col2:
            ste.download_button(
                label="Download GeoJSON",
                file_name= "antipodes.geojson",
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
    coords = list(p.coords)
    coords = [Point(antipode_lon(p[0]), antipode_lat(p[1])) for p in coords] 
    st.write(coords)
    return Polygon(coords)

def antipodes_transform(source): 
    # st.write(source.geometry.type) 
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
        target = source.drop(['geometry'], axis=1) 
        target = gpd.GeoDataFrame(target, crs=source.crs, geometry=[LineString(x) for x in source['points']])
        target['geometry'] = target.geometry.map(antipode_line) 
        target = target.drop(['points'], axis=1)
        return target    
    elif (source.geometry.type == 'MultiLineString').all():
        st.write(source.geometry.type)
        st.write(source)
        source = source.explode(index_parts=False)
        source['points'] = gdf.apply(lambda x: [y for y in x['geometry'].geoms[0].coords], axis=1)
        source.to_dict('records')      
        st.write(source) 
        target = source.drop(['geometry'], axis=1)       
        target = gpd.GeoDataFrame(target, crs=source.crs, geometry=[LineString(x) for x in source['points']])
        target['geometry'] = target.geometry.map(antipode_line) 
        target = target.drop(['points'], axis=1)
        target = target.dissolve(by = target.index)
        return target
    
    elif (source.geometry.type == 'Polygon').all():
        st.write(source.geometry.type)
        st.write(source)
        source['points'] = gdf.apply(lambda x: [y for y in x['geometry'].coords], axis=1)
        source.to_dict('records')       
        # target = source.drop(['geometry'], axis=1) # drop coordinate tuples, if not needed anymore       
        target = gpd.GeoDataFrame(target, crs=source.crs, geometry=[Polygon(x) for x in source['points']])
        target['geometry'] = target.geometry.map(antipode_polygon) 
        # target = target.drop(['points'], axis=1)
        return target  
    
    else:
        st.write('aaaaa')

    # for index, row in source.iterrows():
    #     polygon_area = row["geometry"].length
    #     st.write(f"The polygon in row {index} has a surface area of {polygon_area:0.1f} m.")

    # features = source.getFeatures()      
    # for current, feature in enumerate(features):
    #     geom= feature.geometry()
    #     if geom.type() == 0: # Point
    #         if not geom.isMultipart(): #Single part  
    #             new_geom = self.antipode_geom(feature.geometry().asPoint())
    #             new_feature = QgsFeature()
    #             new_feature.setGeometry(new_geom)
    #             new_feature.setAttributes(feature.attributes()) 
    #             sink.addFeature(new_feature, QgsFeatureSink.FastInsert)   
    #         else: #Multi part 
    #             # new_geom = self.antipode_geom(feature.geometry().asPoint())                    
    #             # new_feature = QgsFeature()
    #             # new_feature.setGeometry(new_geom)
    #             # new_feature.setAttributes(feature.attributes()) 
    #             # sink.addFeature(new_feature, QgsFeatureSink.FastInsert) 
    #             pass

    #     elif geom.type() == 1 and not geom.isMultipart(): #Single part Polyline  
    #         vertices = geom.asPolyline() 
    #         new_vertices = []
    #         for vertice in vertices:
    #             new_vertice  = self.antipode_geom(vertice)
    #             new_vertices.append(QgsPointXY(new_vertice.asPoint()))
    #         new_polyline = QgsGeometry.fromPolylineXY(new_vertices)
    #         new_feature = QgsFeature()
    #         new_feature.setGeometry(new_polyline)
    #         new_feature.setAttributes(feature.attributes()) 
    #         sink.addFeature(new_feature, QgsFeatureSink.FastInsert)

    #     elif geom.type() == 2 and not geom.isMultipart(): #Single part Polygon  
    #         vertices = geom.asPolygon() 
    #         new_vertices =[]
    #         n = len(vertices[0])
    #         for i in range(n):
    #             new_vertice  = self.antipode_geom(vertices[0][i])
    #             new_vertices.append(QgsPointXY(new_vertice.asPoint()))
            
    #         new_vertices_polygon = [[QgsPointXY(i[0], i[1] ) for i in new_vertices]]
    #         new_polygon = QgsGeometry.fromPolygonXY(new_vertices_polygon)
    #         new_feature = QgsFeature()
    #         new_feature.setGeometry(new_polygon)
    #         new_feature.setAttributes(feature.attributes()) 
    #         sink.addFeature(new_feature, QgsFeatureSink.FastInsert)

    #     if feedback.isCanceled():
    #         break
    #     feedback.setProgress(int(current * total))    
    #     # feedback.pushInfo(self.tr('Operation completed successfully!', 'Hoàn thành!'))          
    # return {self.OUTPUT: dest_id}
    # pass

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
            "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/polygon.geojson",
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
            m = folium.Map(tiles='stamenterrain', location = [center_lat, center_lon], zoom_start=16)           
            folium.GeoJson(gdf, name = layer_name).add_to(m)
            folium_static(m, width = 600)
        
        submitted = st.form_submit_button("Antipodes Transform")        
        if submitted:
            target = antipodes_transform(gdf)
            with col2:
                if not target.empty: 
                    center = target.dissolve().centroid
                    center_lon, center_lat = center.x, center.y             
                    m = folium.Map(tiles='stamentoner', location = [center_lat, center_lon], zoom_start=16)
                    folium.GeoJson(target).add_to(m)
                    folium_static(m, width = 600)         
                    download_geojson(target)   