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


airports =  'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airports.csv'
df_airports = pd.read_csv(airports)

# airlines =  'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airlines.csv'
airlines = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/uk_commute.csv"

df_airlines = pd.read_csv(airlines)

m = KeplerGl(height=600)
m.add_data(
    data=df_airports, name="airports"
)  # Alternative: KeplerGl(height=400, data={"name": df})

m.add_data(
    data=df_airlines, name="airlines"
)  

keplergl_static(m, center_map=True)