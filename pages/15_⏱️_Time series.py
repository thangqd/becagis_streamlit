import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import sys, os
import io
import logging
import warnings
from importlib_metadata import version  # python3.8+

# disable FutureWarning/DeprecationWarning from prophet/pandas
warnings.simplefilter(action='ignore', category=DeprecationWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import prophet
import streamlit as st
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))

# Workaround to suppress stdout/stderr output from prophet/pystan
# import stdout_suppressor

# disable verbose logging from prophet
logging.getLogger('prophet').setLevel(logging.WARNING)


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


import os

# Workaround to suppress stdout/stderr output from prophet/pystan
# see https://github.com/facebook/prophet/issues/223

class suppress_stdout_stderr(object):
    '''
    A context manager for doing a "deep suppression" of stdout and stderr in
    Python, i.e. will suppress all print, even if the print originates in a
    compiled C/Fortran sub-function.
    This will not suppress raised exceptions, since exceptions are printed
    to stderr just before a script exits, and after the context manager has
    exited (at least, I think that is why it lets exceptions through).

    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for _ in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        for fd in self.null_fds + self.save_fds:
            os.close(fd)



# disable verbose logging from prophet
logging.getLogger('prophet').setLevel(logging.WARNING)

# read data from csv file
df = pd.read_csv('./data/wqi_timeseries.csv')

# streamlit app starts here
st.title("Prophet Test App in Streamlit")
st.markdown('''This is a test app for the `prophet` time-series-forecasting library running in **Streamlit**.
More documentation about `prophet` can be found at the links below:
- `prophet` Website: <https://facebook.github.io/prophet/docs/installation.html>
- `prophet` Github: <https://github.com/facebook/prophet>
- This example app in Github: <https://github.com/Franky1/Streamlit-Prophet-Test>
---
''')
st.subheader("Prophet Version")
st.markdown(f'Currently used `prophet` library version is `{version("prophet")}`')
st.markdown('''---''')

st.subheader("Input DataFrame - df.info()")
# this workaround below is required to show the output of df.info() in the streamlit text widget
buffer = io.StringIO()
df.info(buf=buffer)
st.text(buffer.getvalue())
st.subheader("Input DataFrame - df.describe()")
st.table(df.describe())
st.subheader("Input DataFrame - Head and Tail")
st.table(pd.concat([df.head(5), df.tail(5)]))

# create prophet model
model = prophet.Prophet()
# this is a workaround to suppress stdout/stderr output from pystan
# if you want to see the output, comment out the following line
# with stdout_suppressor.suppress_stdout_stderr():
with suppress_stdout_stderr():
    model.fit(df)  # fit the model

# prepare the dataframe for the prediction
future = model.make_future_dataframe(periods=365)
st.subheader("Future DataFrame Timestamps - Tail")
st.table(future.tail())

# make the prediction
forecast = model.predict(future)
df_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper', 'trend']].tail()
st.subheader("Future DataFrame Predictions - Tail")
st.table(df_forecast)

st.header("Matplotlib Plots")
st.subheader("Prophet Predictions")
# plot the predictions
st.pyplot(model.plot(forecast))
st.subheader("Prophet Components")
# plot the components
st.pyplot(model.plot_components(forecast))
