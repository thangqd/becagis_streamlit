import streamlit as st
import leafmap.foliumap as leafmap

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
    Thang Quach: <https://wetlands.io>
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/thangqd) | [LinkedIn](https://www.linkedin.com/thangqd)
    """
)

st.title("Marker Cluster")

with st.expander("See source code"):
    with st.echo():

        m = leafmap.Map(center=[10.045180, 105.78841], zoom=10)       
        watersupply_mekong = 'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/watersupply_mekong.csv'
        # provinces = 'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/vn_provinces.geojson'

        # m.add_geojson(regions, layer_name='Vietnam Province')
        m.add_points_from_xy(
            watersupply_mekong,
            x="longitude",
            y="latitude",
            # color_column='province',
            icon_names=['gear', 'map', 'leaf', 'globe'],
            spin=True,
            add_legend=True,
        )

m.to_streamlit(height=700)
