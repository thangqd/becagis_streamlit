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
    Thang Quach: [BecaGIS Homepage](https://becagis.vn/?lang=en) | [GitHub Pages](https://thangqd.github.io)
    [GitHub](https://github.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

# Customize page title
col1, mid, col2 = st.columns([1,1,20])
with col1:
    st.image("./data/images/becagis.png", width = 90)
with col2:
    st.title("BecaGIS on Streamlit")

st.image("./data/images/pythonmaps/flight_routes.png")

# m = leafmap.Map(minimap_control=True,tiles=None)
# m.add_basemap("Stamen.Watercolor")
# m.to_streamlit(height=500)

# HtmlFile = open("./data/fansipan.html", 'r', encoding='utf-8')
# source_code = HtmlFile.read() 
# components.html(source_code,height = 400)

st.markdown(
    """
    BecaGIS Streamlit is inspired by [streamlit-geospatial](https://github.com/giswqs/streamlit-geospatial).
    """
)
# from streamlit_extras.buy_me_a_coffee import button

# button(username="thangqd", floating=False, width=221)
