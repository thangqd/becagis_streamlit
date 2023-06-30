import streamlit as st
import leafmap.deck as leafmap
import geopandas as gpd
from gadm import GADMDownloader


# st.set_page_config(
#     page_title="prettymapp", page_icon="🖼️", initial_sidebar_state="collapsed"
# )
st.set_page_config(layout="wide",page_icon="🖼️")

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
country = ['Afghanistan','Akrotiri and Dhekelia','Åland','Albania','Algeria','American Samoa','Andorra','Angola','Anguilla','Antarctica',\
            'Antigua and Barbuda','Argentina','Armenia','Aruba','Australia','Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh',\
            'Barbados','Belarus','Belgium','Belize','Benin','Bermuda','Bhutan','Bolivia','Bonaire, Saint Eustatius and Saba','Bosnia and Herzegovina',\
            'Botswana','Bouvet Island','Brazil','British Indian Ocean Territory','British Virgin Islands','Brunei','Bulgaria','Burkina Faso','Burundi','Cambodia',\
            'Cameroon','Canada','Cape Verde','Caspian Sea','Cayman Islands','Central African Republic','Chad','Chile','China','Christmas Island',\
            'Clipperton Island','Cocos Islands','Colombia','Comoros','Cook Islands','Costa Rica','Côte d''Ivoire','Croatia','Cuba','Curaçao',\
            'Cyprus','Czech Republic','Democratic Republic of the Congo','Denmark','Djibouti','Dominica','Dominican Republic','East Timor','Ecuador','Egypt',\
            'El Salvador','Equatorial Guinea','Eritrea','Estonia','Ethiopia','Falkland Islands','Faroe Islands','Fiji','Finland','France',\
            'French Guiana','French Polynesia','French Southern Territories','Gabon','Gambia','Georgia','Germany','Ghana','Gibraltar','Greece',\
            'Greenland','Grenada','Guadeloupe','Guam','Guatemala','Guernsey','Guinea','Guinea-Bissau','Guyana',\
            'Haiti','Heard Island and McDonald Islands','Honduras','Hong Kong','Hungary','Iceland','India','Indonesia','Iran','Iraq','Ireland',\
            'Isle of Man','Israel','Italy','Jamaica','Japan','Jersey','Jordan','Kazakhstan','Kenya','Kiribati',\
            'Kosovo','Kuwait','Kyrgyzstan','Laos','Latvia','Lebanon','Lesotho','Liberia','Libya','Liechtenstein',\
            'Lithuania','Luxembourg','Macao','Macedonia','Madagascar','Malawi','Malaysia','Maldives','Mali','Malta',\
            'Marshall Islands','Martinique','Mauritania','Mauritius','Mayotte','Mexico','Micronesia','Moldova','Monaco','Mongolia',\
            'Montenegro','Montserrat','Morocco','Mozambique','Myanmar','Namibia','Nauru','Nepal','Netherlands','New Caledonia',\
            'New Zealand','Nicaragua','Niger','Nigeria','Niue','Norfolk Island','North Korea','Northern Cyprus','Northern Mariana Islands','Norway',\
            'Oman','Pakistan','Palau','Palestina','Panama','Papua New Guinea','Paracel Islands','Paraguay','Peru','Philippines',\
            'Pitcairn Islands','Poland','Portugal','Puerto Rico','Qatar','Republic of Congo','Reunion','Romania','Russia','Rwanda',\
            'Saint-Barthélemy','Saint-Martin','Saint Helena','Saint Kitts and Nevis','Saint Lucia','Saint Pierre and Miquelon','Saint Vincent and the Grenadines','Samoa','San Marino','Sao Tome and Principe',\
            'Saudi Arabia','Senegal','Serbia','Seychelles','Sierra Leone','Singapore','Sint Maarten','Slovakia','Slovenia','Solomon Islands',\
            'Somalia','South Africa','South Georgia and the South Sandwich Islands','South Korea','South Sudan','Spain','Spratly islands','Sri Lanka','Sudan','Suriname',\
            'Svalbard and Jan Mayen','Swaziland','Sweden','Switzerland','Syria','Taiwan','Tajikistan','Tanzania','Thailand','Togo',\
            'Tokelau','Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Turks and Caicos Islands','Tuvalu','Uganda','Ukraine',\
            'United Arab Emirates','United Kingdom','United States','United States Minor Outlying Islands','Uruguay','Uzbekistan','Vanuatu','Vatican City','Venezuela','Vietnam',\
            'Virgin Islands, U.S.','Wallis and Futuna','Western Sahara','Yemen','Zambia','Zimbabwe']
country_short = ['AFG','XAD','ALA','ALB','DZA','ASM','AND','AGO','AIA','ATA',\
    'ATG','ARG','ARM','ABW','AUS','AUT','AZE','BHS','BHR','BGD',\
    'BRB','BLR','BEL','BLZ','BEN','BMU','BTN','BOL','BES','BIH',\
    'BWA','BVT','BRA','IOT','VGB','BRN','BGR','BFA','BDI','KHM',\
    'CMR','CAN','CPV','XCA','CYM','CAF','TCD','CHL','CHN','CXR',\
    'XCL','CCK','COL','COM','COK','CRI','CIV','HRV','CUB','CUW',\
    'CYP','CZE','COD','DNK','DJI','DMA','DOM','TLS','ECU','EGY',\
    'SLV','GNQ','ERI','EST','ETH','FLK','FRO','FJI','FIN','FRA',\
    'GUF','PYF','ATF','GAB','GMB','GEO','DEU','GHA','GIB','GRC',\
    'GRL','GRD','GLP','GUM','GTM','GGY','GIN','GNB','GUY','HTI',\
    'HMD','HND','HKG','HUN','ISL','IND','IDN','IRN','IRQ','IRL',\
    'IMN','ISR','ITA','JAM','JPN','JEY','JOR','KAZ','KEN','KIR',\
    'XKO','KWT','KGZ','LAO','LVA','LBN','LSO','LBR','LBY','LIE',\
    'LTU','LUX','MAC','MKD','MDG','MWI','MYS','MDV','MLI','MLT',\
    'MHL','MTQ','MRT','MUS','MYT','MEX','FSM','MDA','MCO','MNG',\
    'MNE','MSR','MAR','MOZ','MMR','NAM','NRU','NPL','NLD','NCL',\
    'NZL','NIC','NER','NGA','NIU','NFK','PRK','XNC','MNP','NOR',\
    'OMN','PAK','PLW','PSE','PAN','PNG','XPI','PRY','PER','PHL',\
    'PCN','POL','PRT','PRI','QAT','COG','REU','ROU','RUS','RWA',\
    'BLM','MAF','SHN','KNA','LCA','SPM','VCT','WSM','SMR','STP',\
    'SAU','SEN','SRB','SYC','SLE','SGP','SXM','SVK','SVN','SLB',\
    'SOM','ZAF','SGS','KOR','SSD','ESP','XSP','LKA','SDN','SUR',\
    'SJM','SWZ','SWE','CHE','SYR','TWN','TJK','TZA','THA','TGO',\
    'TKL','TON','TTO','TUN','TUR','TKM','TCA','TUV','UGA','UKR',\
    'ARE','GBR','USA','UMI','URY','UZB','VUT','VAT','VEN','VNM',\
    'VIR','WLF','ESH','YEM','ZMB','ZWE']
lod = [3,2,2,4,3,4,2,4,1,1,2,3,2,1,3,4,3,2,2,5,2,3,5,2,3,2,3,4,2,4,3,1,4,1,2,3,3,4,5,5,4,4,2,1,2,3,4,4,4,1,1,1,3,2,1,3,5,3,3,1,2,3,4,3,3,2,3,4,4,\
            3,3,3,3,4,4,1,3,3,5,6,3,2,2,3,3,3,5,3,1,4,2,2,3,2,3,2,4,3,3,5,1,3,2,3,3,4,5,3,3,2,3,2,4,2,3,2,3,3,4,1,3,2,3,3,3,4,2,4,2,2,3,5,3,2,5,4,3,1,5,3,\
            1,3,3,2,2,3,2,2,1,3,2,2,5,4,4,3,2,5,3,3,3,3,4,3,1,1,3,2,2,3,3,4,2,3,4,3,1,3,4,4,1,4,4,2,2,3,3,3,4,6,1,1,3,2,2,2,2,3,2,3,2,5,3,2,4,2,1,3,3,3,3,\
            5,1,3,4,5,1,3,4,3,2,3,3,4,3,3,4,4,4,3,2,2,2,3,3,2,2,2,5,3,4,4,3,2,3,3,3,1,3,4,3,3,2,3,3,3]

country = st.selectbox(
    'Choose a country', country)

st.write('You selected:', country)


downloader = GADMDownloader(version="4.1")

country_name = country
ad_level = 0
gdf = downloader.get_shape_data_by_country_name(country_name=country_name, ad_level=2)
m = leafmap.Map()
m.add_gdf(gdf)
st.pydeck_chart(m)
