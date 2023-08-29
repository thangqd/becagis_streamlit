import streamlit as st 
import pandas as pd
from keplergl import KeplerGl
from streamlit_keplergl import keplergl_static



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

st.title("Time Series Data")

config = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": [
                {
                    "id": "wlh9osp",
                    "type": "trip",
                    "config": {
                        "dataId": "trip_data",
                        "label": "trip_data",
                        "color": [218, 0, 0],
                        "highlightColor": [252, 242, 26, 255],
                        "columns": {"geojson": "_geojson"},
                        "isVisible": True,
                        "visConfig": {
                            "opacity": 0.8,
                            "thickness": 2,
                            "colorRange": {
                                "name": "ColorBrewer Set1-6",
                                "type": "qualitative",
                                "category": "ColorBrewer",
                                "colors": [
                                    "#e41a1c",
                                    "#377eb8",
                                    "#4daf4a",
                                    "#984ea3",
                                    "#ff7f00",
                                    "#ffff33",
                                ],
                            },
                            "trailLength": 10000000,
                            "sizeRange": [0, 100],
                        },
                        "hidden": False,
                        "textLabel": [
                            {
                                "field": None,
                                "color": [255, 255, 255],
                                "size": 18,
                                "offset": [0, 0],
                                "anchor": "start",
                                "alignment": "center",
                            }
                        ],
                    },
                    "visualChannels": {
                        "colorField": {"name": "trip_id", "type": "integer"},
                        "colorScale": "quantile",
                        "sizeField": None,
                        "sizeScale": "linear",
                    },
                }
            ],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "trip_data": [{"name": "trip_id", "format": None}]
                    },
                    "compareMode": False,
                    "compareType": "absolute",
                    "enabled": True,
                },
                "brush": {"size": 0.5, "enabled": False},
                "geocoder": {"enabled": False},
                "coordinate": {"enabled": False},
            },
            "layerBlending": "normal",
            "splitMaps": [],
            "animationConfig": {"speed": 0.5},
        },
        "mapState": {
            "bearing": 0,
            "dragRotate": False,
            "latitude": 49.555586010427305,
            "longitude": 6.153559360201813,
            "pitch": 0,
            "zoom": 10,
            "isSplit": False,
        },
        "mapStyle": {
            "styleType": "dark",
            "topLayerGroups": {},
            "visibleLayerGroups": {
                "label": True,
                "road": True,
                "border": False,
                "building": True,
                "water": True,
                "land": True,
                "3d building": False,
            },
            "threeDBuildingColor": [
                9.665468314072013,
                17.18305478057247,
                31.1442867897876,
            ],
            "mapStyles": {},
        },
    },
}


# df = pd.read_csv('https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/strava/lenny_maughan.csv')

# geo_json = dict(type="FeatureCollection", features=[])
# geo_json["features"]
# for trip in df.trip_id.unique():
#     feature = dict(type="Feature", geometry=None, properties=dict(trip_id=str(trip)))
#     feature["geometry"] = dict(type="LineString", coordinates=df.loc[df.trip_id==trip, ["lon", "lat", "ele", "time"]].to_records(index=False).tolist())
#     geo_json["features"].append(feature)

# geo_json["features"].append(feature)
# st.write(geo_json)

# # with open("aaa.geojson", "w") as outfile:
# #     outfile.write(geo_json)


# my_map = KeplerGl(data={"trip_data": geo_json}, config = config, height=600)
# # my_map = KeplerGl(data= geo_json, height=600)
# keplergl_static(my_map,  center_map=True)

