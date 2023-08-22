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
    Thang Quach: [BecaGIS Homepage](https://becagis.vn/?lang=en) | [My Homepage](https://thangqd.github.io) | [GitHub](https://github.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)
st.title("Strava Art")


tiger_timeseries =  'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/tiger.csv'
df_tiger = pd.read_csv(tiger_timeseries)

m = KeplerGl(height=600)
m.add_data(
    data=df_tiger, name="Time Series Data"
)  

keplergl_static(m, center_map=True)