import streamlit as st
import leafmap.leafmap as leafmap
import os
import leafmap
import torch
from samgeo import SamGeo, tms_to_geotiff

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


st.title(" Segment Anything Model (SAM)")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map(center=[29.676840, -95.369222], zoom=19)
        m.add_basemap('SATELLITE')
        if m.user_roi_bounds() is not None:
            bbox = m.user_roi_bounds()
        else:
            bbox = [-95.3704, 29.6762, -95.368, 29.6775]
        image = 'satellite.tif'
        tms_to_geotiff(output=image, bbox=bbox, zoom=20, source='Satellite')
        # m.add_raster(image, layer_name='Image')        
        out_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
        checkpoint = os.path.join(out_dir, 'sam_vit_h_4b8939.pth')
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        sam = SamGeo(
            checkpoint=checkpoint,
            model_type='vit_h',
            device=device,
            # erosion_kernel=(3, 3),
            # mask_multiplier=255,
            sam_kwargs=None,
            )
        mask = 'segment.tiff'
        sam.generate(image, mask)
        vector = 'segment.gpkg'
        sam.tiff_to_gpkg(mask, vector, simplify_tolerance=None)
        shapefile = 'segment.shp'
        sam.tiff_to_vector(mask, shapefile)
        style = {
            'color': '#3388ff',
            'weight': 2,
            'fillColor': '#7c4185',
            'fillOpacity': 0.5,
        }
        m.add_vector(vector, layer_name='Vector', style=style)

m.to_streamlit(height=700)
