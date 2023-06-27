import streamlit as st
import leafmap.foliumap as leafmap
import base64

st.set_page_config(layout="wide")

st.sidebar.info(
    """
    - Web: <https://becagis.streamlit.app/>
    - GitHub: <https://github.com/thangqd/streamlit-becagis>
    """
)

st.sidebar.title("Contact")
st.sidebar.info(
    """
    Thang Quach: <https://thangqd.github.io>
    [GitHub](https://github.com/thangqd) | [Twitter](https://twitter.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)

st.title("Vector to gif")

with st.expander("See source code"):
    with st.echo():
        # data = 'https://github.com/opengeos/data/raw/main/us/boulder_buildings.zip'
        # m = leafmap.Map(center=[39.9898, -105.2532], zoom=14)
        # m.add_vector(data, layer_name='Buildings')
        # out_gif = 'buildings.gif'
        # colname = 'year_built'
        # title = 'Building Evolution in Boulder, Colorado, USA (1950-2015)'
        # leafmap.vector_to_gif(
        #     data,
        #     out_gif,
        #     colname,
        #     vmin=1950,
        #     vmax=2015,
        #     step=10,
        #     facecolor='black',
        #     figsize=(10, 8),
        #     title=title,
        #     xy=('1%', '1%'),
        #     fontsize=20,
        #     progress_bar_color='blue',
        #     progress_bar_height=10,
        #     dpi=300,
        #     fps=10,
        #     mp4=False,
        #     verbose=True,
        # )
        pass
# st.write("![Your Awsome GIF](https://media.giphy.com/media/3ohzdIuqJoo8QdKlnW/giphy.gif)")
file_ = open("./data/buildings.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)

# st.write("![Building](https://github.com/thangqd/becagis_streamlit/blob/main/buildings.gif)")

# m.to_streamlit(height=700)
# st.write("![Your Awsome GIF](https://media.giphy.com/media/3ohzdIuqJoo8QdKlnW/giphy.gif)")
# # st.image("buildings.gif") 