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
    Thang Quach: <https://thangqd.github.io>
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

st.title("Heatmap")

with st.expander("See source code"):
    with st.echo():
        filepath = "./data/wqi.csv"
        m = leafmap.Map(center=[10.045180, 105.78841], zoom=8, tiles="stamentoner")
        m.add_heatmap(
            filepath,
            latitude="latitude",
            longitude="longitude",
            value="WQI",
            name="Heat map",
            radius=20,
        )
m.to_streamlit(height=700)
