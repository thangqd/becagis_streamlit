from ipyleaflet import Map, basemaps, basemap_to_tiles
from ipyleaflet.velocity import Velocity
import xarray as xr
import os
import streamlit.components.v1 as components

center = [44.33956524809713, -130.60546875000003]
zoom = 1
m = Map(
    center=center,
    zoom=zoom,
    interpolation="nearest",
    basemap=basemaps.CartoDB.DarkMatter,
)

m = Map(
    center=center,
    zoom=zoom,
    interpolation="nearest",
    basemap=basemap_to_tiles(basemaps.NASAGIBS.ModisTerraTrueColorCR, "2017-04-08"),
)


import os

if not os.path.exists("wind-global.nc"):
    url = "https://github.com/benbovy/xvelmap/raw/master/notebooks/wind-global.nc"
    import requests

    r = requests.get(url)
    wind_data = r.content
    with open("wind-global.nc", "wb") as f:
        f.write(wind_data)

ds = xr.open_dataset("wind-global.nc")

display_options = {
    "velocityType": "Global Wind",
    "displayPosition": "bottomleft",
    "displayEmptyString": "No wind data",
}
wind = Velocity(
    data=ds,
    zonal_speed="u_wind",
    meridional_speed="v_wind",
    latitude_dimension="lat",
    longitude_dimension="lon",
    velocity_scale=0.01,
    max_velocity=20,
    display_options=display_options,
)
m.add(wind)
m.save('./data/html/velocity.html', title='Velocity Map')
with open("./data/html/velocity.html", 'r', encoding='utf-8') as f: 
    html_data = f.read()

components.html(html_data,height = 500)

