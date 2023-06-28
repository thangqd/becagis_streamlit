import streamlit as st
from itertools import cycle
import streamlit.components.v1 as components


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


from PIL import Image
import os
import streamlit as st
# from streamlit_elements import elements, mui, html, sync


HtmlFile = open("./data/image_slideshow.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code,height = 800)

# path = "./data/AIFaces/"
# list = os.listdir(path)
# col1, col2 = st.columns(2)

# with col1 :
#     for i in range(int(len(list) / 2)) :
#         image = Image.open(path + list[i])
#         # st.image(image, caption=list[i][:-4])
#         st.image(image)
# with col2 :
#     for i in range(int(len(list)/2), len(list)) :
#         image = Image.open(path + list[i])
#         st.image(image)


# path = "./data/AIFaces/"
# list =os.listdir(path)
# IMAGES = []
# for i in range (len(list)) :
#     IMAGES.append(path + list[i])

# IMAGES = [
#     "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/AIFaces/ai_face1.png",
#     "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/AIFaces/ai_face2.png",
#     "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/AIFaces/ai_face3.png",
#     "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/AIFaces/ai_face4.png",
#     "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/AIFaces/ai_face5.png",
#     "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/AIFaces/ai_face6.png",
# ]


# def slideshow_swipeable(images):
#     # Generate a session state key based on images.
#     key = f"slideshow_swipeable_{str(images).encode().hex()}"

#     # Initialize the default slideshow index.
#     if key not in st.session_state:
#         st.session_state[key] = 0

#     # Get the current slideshow index.
#     index = st.session_state[key]

#     # Create a new elements frame.
#     with elements(f"frame_{key}"):

#         # Use mui.Stack to vertically display the slideshow and the pagination centered.
#         # https://mui.com/material-ui/react-stack/#usage
#         with mui.Stack(spacing=2, alignItems="cnter"):

#             # Create a swipeable view that updates st.session_state[key] thanks to sync().
#             # It also sets the index so that changing the pagination (see below) will also
#             # update the swipeable view.
#             # https://mui.com/material-ui/react-tabs/#full-width
#             # https://react-swipeable-views.com/demos/demos/
#             with mui.SwipeableViews(index=index, resistance=True, onChangeIndex=sync(key)):
#                 for image in images:
#                     html.img(src=image, css={"width": "60%"})

#             # Create a handler for mui.Pagination.
#             # https://mui.com/material-ui/react-pagination/#controlled-pagination
#             def handle_change(event, value):
#                 # Pagination starts at 1, but our index starts at 0, explaining the '-1'.
#                 st.session_state[key] = value-1

#             # Display the pagination.
#             # As the index value can also be updated by the swipeable view, we explicitely
#             # set the page value to index+1 (page value starts at 1).
#             # https://mui.com/material-ui/react-pagination/#controlled-pagination
#             mui.Pagination(page=index+1, count=len(images), color="primary", onChange=handle_change)

# slideshow_swipeable(IMAGES)

# imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

# selectedImageUrl = imageCarouselComponent(imageUrls=IMAGES, height=200)

# if selectedImageUrl is not None:
#     st.image(selectedImageUrl)
