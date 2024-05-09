import streamlit as st
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
import pandas as pd

st.set_page_config(layout="wide")

st.title("Kepler Arc")

airports =  'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/airports.csv'
df_airports = pd.read_csv(airports)

# airlines =  'https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/airlines.csv'
airlines = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/csv/airlines.csv"

df_airlines = pd.read_csv(airlines)

m = KeplerGl(height=600)
m.add_data(
    data=df_airlines, name="airlines"
)  

keplergl_static(m, center_map=True)