import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web: <https://becagis.streamlit.app/>
    - GitHub: <https://github.com/thangqd/streamlit-becagis>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Thang Quach: <https://thangqd.github.io>
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/thangqd) | [LinkedIn](https://www.linkedin.com/thangqd)
    """
)

st.title("Marker Cluster")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map(center=[10.045180, 105.78841], zoom=0, tiles="stamentoner")       
        # watersupply_mekong = './data/wqi.csv'
        airports =  'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/watersupply_mekong.csv'
        df = pd.read_csv(airports)

        # provinces = './data/vn_provinces.geojson'

        # m.add_geojson(provinces, layer_name='Vietnam Province')
        m.add_points_from_xy(
            airports,
            x="longitude",
            y="latitude",
            # color_column='province',
            # icon_names=['gear', 'map', 'leaf', 'globe'],
            spin=True
            # add_legend=True
        )
# st.write(df)
m.to_streamlit(height=700)
