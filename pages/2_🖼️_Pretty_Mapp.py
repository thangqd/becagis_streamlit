import streamlit as st
from prettymapp.settings import STYLES
import copy
import json
from prettymapp.geo import GeoCodingError, get_aoi
from streamlit_image_select import image_select
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
from folium import plugins
import shapely
import pandas as pd

# @st.experimental_memo(show_spinner=False)
@st.cache_data
def st_get_osm_geometries(aoi):
    """Wrapper to enable streamlit caching for package function"""
    df = get_osm_geometries(aoi=aoi)
    return df

@st.cache_data
# @st.experimental_memo(show_spinner=False)
def st_plot_all(_df: GeoDataFrame, **kwargs):
    """Wrapper to enable streamlit caching for package function"""
    fig = Plot(_df, **kwargs).plot_all()
    return fig

@st.cache_data
def get_colors_from_style(style: str) -> dict:
    """
    Returns dict of landcover_class : color
    """
    lc_class_colors = {}
    for lc_class, class_style in STYLES[style].items():
        colors = class_style.get("cmap", class_style.get("fc"))
        if isinstance(colors, list):
            for idx, color in enumerate(colors):
                lc_class_colors[f"{lc_class}_{idx}"] = color
        else:
            lc_class_colors[lc_class] = colors
    return lc_class_colors

@st.cache_data
def plt_to_svg(_fig: figure) -> str:
    imgdata = StringIO()
    _fig.savefig(
        imgdata, format="svg", pad_inches=0, bbox_inches="tight", transparent=True
    )
    imgdata.seek(0)
    svg_string = imgdata.getvalue()
    return svg_string

@st.cache_data
def svg_to_html(svg_string: str) -> str:
    b64 = base64.b64encode(svg_string.encode("utf-8")).decode("utf-8")
    css_justify = "center"
    css = '<p style="text-align:center; display: flex; flex-direction: column; justify-content: {};">'.format(
        css_justify
    )
    html = r'{}<img src="data:image/svg+xml;base64,{}"/>'.format(css, b64)
    return html

@st.cache_data
def plt_to_href(fig: figure, filename: str):
    buf = BytesIO()
    fig.savefig(buf, format="png", pad_inches=0, bbox_inches="tight", transparent=True)
    img_str = base64.b64encode(buf.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}"></a>'
    return href

@st.cache_data
def slugify(value: Any, allow_unicode: bool = False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")

def gdf_to_bytesio_geojson(geodataframe):
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

with open("./data/images/prettymapp/examples.json", "r",encoding="utf-8") as f:
    EXAMPLES = json.load(f)

if not st.session_state:
    st.session_state.update(EXAMPLES["Portland"])
    lc_class_colors = get_colors_from_style("Peach")
    st.session_state.lc_classes = list(lc_class_colors.keys())  # type: ignore
    st.session_state.update(lc_class_colors)
    st.session_state["previous_style"] = "Peach"
    st.session_state["previous_example_index"] = 0

example_image_pattern = "./data/images/prettymapp/{}_small.png"
example_image_fp = [
    example_image_pattern.format(name.lower()) for name in list(EXAMPLES.keys())[:5]
]
index_selected = image_select(
    "",
    images=example_image_fp,
    captions=list(EXAMPLES.keys())[:5],
    index=0,
    return_value="index",
)
if index_selected != st.session_state["previous_example_index"]:
    name_selected = list(EXAMPLES.keys())[index_selected]
    st.session_state.update(EXAMPLES[name_selected].copy())
    st.session_state["previous_example_index"] = index_selected

st.write("")
form = st.form(key="form_settings")
col1, col2, col3 = form.columns([3, 1, 1]) 
lat_input = 10.77588,
long_input = 106.70388,
add_cord = st.radio(
    "Address or Coordinate?",
    ('Address', 'Coordinate', 'Choose from map'))
if add_cord == 'Address':
    address = col1.text_input(
    "Location address",
    key="address",
)
elif add_cord == 'Coordinate':
    df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/world_cities.csv')
    city_name = df['CITY_NAME'].tolist()
    cities = col1.selectbox(
    'Choose a city',city_name)
    lat_input = col1.number_input(
    "Lat",
    value = 10.77588,
    min_value=-90.00000, 
    max_value=90.00000,
    step=0.001,
    format = "%f",
    # key="lat_input",
)
    long_input = col1.number_input(
    "Long",
    value = 106.70388,
    min_value=-180.00000, 
    max_value=180.00000,
    step=0.001,
    format = "%f",
    # key="long_input",
)

elif add_cord == 'Choose from map':
    m = folium.Map(tiles="stamenterrain", location = [10.77588,106.70388], zoom_start =14)
    draw = plugins.Draw(export=True,draw_options={
                            'polyline': False,
                            'circlemarker': False,
                            'polygon': False,
                            'rectangle': False,
                            'circle': False,
                            'marker': True},
                            edit_options=None)
    draw.add_to(m)
    output = st_folium(m, width=400, height=400)
    lat = 10.77588
    long = 106.70388

    lastest_drawing =output.get('last_active_drawing')
    if lastest_drawing is not None:  
        if lastest_drawing['geometry']['type'] == 'Point':
            lastest_point = shapely.geometry.asShape(lastest_drawing['geometry'])
            lat = lastest_point.y
            long = lastest_point.x            
            st.write('Coordinates: (',lat, ',', long, ')' )             

radius = col2.slider(
    "Radius",
    100,
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
    try:
        # aoi = get_aoi(address=address, radius=radius, rectangular=rectangular)
        if add_cord == 'Address':
            aoi = get_aoi(address=address, radius=radius, rectangular=rectangular)
        elif add_cord == 'Coordinate':
            aoi = get_aoi(coordinates=(lat_input, long_input), radius=radius, rectangular=rectangular)    
        elif add_cord == 'Choose from map':
            aoi = get_aoi(coordinates=(lat, long), radius=radius, rectangular=rectangular)   

    except GeoCodingError as e:
        st.error(f"ERROR: {str(e)}")
        st.stop()
    df = st_get_osm_geometries(aoi=aoi)
    config = {
        "aoi_bounds": aoi.bounds,
        "draw_settings": draw_settings,
        "name_on": name_on,
        # "name": '' if custom_title == "" else custom_title,
        "name": '',
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

st.markdown("</br>", unsafe_allow_html=True)
st.markdown("</br>", unsafe_allow_html=True)
ex1, ex2 = st.columns(2)

with ex2.expander("Export geometries as GeoJSON"):
    st.write(f"{df.shape[0]} geometries")
    st.download_button(
        label="Download",
        data=gdf_to_bytesio_geojson(df),
        file_name=f"becagis_prettymapp.geojson",
        mime="application/geo+json",
    )

# config = {"address": address, **config}
# with ex2.expander("Export map configuration"):
#     st.write(config)
st.session_state["previous_style"] = style