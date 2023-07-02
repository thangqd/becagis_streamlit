import streamlit as st
# import leafmap.foliumap as leafmap
# import leafmap.leafmap as leafmap
import leafmap.foliumap as leafmap
import leafmap as lm
import io

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


st.title(" Download OSM Data")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map(tiles='Stamen Toner',toolbar_control=True, layers_control=True)
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
        gdf = lm.osm_gdf_from_point(
            center_point=(10.784077934654013, 106.70343973062722),
            tags={"landuse": ["retail", "commercial"], "building": True},
            dist=2000
        )
        m.add_gdf(gdf, layer_name='HCMC')

        # m.osm_gdf_from_point(
        #     # center_point=(46.7808, -96.0156),
        #     center_point=(10.784077934654013, 106.70343973062722),
        #     tags={"landuse": ["retail", "commercial"], "building": True},
        #     dist=2000,
        #     layer_name="HCMC",
        # )

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


