import streamlit as st
import leafmap
import geopandas as gpd


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
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

st.title("Zonal Stats")

with st.expander("See source code"):
    with st.echo():
        dsm = 'https://opengeos.github.io/data/elevation/dsm.tif'
        hag = 'https://opengeos.github.io/data/elevation/hag.tif'
        buildings = 'https://opengeos.github.io/data/elevation/buildings.geojson'
        m = leafmap.Map()
        # m.add_cog_layer(dsm, name='DSM', palette='terrain')
        # m.add_cog_layer(hag, name='Height Above Ground', palette='magma')
        m.add_geojson(buildings, layer_name='Buildings')
        gdf = gpd.read_file(buildings)
        stats_gdf = leafmap.zonal_stats(gdf, hag, stats=['mean', 'count'], gdf_out=True)

st.write (gdf)
st.write(stats_gdf)
# m.add_gdf(stats_gdf, layer_name='Zonal Stats')
m.to_streamlit(height=700)