import pandas as pd
import streamlit as st

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

st.title("Dowload Microsoft Building Footprints")


path = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/ms_buildings.csv"
df =    pd.read_csv(path)
countries = df['Location'].drop_duplicates()
country = st.sidebar.selectbox('Select a country:', countries)
st.write(df)