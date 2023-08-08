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

@st.cache_data
def read_data():
    path = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/ms_buildings.csv"
    return   pd.read_csv(path)

df = read_data()


countries = df['Location'].drop_duplicates()
country = st.selectbox('', countries )
df_filter = df[df['Location'] == country]  # filter

def make_clickable(url, text):
    return f'<a target="_blank" href="{url}">{text}</a>'

df_filter['Url'] = df_filter['Url'].apply(make_clickable, args = ('Download',))
st.write(df.to_html(escape = False), unsafe_allow_html = True)

# st.write(df_filter)