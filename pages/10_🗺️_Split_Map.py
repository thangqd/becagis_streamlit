import streamlit as st
import leafmap.foliumap as leafmap


st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web: <https://becagis.streamlit.app/>
    - GitHub: <https://github.com/thangqd/becagis_streamlit>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Thang Quach: <https://thangqd.github.io>
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)
st.title("Split Map")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map()     
        m.split_map(
            left_layer='ROADMAP', right_layer='HYBRID'
        )
m.to_streamlit(height=700)
