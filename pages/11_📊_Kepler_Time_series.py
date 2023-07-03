import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
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
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/quachdongthang) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)


wqi_timeseries =  'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/cali_earthquakes.csv'
df_wqi = pd.read_csv(wqi_timeseries)


m = KeplerGl(height=600)
m.add_data(
    data=df_wqi, name="Cali Earthquakes"
)  

keplergl_static(m, center_map=True)