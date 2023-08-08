import streamlit as st
# import leafmap.foliumap as leafmap
import leafmap as lm
import io
import folium
from streamlit_folium import st_folium
# from folium import plugins
# import shapely
# import shapely.geometry

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


st.title(" Download OSM Data")

# m = leafmap.Map(tiles='Stamen Toner',toolbar_control=True, layers_control=True)
# gdf = leafmap.osm_gdf_from_place("New York City", tags={"amenity": "bar"})
# m.add_gdf(gdf, layer_name='New York City')
# m.add_osm_from_geocode("New York City", layer_name='NYC')
# m.add_osm_from_address(
#     address="New York City",
#     tags={"landuse": ["retail", "commercial"], "building": True},
#     dist=1000,
#     layer_name="NYC buildings",
# )
# m = leafmap.Map(
#         center=[46.7808, -96.0156], zoom=12, toolbar_control=False, layers_control=True
#     )
# m.add_osm_from_point(
# gdf = lm.osm_gdf_from_place("New York City", tags={"amenity": "bar"})
m = folium.Map(tiles="stamenterrain", location = [10.77588,106.70388], zoom_start =15)
# m = leafmap.Map(tiles='Stamen Toner',toolbar_control=False, layers_control=False,location = [10.784077934654013, 106.70343973062722], zoom_start =15)
# draw = plugins.Draw(export=True,draw_options={'polyline': False,
#                         'circlemarker': False,
#                         'polygon': False,
#                         'rectangle':False,
#                         'circle': False,
#                         'marker': True},
#                         edit_options={'poly': {'allowIntersection': False}})
# draw.add_to(m)

# output = st_folium(m, width=700)
# lastest_drawing =output.get('last_active_drawing')
# st.write(lastest_drawing)

gdf = lm.osm_gdf_from_point(
    center_point=(10.784077934654013, 106.70343973062722),
    tags={"landuse": ["retail", "commercial"], "building": True},
    dist=2000
)
# aoi_shape = shapely.geometry.asShape(lastest_drawing['geometry'])

# minx, miny, maxx, maxy = aoi_shape.bounds


# gdf = lm.add_osm_from_polygon(
#     aoi_shape,
#     tags={"landuse": ["retail", "commercial"], "building": True}
# )


# m.osm_gdf_from_point(
#     # center_point=(46.7808, -96.0156),
#     center_point=(10.784077934654013, 106.70343973062722),
#     tags={"landuse": ["retail", "commercial"], "building": True},
#     dist=2000,
#     layer_name="HCMC",
# )
m.add_gdf(gdf, layer_name='HCMC')


# north, south, east, west = 109.33526981, 102.170435826, 8.59975962975, 23.3520633001
# m.add_osm_from_bbox(
#     north, south, east, west, tags={"amenity": "bar"}, layer_name="NYC bars"
# )
def save_geojson_with_bytesio(dataframe):
    #Function to return bytesIO of the geojson
    shp = io.BytesIO()
    dataframe.to_file(shp,  driver='GeoJSON')
    return shp

m.to_streamlit(height=700)
st.write(f"{gdf.shape[0]} geometries")
# gdf.to_file(path, driver="GeoJSON")  
# gdf.to_json()
# st.download_button(
#     label="Download data",
#     data=save_geojson_with_bytesio(gdf),
#     file_name='my_geojson.geojson',
#     mime='application/geo+json',
# )
st.write(gdf)
# gdf.to_file('dataframe.geojson', driver='GeoJSON')  


