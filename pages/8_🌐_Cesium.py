import streamlit as st
import leafmap
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.title("Cesium 3D Map")
html = "./data/html/saigon_buildings.html"
# html = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/html/saigon_buildings.html"
# leafmap.cesium_to_streamlit(html,width=800, height=600, responsive=True, scrolling=False)

with open(html, 'r', encoding='utf-8') as f: 
    html_data = f.read()

components.html(html_data,height = 500)
