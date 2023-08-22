import gpxpy
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.map import Marker, Template

def overlayGPX(gpxData, zoom):
    '''
    overlay a gpx route on top of an OSM map using Folium
    some portions of this function were adapted
    from this post: https://stackoverflow.com/questions/54455657/
    how-can-i-plot-a-map-using-latitude-and-longitude-data-in-python-highlight-few
    '''
    gpx_file = open(gpxData, 'r')
    gpx = gpxpy.parse(gpx_file)
    points = []
    for track in gpx.tracks:
        for segment in track.segments:        
            for point in segment.points:
                points.append(tuple([point.latitude, point.longitude]))
    latitude = sum(p[0] for p in points)/len(points)
    longitude = sum(p[1] for p in points)/len(points)
    myMap = folium.Map(location=[latitude,longitude],zoom_start=zoom)
    folium.PolyLine(points, color="red", weight=2.5, opacity=1).add_to(myMap)
    return (myMap)

filename = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/gpx/tiger.gpx"
overlayGPX(filename, 14)


# def get_path_coordinates(activity_id):
#     filename = "https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/gpx/tiger.gpx"
#     gpx = gpxpy.parse(open(filename))
#     track = gpx.tracks[0]
#     segment = track.segments[0]
#     data_act= []
#     segment_length = segment.length_3d()
#     for point_idx, point in enumerate(segment.points):
#         data_act.append([point.longitude, point.latitude,point.elevation,
#                 point.time, segment.get_speed(point_idx)])

#         columns = ['Longitude', 'Latitude', 'Altitude', 'Time', 'Speed']
#     df_gpx = pd.DataFrame(data_act, columns=columns)
#     return list(map(list, zip(df_gpx.Longitude, df_gpx.Latitude)))


# # Modify Marker template to include the onClick event
# click_template = """{% macro script(this, kwargs) %}
#     var {{ this.get_name() }} = L.marker(
#         {{ this.location|tojson }},
#         {{ this.options|tojson }}
#     ).addTo({{ this._parent.get_name() }}).on('click', onClick);
# {% endmacro %}"""

# # Change template to custom template
# Marker._template = Template(click_template)

# #Map
# df_loc = pd.read_csv("https://raw.githubusercontent.com/thangqd/becagis_streamlit/main/data/gpx/tiger.gpx")
# map = folium.Map(
#     location=[df_loc["Begin Latitude (°DD)"][0].mean(),df_loc["Begin Longitude (°DD)"][0].mean()],
#     control_scale=True,
#     zoom_start = 6)

# # Add js to draw paths on marker click
# map_id = map.get_name()
# click_js = f"""function onClick(e) {{                                 
#                  var coords = e.target.options.pathCoords;                 
#                  var path = L.polyline(coords); 
                
#                 {map_id}.eachLayer(function(layer){{
#                    if (layer instanceof L.Polyline)
#                       {{ {map_id}.removeLayer(layer) }}
#                       }});
                     
#                 path.addTo({map_id});
#                  }}"""
                 
# e = folium.Element(click_js)
# html = map.get_root()
# html.script.add_child(e)

# for i, row in df_loc.iterrows():
#     activity_id = row["Activity ID"]   
#     path_coordinates = get_path_coordinates(activity_id)    
#     folium.Marker(
#         location = [row["Begin Latitude (°DD)"],row["Begin Longitude (°DD)"]],
#         pathCoords=path_coordinates
#     ).add_to(map)  
# st_folium(map)
