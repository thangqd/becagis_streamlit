import geopandas as gpd
import pandas as pd
from shapely import wkt
# df = pd.read_csv("d:\\Projects\\2023\\Satra\\Buildings\\317_buildings.csv", nrows  =1000)
df = pd.read_csv("d:\\Projects\\2023\\Satra\\Buildings\\317_buildings.csv")
df['geometry'] = df['geometry'].apply(wkt.loads)
gdf = gpd.GeoDataFrame(df, crs='epsg:4326')
gdf.to_file("d:\\Projects\\2023\\Satra\\Buildings\\317_buildings.geojson", driver="GeoJSON") 
# print(gdf.head)