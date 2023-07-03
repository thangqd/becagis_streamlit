import streamlit as st
import urllib.request, urllib.parse
from http.cookiejar import CookieJar
import webbrowser
import os

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


st.title(" Download SRTM Data")

# with st.expander("See source code"):
#     with st.echo():

 
# The user credentials that will be used to authenticate access to the data
 
username = "thangqd"
password = "1204Hwen@lio"
lat_tx = 'N10'
lon_tx =  'E106'
# The url of the file we wish to retrieve 
url = "https://e4ftl01.cr.usgs.gov/MEASURES/SRTMGL1.003/2000.02.11/N11E107.SRTMGL1.hgt.zip"
url_png = "https://e4ftl01.cr.usgs.gov/DP133/SRTM/SRTMGL1.003/2000.02.11/N11E107.SRTMGL1.2.jpg"
 
# Create a password manager to deal with the 401 reponse that is returned from
# Earthdata Login
 
password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
password_manager.add_password(None, "https://urs.earthdata.nasa.gov", username, password)
 
 
# Create a cookie jar for storing cookies. This is used to store and return
# the session cookie given to use by the data server (otherwise it will just
# keep sending us back to Earthdata Login to authenticate).  Ideally, we
# should use a file based cookie jar to preserve cookies between runs. This
# will make it much more efficient.
 
cookie_jar = CookieJar()
 
# Install all the handlers.
 
opener = urllib.request.build_opener(
    urllib.request.HTTPBasicAuthHandler(password_manager),
    #urllib.HTTPHandler(debuglevel=1),    # Uncomment these two lines to see
    #urllib.HTTPSHandler(debuglevel=1),   # details of the requests/responses
    urllib.request.HTTPCookieProcessor(cookie_jar))
urllib.request.install_opener(opener)
 
 
# Create and submit the request. There are a wide range of exceptions that
# can be thrown here, including HTTPError and URLError. These should be
# caught and handled.
 
response = urllib.request.urlopen(url)
# Print out the result (not a good idea with binary data!)
# body = response.read()
# st.write(body)
# print (body)
rast_fname = os.path.basename(url)
outfp = open(rast_fname, 'wb')

# Transfer data .. this can take a while ...
outfp.write(response.read())
outfp.close()

print('Your file is at ' + os.path.join(os.getcwd(), rast_fname))

# webbrowser.open_new_tab(url)

