import streamlit as st
import copy
from prettymapp.geo import  get_aoi
import base64
from io import StringIO, BytesIO
import unicodedata
import re
from typing import Any
import io
from matplotlib.pyplot import figure
import streamlit as st
from geopandas import GeoDataFrame
from prettymapp.plotting import Plot
from prettymapp.osm import get_osm_geometries
from prettymapp.settings import STYLES
import folium
from streamlit_folium import st_folium
import pandas as pd
import json
import streamlit_ext as ste


from becalib.prettymapp_utils import (
    st_get_osm_geometries,
    st_plot_all,
    get_colors_from_style,
    gdf_to_bytesio_geojson,
    slugify  

)

def update_latlong(geodataframe):
    geojson_object = io.BytesIO()
    geodataframe.to_file(geojson_object, driver="GeoJSON")
    return geojson_object


# st.set_page_config(
#     page_title="prettymapp", page_icon="🖼️", initial_sidebar_state="collapsed"
# )
st.set_page_config(layout="wide",page_icon="🖼️")

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

st.title("BecaGIS Prettymapp")


st.write(
    "BecaGIS Prettymapp is inspired by [prettymapp](https://github.com/chrieke/prettymapp)"
)
with open("./data/images/prettymapp/examples.json", "r") as f:
    EXAMPLES = json.load(f)


if not st.session_state:
    st.session_state.update(EXAMPLES["Peach"])
    lc_class_colors = get_colors_from_style("Peach")
    st.session_state.lc_classes = list(lc_class_colors.keys())  # type: ignore
    st.session_state.update(lc_class_colors)
    st.session_state["previous_style"] = "Peach"
    st.session_state["previous_example_index"] = 0


st.write("")
form = st.form(key="form_settings")
col1, col2, col3 = form.columns([3, 1, 1]) 
lat_input = 10.77588,
long_input = 106.70388,
with col1: 
    add_cord = st.radio(
        "Input coordinate or Choose from Map?",
        ('Input coordinate', 'Choose from map'))
if add_cord == 'Input coordinate':
    df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/world_cities.csv')
    df.sort_values("CITY_NAME")
    cities = df.sort_values(by="CITY_NAME").CITY_NAME
    selected_city = col1.selectbox(
    'Choose a city',cities, index = 922)
    df2=df.loc[df['CITY_NAME'] == selected_city, ['lat','long']].iloc[0]
    col1_1,col1_2 = col1.columns(2)

    lat_input = col1_1.number_input(
    "Lat",
    value =float(df2['lat']),
    min_value=-90.00000, 
    max_value=90.00000,
    step=0.001,
    format = "%f",
    # key="lat_input",
)
    long_input = col1_2.number_input(
    "Long",
    value = float(df2['long']),
    min_value=-180.00000, 
    max_value=180.00000,
    step=0.001,
    format = "%f",
    # key="long_input",
)

elif add_cord == 'Choose from map':
    with form:
        m = folium.Map(tiles="stamenterrain", location = [10.77588,106.70388], zoom_start =14)       
        markers = m.add_child(folium.ClickForMarker())
        map = st_folium(m, width=400, height=400)
        lat = 10.77588
        long = 106.70388
        if map['last_clicked'] is not None:
            lat = map['last_clicked']['lat']
            long = map['last_clicked']['lng']
            st.write('Coordinates: (',lat, ',', long, ')' )          

radius = col2.slider(
    "Radius",
    1000,
    2000,
    key="radius",
)

style = col3.selectbox(
    "Color theme",
    options=list(STYLES.keys()),
    key="style",
)

expander = form.expander("Customize map style")
col1style, col2style, _, col3style = expander.columns([2, 2, 0.1, 1])

shape_options = ["circle", "rectangle"]
shape = col1style.radio(
    "Map Shape",
    options=shape_options,
    key="shape",
)

bg_shape_options = ["rectangle", "circle", None]
bg_shape = col1style.radio(
    "Background Shape",
    options=bg_shape_options,
    key="bg_shape",
)
bg_color = col1style.color_picker(
    "Background Color",
    key="bg_color",
)
bg_buffer = col1style.slider(
    "Background Size",
    min_value=0,
    max_value=50,
    help="How much the background extends beyond the figure.",
    key="bg_buffer",
)

col1style.markdown("---")
contour_color = col1style.color_picker(
    "Map contour color",
    key="contour_color",
)
contour_width = col1style.slider(
    "Map contour width",
    0,
    30,
    help="Thickness of contour line sourrounding the map.",
    key="contour_width",
)

name_on = col2style.checkbox(
    "Display title",
    help="If checked, adds the selected address as the title. Can be customized below.",
    key="name_on",
)
custom_title = col2style.text_input(
    "Custom title (optional)",
    max_chars=30,
    key="custom_title",
)
font_size = col2style.slider(
    "Title font size",
    min_value=1,
    max_value=50,
    key="font_size",
)
font_color = col2style.color_picker(
    "Title font color",
    key="font_color",
)
text_x = col2style.slider(
    "Title left/right",
    -100,
    100,
    key="text_x",
)
text_y = col2style.slider(
    "Title top/bottom",
    -100,
    100,
    key="text_y",
)
text_rotation = col2style.slider(
    "Title rotation",
    -90,
    90,
    key="text_rotation",
)

if style != st.session_state["previous_style"]:
    st.session_state.update(get_colors_from_style(style))
draw_settings = copy.deepcopy(STYLES[style])
for lc_class in st.session_state.lc_classes:
    picked_color = col3style.color_picker(lc_class, key=lc_class)
    if "_" in lc_class:
        lc_class, idx = lc_class.split("_")
        draw_settings[lc_class]["cmap"][int(idx)] = picked_color  # type: ignore
    else:
        draw_settings[lc_class]["fc"] = picked_color

form.form_submit_button(label="Submit")

result_container = st.empty()
with st.spinner("Creating map... (may take up to a minute)"):
    rectangular = shape != "circle"
    aoi = None    
    if add_cord == 'Input coordinate':
        aoi = get_aoi(coordinates=(lat_input, long_input), radius=radius, rectangular=rectangular)    
    elif add_cord == 'Choose from map':
        aoi = get_aoi(coordinates=(lat, long), radius=radius, rectangular=rectangular) 
    df = st_get_osm_geometries(aoi=aoi)
    config = {
        "aoi_bounds": aoi.bounds,
        "draw_settings": draw_settings,
        "name_on": name_on,
        "name": '' if custom_title == "" else custom_title,
        "font_size": font_size,
        "font_color": font_color,
        "text_x": text_x,
        "text_y": text_y,
        "text_rotation": text_rotation,
        "shape": shape,
        "contour_width": contour_width,
        "contour_color": contour_color,
        "bg_shape": bg_shape,
        "bg_buffer": bg_buffer,
        "bg_color": bg_color,
    }
    fig = st_plot_all(_df=df, **config)
    # result_container.write(html, unsafe_allow_html=True)
    st.pyplot(fig, pad_inches=0, bbox_inches="tight", transparent=True, dpi=300)

# svg_string = plt_to_svg(fig)
# html = svg_to_html(svg_string)
# st.write("")
# fname = slugify(address)
# img_format = st.selectbox("Download image as", ["svg", "png", "jpg"], index=0)
# if img_format == "svg":
#     data = svg_string
# elif img_format == "png":
#     import io
#     data = io.BytesIO()
#     fig.savefig(data, pad_inches=0, bbox_inches="tight", transparent=True)
# st.download_button(label="Download image", data=data, file_name=f"{fname}.{img_format}")

import io
data = io.BytesIO()
fig.savefig(data, pad_inches=0, bbox_inches="tight", transparent=True)
ste.download_button(label="Download image", data=data, file_name=f"prettymapp.png")


st.markdown("</br>", unsafe_allow_html=True)
st.markdown("</br>", unsafe_allow_html=True)
ex1, ex2 = st.columns(2)

with ex2.expander("Export geometries as GeoJSON"):
    st.write(f"{df.shape[0]} geometries")
    ste.download_button(
        label="Download",
        data=gdf_to_bytesio_geojson(df),
        file_name=f"becagis_prettymapp.geojson",
        mime="application/geo+json",
    )
try:
    config = {"address": address, **config}
except:
    pass
with ex2.expander("Export map configuration"):
    st.write(config)
st.session_state["previous_style"] = style