import streamlit as st
import urllib.request, urllib.parse
from http.cookiejar import CookieJar
import webbrowser
import  leafmap.foliumap as leafmap
from streamlit_folium import st_folium
import folium
from folium import FeatureGroup
from folium.plugins import MarkerCluster
import geopandas as gpd
import pandas as pd
from folium import plugins
import json
import requests




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

# Reference: https://dwtkns.com/srtm30m/

st.title("Download SRTM Data")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/nasa.png", width = 30)
with col2:
    st.write("Download 30-meter resolution elevation data (DEM) from the [Shuttle Radar Topography Mission](https://www2.jpl.nasa.gov/srtm/) | Reference: [Derek Watkins](https://dwtkns.com/srtm30m/)")

# with st.expander("See source code"):
#     with st.echo():

 
# The user credentials that will be used to authenticate access to the data
 
username = "thangqd"
password = "1204Hwen@lio"
lat_tx = 'N10'
lon_tx =  'E106'
# The url of the file we wish to retrieve 


url = "https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/N11E107.SRTMGL1.hgt.zip"
url_png = "https://e4ftl01.cr.usgs.gov/DP133/SRTM/SRTMGL1.003/2000.02.11/N11E107.SRTMGL1.2.jpg"
# Create a password manager to deal with the 401 reponse that is returned from
# Earthdata Login
 
password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
 
 
# Create a cookie jar for storing cookies. This is used to store and return
# the session cookie given to use by the data server (otherwise it will just
# keep sending us back to Earthdata Login to authenticate).  Ideally, we
# should use a file based cookie jar to preserve cookies between runs. This
# will make it much more efficient.
 
cookie_jar = CookieJar()
 
# Install all the handlers.
 
opener = urllib.request.build_opener(
    urllib.request.HTTPBasicAuthHandler(password_manager),
    #urllib.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
    #urllib.HTTPSHandler(debuglevel=1),   # details of the requests/responses
    urllib.request.HTTPCookieProcessor(cookie_jar))
urllib.request.install_opener(opener)
 
# Create and submit the request. There are a wide range of exceptions that
# can be thrown here, including HTTPError and URLError. These should be
# caught and handled.
 
response = urllib.request.urlopen(url)
# Print out the result (not a good idea with binary data!)
# body = response.read()
# st.write(body)
# print (body)
# rast_fname = os.path.basename(url)
# outfp = open(rast_fname, 'wb')

# # Transfer data .. this can take a while ...
# outfp.write(response.read())
# outfp.close()

# print('Your file is at ' + os.path.join(os.getcwd(), rast_fname))
# webbrowser.open_new_tab(url)

# srtm_grid = 'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/srtm_bbox.geojson'      
# gdf = gpd.read_file(srtm_grid)   
# m = leafmap.Map(tiles='Stamen Toner')
# # m.add_gdf(gdf, layer_name='SRTM BBox')
# m.add_geojson(srtm_grid, layer_name='SRTM BBox')

srtm_bbox_url = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/srtm_bbox.geojson"
srtm_bbox_gdp = gpd.read_file(srtm_bbox_url)

m = folium.Map(tiles="stamenterrain", location = [10.78418915150491, 106.70361262696979], zoom_start = 3)

def style_function(feature):
    return {
        'fillColor': '#ffaf00',
        'fillOpacity': 0.3,
        'color': 'blue',
        'weight': 0.2,
        'dashArray': '5, 5'
    }

def highlight_function(feature):
    return {
        'fillColor': '#ffaf00',
        'fillOpacity': 0.5,
        'color': 'magenta',
        'weight': 3,
        'dashArray': '5, 5'
    }

srtm_bbox = json.loads(requests.get(srtm_bbox_url).text)
# print(js_data)

m = folium.Map(location=[53.2193835, 6.5665018], zoom_start=2)

featuregroup = folium.map.FeatureGroup(name='SRTM BBox').add_to(m)

for feature in srtm_bbox['features']:
    fea = folium.GeoJson(feature['geometry'],style_function = style_function, highlight_function=highlight_function)
    fea.add_child(folium.Popup(['<a href="' + feature['properties']['dem'] + '" target="blank">DEM: </a>',
                              '<a href=' + feature['properties']['image'] + '" target="blank">JPG: </a>'] ))
    featuregroup.add_child(fea)

# folium.LayerControl().add_to(m)
# popup = folium.GeoJsonPopup(
#     fields=["dem", "image"],
#     aliases=['DEM', 'JPG'],
#     localize=True,
#     labels=True,
#     # style="background-color: yellow;",
# )

# folium.GeoJson(srtm_bbox_gdp, style_function = style_function, highlight_function=highlight_function, popup=popup).add_to(m)
# srtm_bbox = folium.GeoJson(srtm_bbox_gdp, style_function = style_function, highlight_function=highlight_function, popup=popup)
# srtm_bbox.add_to(m)

st_folium(m, width=800,returned_objects=[])