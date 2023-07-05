import streamlit as st
import leafmap.foliumap as leafmap

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


st.title("Web Map Service (WMS)")
st.markdown(
    """
This app is a demonstration of loading Web Map Service (WMS) layers. Simply enter the URL of the WMS service 
in the text box below and press Enter to retrieve the layers.
"""
)

row1_col1, row1_col2 = st.columns([3, 1.3])
width = 800
height = 600
layers = None

with row1_col2:

    becagis_opendata = "https://geoportal.becagis.vn/geoserver/ows"
    url = st.text_input(
        "Enter a WMS URL:", value="https://geoportal.becagis.vn/geoserver/ows"
    )
    empty = st.empty()

    if url:
        options = get_layers(url)
        default = None
        if url == becagis_opendata:
            default = "geonode:BDNC_tuyencap_polyline"
        layers = empty.multiselect(
            "Select WMS layers to add to the map:", options, default=default
        )
        # add_legend = st.checkbox("Add a legend to the map", value=True)
        # if default == "Global Submarine Cables":
        #     legend = str(leafmap.builtin_legends["Global Submarine Cables"])
        # else:
        #     legend = ""
        # if add_legend:
        #     legend_text = st.text_area(
        #         "Enter a legend as a dictionary {label: color}",
        #         value=legend,
        #         height=200,
        #     )

    with row1_col1:
        # m = leafmap.Map(center=(10.045180, 105.78841), zoom=2)
        m = leafmap.Map(tiles='Stamen Toner',toolbar_control=False, layers_control=True)
        if layers is not None:
            for layer in layers:
                m.add_wms_layer(
                    url, layers=layer, name=layer, attribution="", transparent=True
                )
        # if add_legend and legend_text:
        #     legend_dict = ast.literal_eval(legend_text)
        #     m.add_legend(legend_dict=legend_dict)
        # m.st_fit_bounds()
        m.to_streamlit(height=height)