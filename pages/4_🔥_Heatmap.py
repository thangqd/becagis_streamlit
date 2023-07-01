import streamlit as st
import leafmap.foliumap as leafmap

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
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/quachdongthang) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)


st.title("Heatmap")

with st.expander("See source code"):
    with st.echo():
        # filepath = "./data/wqi.csv"
        filepath = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airports.csv"
        m = leafmap.Map(center=[10.045180, 105.78841], zoom=4, tiles="stamentoner")
        m.add_heatmap(
            filepath,
            latitude="latitude",
            longitude="longitude",
            value="id",
            name="Heat map",
            radius=20,
        )
m.to_streamlit(height=700)
