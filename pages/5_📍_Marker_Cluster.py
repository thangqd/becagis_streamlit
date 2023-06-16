import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web App URL: <https://streamlit.geemap.org>
    - GitHub repository: <https://github.com/thangqd/streamlit-becagis>
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

        m = leafmap.Map(center=[10.045180, 105.78841], zoom=4)       
        points = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv'
        # regions = 'https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_regions.geojson'

        # m.add_geojson(regions, layer_name='Vietnam Province')
        m.add_points_from_xy(
            points,
            x="x",
            y="y",
            color_column='tinh',
            icon_names=['gear', 'map', 'leaf', 'globe'],
            spin=True,
            add_legend=True,
        )

m.to_streamlit(height=700)
