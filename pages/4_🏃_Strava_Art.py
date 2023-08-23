import pandas as pd
import folium
from streamlit_folium import st_folium, folium_static
from folium.plugins import AntPath, Fullscreen
import streamlit as st
import json
from streamlit_image_select import image_select

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

# Reference: https://dwtkns.com/srtm30m/

st.title("Strava Art")
col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/strava.png", width = 30)
with col2:
    st.write("[Lenny Maughan's Strava Art](https://www.strava.com/athletes/7019519)")

with open("./data/images/strava/strava.json", "r",encoding="utf-8") as f:
    STRAVA = json.load(f)

# if "previous_strava_index" not in st.session_state:
#     st.session_state.update(STRAVA["Tiger"])
#     st.session_state["previous_strava_index"] = 0

strava_image_pattern = "./data/images/strava/{}_small.png"
strava_image_fp = [
    strava_image_pattern.format(name.lower()) for name in list(STRAVA.keys())[:7]
]

index_selected = image_select(
    label = "Choose a route",
    images=strava_image_fp,
    captions=list(STRAVA.keys())[:7],
    use_container_width=False,
    return_value="index",
)
name_selected = list(STRAVA.keys())[index_selected].lower()

try:
    img2 = image_select(
        label="",
        images=[],
        return_value="index",
        use_container_width = False
    )
except: st.write('')
# if index_selected != st.session_state["previous_strava_index"]:
#     name_selected = list(STRAVA.keys())[index_selected]
#     st.write(name_selected)
#     st.session_state.update(STRAVA[name_selected].copy())
#     st.session_state["previous_strava_index"] = index_selected



st.write("")
form = st.form(key="form_settings")


strava_point  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/" + name_selected +  "_point.csv"
strava_polyline  = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/"+ name_selected + "_polyline.geojson"

tiger_style = lambda x: {
  'color' :  'red',
  'opacity' : 1,
  'weight' : 2,
}


df = pd.read_csv(strava_point)
points = df[["lat", "lon"]]
center_lat = points["lat"].mean()
center_lon = points["lon"].mean()

dualmap= folium.plugins.DualMap(tiles="cartodb dark_matter", location = [center_lat,center_lon], zoom_start = 12)


# folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(myMap)
folium.GeoJson(strava_polyline, style_function=tiger_style, name='Track').add_to(dualmap.m1)

Fullscreen(                                                         
        position                = "topright",                                   
        title                   = "Open full-screen map",                       
        title_cancel            = "Close full-screen map",                      
        force_separate_button   = True,                                         
    ).add_to(dualmap) 


# ant_path = AntPath(
#     locations=points,
#     dash_array=[1, 10],
#     delay=1000,
#     color='#7590ba',
#     pulse_color='#3f6fba',
#     radius = 100,
#     # paused=True
# ).add_to(dualmap.m2)


# folium_static(myMap)
# st_folium(myMap)

folium_static(dualmap)
