
import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl

st.set_page_config(layout="wide")

st.title("Kepler Vector Tile Basemaps")

# Define the URL of the vector tile basemap
VECTOR_TILE_URL = "https://tiles.basemaps.cartocdn.com/vectortiles/carto.streets/v1/{z}/{x}/{y}.mvt"
# VECTOR_TILE_STYLE = "https://tiles.stadiamaps.com/styles/alidade_smooth.json"
custom_style_url = 'https://raw.githubusercontent.com/heshan0131/kepler.gl-data/master/style/basic.json'


# Define Kepler.gl configuration
config = {
    "version": "v1",
    "config": {
        "mapState": {
            "bearing": 0,
            "latitude": 52.52,
            "longitude": 13.4,
            "pitch": 0,
            "zoom": 0,
        },
        "mapStyle": {
                "styleType": "light",
                # "styleType": "custom",
                # "custom": custom_style_url,
                # "topLayerGroups": {},
                # "visibleLayerGroups": {"label": True, "road": True, "border": False, "building": True, "water": True, "land": True},
                # "mapStyles": {}
                "mapOptions": {
                    "customTileUrl": VECTOR_TILE_URL
                }
            },
    },
}
m = KeplerGl(config = config)

# Display Kepler.gl map in Streamlit
keplergl_static(m)
