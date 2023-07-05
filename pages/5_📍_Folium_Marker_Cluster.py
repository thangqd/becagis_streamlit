import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

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


st.title("Marker Cluster")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map(center=[10.045180, 105.78841], zoom=8, tiles="stamentoner")       
        # watersupply_mekong = './data/wqi.csv'
        watersupply_mekong =  'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/watersupply_mekong.csv'
        df = pd.read_csv(watersupply_mekong)
        # provinces = './data/vn_provinces.geojson'
        # m.add_geojson(provinces, layer_name='Vietnam Province')
        m.add_points_from_xy(
            watersupply_mekong,
            x="lon",
            y="lat",
            # color_column='province',
            # icon_names=['gear', 'map', 'leaf', 'globe'],
            spin=True
            # add_legend=True
        )
# st.write(df)
m.to_streamlit(height=700)
