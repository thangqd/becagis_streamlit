import streamlit as st
import leafmap.foliumap as leafmap
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


@st.cache_data
def get_layers(url):
    options = leafmap.get_wms_layers(url)
    return options


st.title("Web Feature Service (WFS)")
st.markdown(
"""
This app is a demonstration of loading Web Feature Service (WFS) layers. Simply enter the URL of the WFS service 
in the text box below and press Enter to retrieve the layers.
"""
)

df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/wfs.csv')
wfs = df.url
selected_wfs = st.selectbox('Choose a WFS Server',wfs)
# df2=df.loc[df['CITY_NAME'] == selected_city, ['lat','long']].iloc[0]
