import gpxpy
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.map import Marker, Template
import streamlit as st

tiger  = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/tiger.csv"
df = pd.read_csv(tiger)

latitude = sum(p[0] for p in df)/len(df)
longitude = sum(p[1] for p in df)/len(df)
myMap = folium.Map(location=[latitude,longitude],tiles="stamenterrain", width = 600, zoom_start=12)
folium.PolyLine(df, color="red", weight=2.5, opacity=1).add_to(myMap)
st_folium (myMap)