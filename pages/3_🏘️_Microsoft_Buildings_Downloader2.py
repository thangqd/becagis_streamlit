import pandas as pd
import geopandas as gpd
import shapely
import mercantile
from tqdm import tqdm
import os
import tempfile
import fiona
import folium
from streamlit_folium import st_folium
from folium import plugins
import json
import streamlit as st

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

st.title("Dowload Microsoft Building Footprints")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/ms_buildings.png", width = 30)
with col2:
    st.write("Download [Microsoft Building Footprints](https://github.com/microsoft/GlobalMLBuildingFootprints)")

m = folium.Map(tiles="stamenterrain", location = [10.77588,106.70388], zoom_start =15)

# folium.Rectangle([(10.778904,106.7004), (10.773,106.707)]).add_to(m)
# rectangle = {
#   "type": "Feature",
#   "properties": {},
#   "geometry": {
#     "type": "Polygon",
#     "coordinates": [
#       [
#         [
#           106.693743,
#           10.77176
#         ],
#         [
#           106.693743,
#           10.779694
#         ],
#         [
#           106.706944,
#           10.779694
#         ],
#         [
#           106.706944,
#           10.77176
#         ],
#         [
#           106.693743,
#           10.77176
#         ]
#       ]
#     ]
#   }
# }

# folium.GeoJson(rectangle).add_to(m)


draw = plugins.Draw(export=True,draw_options={'polyline': False,
                          'circlemarker': False,
                          'polygon': False,
                        #   'rectangle': False,
                          'circle': False,
                          'marker': False},
                           edit_options={'poly': {'allowIntersection': False}})
draw.add_to(m)


output = st_folium(m, width=800)
lastest_drawing =output.get('last_active_drawing')
# st.write(lastest_drawing)


aoi_shape = shapely.geometry.asShape(lastest_drawing['geometry'])

minx, miny, maxx, maxy = aoi_shape.bounds

output_fn = "example_building_footprints.geojson"
     
quad_keys = set()
for tile in list(mercantile.tiles(minx, miny, maxx, maxy, zooms=9)):
    quad_keys.add(int(mercantile.quadkey(tile)))
quad_keys = list(quad_keys)
print(f"The input area spans {len(quad_keys)} tiles: {quad_keys}")

df = pd.read_csv(
    "https://minedbuildings.blob.core.windows.net/global-buildings/dataset-links.csv"
)

idx = 0
combined_rows = []

with tempfile.TemporaryDirectory() as tmpdir:
    # Download the GeoJSON files for each tile that intersects the input geometry
    tmp_fns = []
    for quad_key in tqdm(quad_keys):
        rows = df[df["QuadKey"] == quad_key]
        if rows.shape[0] == 1:
            url = rows.iloc[0]["Url"]

            df2 = pd.read_json(url, lines=True)
            df2["geometry"] = df2["geometry"].apply(shapely.geometry.shape)

            gdf = gpd.GeoDataFrame(df2, crs=4326)
            fn = os.path.join(tmpdir, f"{quad_key}.geojson")
            tmp_fns.append(fn)
            if not os.path.exists(fn):
                gdf.to_file(fn, driver="GeoJSON")
        elif rows.shape[0] > 1:
            raise ValueError(f"Multiple rows found for QuadKey: {quad_key}")
        else:
            raise ValueError(f"QuadKey not found in dataset: {quad_key}")

    # Merge the GeoJSON files into a single file
    for fn in tmp_fns:
        with fiona.open(fn, "r") as f:
            for row in tqdm(f):
                row = dict(row)
                shape = shapely.geometry.shape(row["geometry"])

                if aoi_shape.contains(shape):
                    if "id" in row:
                        del row["id"]
                    row["properties"] = {"id": idx}
                    idx += 1
                    combined_rows.append(row)
     
schema = {"geometry": "Polygon", "properties": {"id": "int"}}

with fiona.open(output_fn, "w", driver="GeoJSON", crs="EPSG:4326", schema=schema) as f:
    f.writerecords(combined_rows)
     