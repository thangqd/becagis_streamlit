import streamlit as st
import pydeck as pdk
import pandas as pd
import streamlit.components.v1 as components


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
    [GitHub](https://github.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)
st.title("Display PointCloud Data")

DATA_URL = "https://raw.githubusercontent.com/ajduberstein/geo_datasets/master/small_waterfall.csv"
df = pd.read_csv(DATA_URL)

target = [df.x.mean(), df.y.mean(), df.z.mean()]

point_cloud_layer = pdk.Layer(
    "PointCloudLayer",
    data=DATA_URL,
    get_position=["x", "y", "z"],
    get_color=["r", "g", "b"],
    get_normal=[0, 0, 15],
    auto_highlight=True,
    pickable=True,
    point_size=3,
)

view_state = pdk.ViewState(target=target, controller=True, rotation_x=15, rotation_orbit=30, zoom=4.5)
view = pdk.View(type="OrbitView", controller=True)
r = pdk.Deck(point_cloud_layer, initial_view_state=view_state, views=[view])
# st.pydeck_chart(r)
r.to_html("point_cloud_layer.html", css_background_color="#000000")

with open("point_cloud_layer.html", 'r', encoding='utf-8') as f: 
    html_data = f.read()

components.html(html_data,height = 500)

# components.iframe("point_cloud_layer.html")
# with st.expander("See source code"):
#     with st.echo():
#         laz = './data/pentagon.laz'   
# leafmap.view_lidar(laz, cmap='terrain', backend='pyvista')

