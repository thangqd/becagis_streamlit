import streamlit as st
import leafmap as leafmap
import leafmap.foliumap as leafmap_folium
import io
import folium
from streamlit_folium import st_folium
from folium import plugins
import shapely
import shapely.geometry
import geopandas as gdp
from folium.plugins import Geocoder
import pyproj
from shapely.ops import transform



st.set_page_config(layout="wide")

st.title("Download OSM Data")
st.write('Please draw an area (< 30km2) on the map to download OSM Data')

def save_geojson_with_bytesio(dataframe):
    #Function to return bytesIO of the geojson
    shp = io.BytesIO()
    dataframe.to_file(shp,  driver='GeoJSON')
    return shp

def save_geojson(dataframe):
    #Function to return bytesIO of the geojson
    # shp = io.BytesIO()
    # dataframe.to_file(shp,  driver='GeoJSON')
    geojson = dataframe.to_json()

def download_geojson(gdf):
        # st.write(gdf)
        geojson = gdf.to_json()  
        st.download_button(
            label="Download GeoJSON",
            mime="application/json",
            file_name= 'osm.geojson',
            data=geojson
        )


col1, col2 = st.columns(2)
with col1:
    m = folium.Map(tiles="cartodbpositron", location = [10.77588,106.70388], zoom_start =15)
    osm_tags = st.multiselect(
                    'Choose OSM tags',
                    ["aerialway", "aeroway", "amenity",
                      "building","barrier","bounday",
                      "craft", "emergency",
                      "geological", "healthcare",
                      "highway","historic", "landuse",
                      "leisure","man_made", "military",
                      "natural","office", "place",
                      "power","public_transport", "railway",
                      "route","shop", "sport",
                      "telecom","tourism", "water","waterway"],
                       ['building', 'highway', "landuse"]
                       )   
    tags = '{'
    for tag in osm_tags:
        tags  += '"' + tag + '": True,'
    tags  += '}'

    draw = plugins.Draw(export=True,
                    # show_geometry_on_click=True,
                    edit_options=None,
                    draw_options={
                    'polyline': False,
                    'circlemarker': False,
                    'polygon': True,
                    'rectangle':True,
                    'circle': False,
                    'marker': True}
                    )
    draw.add_to(m)
    output = st_folium(m, width=500, height = 500)
    lastest_drawing =output.get('last_active_drawing')

map = leafmap_folium.Map(tiles='cartodbpositron',location = [10.77588,106.70388], toolbar_control=False, layers_control=False,zoom_start =15)
if lastest_drawing is not None:  
    gdf = None  
    if lastest_drawing['geometry']['type'] == 'Point':
        lastest_point = shapely.geometry.shape(lastest_drawing['geometry'])
        with col2:
            radius = st.select_slider(
                        "Choose a radius (meters)", 
                        options=[500, 1000, 1500, 2000, 2500, 3000]
                    )
        gdf = leafmap.osm_gdf_from_point(
            center_point=(lastest_point.y, lastest_point.x),
            tags=eval(tags),
            dist=radius
                )
    
    elif lastest_drawing['geometry']['type'] == 'Polygon':
        lastest_polygon = shapely.geometry.shape(lastest_drawing['geometry'])
        wgs84 = pyproj.CRS('EPSG:4326')
        utm = pyproj.CRS('EPSG:3857')
        project = pyproj.Transformer.from_crs(wgs84, utm, always_xy=True).transform
        projected_area = round(transform(project, lastest_polygon).area*10**(-6),2) # area in km2
        if projected_area < 30:
            with col2:
                st.write('The polygon area is '+ str(projected_area) +' km2. Download is in progress')
            gdf = leafmap.osm_gdf_from_polygon(
                polygon= lastest_polygon,
                # tags={"landuse": ["retail", "commercial"], "building": True}                    )
                tags=eval(tags),
                )
        else: 
            with col2:
                st.warning('The polygon area is '+ str(projected_area) +' km2, exceeds 30 km2 area. Please draw a new one', icon="⚠️")
        
    if gdf is not None:
        with col2:
            map.add_gdf(gdf, layer_name='OSM')
            map.to_streamlit(width=500, height=500, returned_objects=[])
        download_geojson(gdf)
        st.write(gdf)