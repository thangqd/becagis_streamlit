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

st.title("Global Building Footprints")


@st.cache
def get_data():
    path = r'cars.csv'
    return pd.read_csv(path)
    df = get_data()

makes = df['make'].drop_duplicates()
years = df['year']
models = df['model']
engines = df['engine']
components = df['components']
make_choice = st.sidebar.selectbox('Select your vehicle:', makes)
year_choice = st.sidebar.selectbox('', years)
model_choice = st.sidebar.selectbox('', models)
engine_choice = st.sidebar.selectbox('', engines)
st.write('Results:', components)
