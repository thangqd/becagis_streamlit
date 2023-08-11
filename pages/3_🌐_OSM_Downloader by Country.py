import streamlit as st
import geopandas as gpd
import leafmap.kepler as leafmap

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
    Thang Quach: [BecaGIS Homepage](https://becagis.vn/?lang=en) | [My Homepage](https://thangqd.github.io) | [GitHub](https://github.com/thangqd) | [LinkedIn](https://www.linkedin.com/in/thangqd)
    """
)
st.title("Download OSM Data by Country")

col1, col2 = st.columns([1,30])
with col1:
    st.image("./data/images/geofabrik.png", width = 30)
with col2:
    st.write("Download OSM data by country from [Geofabrik](http://download.geofabrik.de/)")

@st.cache_data(experimental_allow_widgets=True) 
def osm_geofabrik(region, country):   
    download_url_pbf = r'https://download.geofabrik.de/' + region + '/'+ country+ '-latest.osm.pbf'
    download_url_shp = r'https://download.geofabrik.de/' + region + '/'+ country+ '-latest-free.shp.zip'
    st.write('Pbf file: ',  download_url_pbf)
    st.write('Shape-zip file (if existed): ' , download_url_shp)
    return   download_url_shp, download_url_pbf

def osm_geofabrik_state(region, country,state):
    #temp_dir = tempfile.mkdtemp()
    download_url_pbf = r'https://download.geofabrik.de/' + region + '/'+ country+ '/' + state+'-latest.osm.pbf'
    download_url_shp = r'https://download.geofabrik.de/' + region + '/'+ country+ '/' + state + '-latest-free.shp.zip'	
    st.write('Pbf file: ',  download_url_pbf)
    st.write('Shape-zip file (if existed): ' , download_url_shp)
    return download_url_pbf, download_url_shp

def filter_states(country):
    ####### Japan:
    if (country =='Japan' ):
        japan_state = ['Chubu region','Chugoku region','Hokkaido','Kansai region','Kanto region','Kyushu','Shikoku','Tohoku region']        
        japan_state_name= []
        for state in japan_state:
            state_name = state.replace(' region','').lower()
            japan_state_name.append(state_name)  
        with col2:
            state_select = st.selectbox('Select a state', japan_state)
            state_name_select =  japan_state_name[japan_state.index(state_select)]
            osm_geofabrik_state('asia','japan',state_name_select )
    
    ####### France:
    elif (country =='France' ):
        france_state = ['Alsace','Aquitaine','Auvergne','Basse-Normandie','Bourgogne','Bretagne','Centre','Champagne Ardenne','Corse','Franche Comte',\
                        'Guadeloupe','Guyane','Haute-Normandie','Ile-de-France','Languedoc-Roussillon','Limousin','Lorraine','Martinique','Mayotte','Midi-Pyrenees',\
                        'Nord-Pas-de-Calais','Pays de la Loire','Picardie','Poitou-Charentes','Provence Alpes-Cote-d''Azur','Reunion','Rhone-Alpes']
        france_state_name= []
        for state in france_state:
            state_name = state.replace(' ','-').lower()
            france_state_name.append(state_name)
        with col2:
            state_select = st.selectbox('Select a state', france_state)
            state_name_select =  france_state_name[france_state.index(state_select)]
            osm_geofabrik_state('europe','france',state_name_select )
    
    ####### France:
    elif (country =='Germany' ):
        germany_state = ['Baden-Wurttemberg','Bayern','Berlin','Brandenburg (mit Berlin)','Bremen','Hamburg','Hessen','Mecklenburg-Vorpommern','Niedersachsen','Nordrhein-Westfalen',\
                        'Rheinland-Pfalz','Saarland','Sachsen','Sachsen-Anhalt','Schleswig-Holstein','Thuringen']
        germany_state_name= []
        for state in germany_state:
            state_name = state.replace('Brandenburg (mit Berlin)','brandenburg').lower()
            germany_state_name.append(state_name)
        with col2:
            state_select = st.selectbox('Select a state', germany_state)
            state_name_select =  germany_state_name[germany_state.index(state_select)]
            osm_geofabrik_state('europe','germany',state_name_select )

    ####### Great Britain:
    elif (country =='Great Britain' ):
        great_britain_state = ['England','Scotland','Wales']
        great_britain_state_name =[]
        for state in great_britain_state:
            state_name = state.lower()
            great_britain_state_name.append(state_name)
        with col2:
            state_select = st.selectbox('Select a state', great_britain_state)
            state_name_select =  great_britain_state_name[great_britain_state.index(state_select)]
            osm_geofabrik_state('europe','great-britain',state_name_select )

    ####### Italy:
    elif (country =='Italy' ):
        italy_state = ['Centro', 'Isole', 'Nord-Est', 'Nord-Ovest', 'Sud']      
        italy_state_name =[]
        for state in italy_state:
            state_name = state.lower()
            italy_state_name.append(state_name)
        with col2:
            state_select = st.selectbox('Select a state', italy_state)
            state_name_select =  italy_state_name[italy_state.index(state_select)]
            osm_geofabrik_state('europe','italy',state_name_select )
    
    ####### Netherlands:
    elif (country =='Netherlands' ):
        netherlands_state = ['Drenthe','Flevoland','Friesland','Gelderland','Groningen','Limburg','Noord-Brabant','Noord-Holland','Overijssel','Utrecht',\
                    'Zeeland','Zuid-Holland']
        netherlands_state_name= []
        for state in netherlands_state:
            state_name = state.lower()
            netherlands_state_name.append(state_name)
        with col2:
            state_select = st.selectbox('Select a state', netherlands_state)
            state_name_select =  netherlands_state_name[netherlands_state.index(state_select)]
            osm_geofabrik_state('europe','netherlands',state_name_select )

    ####### Poland:
    elif (country =='Poland' ):
        poland_state =['Lower Silesian Voivodeship','Kuyavian-Pomeranian Voivodeship','Lodzkie Voivodeship','Lublin Voivodeship','Lubusz Voivodeship',\
            'Lesser Poland Voivodeship','Mazovian Voivodeship','Opole Voivodeship','Subcarpathian Voivodeship','Podlaskie Voivodeship',\
            'Pomeranian Voivodeship','Silesian Voivodeship','Swietokrzyskie Voivodeship','Warmian-Masurian Voivodeship','Greater Poland Voivodeship','West Pomeranian Voivodeship']
        poland_state_name= ['dolnoslaskie', 'kujawsko-pomorskie', 'lodzkie','lubelskie', 'lubuskie',\
                            'malopolskie', 'mazowieckie', 'opolskie','podkarpackie','podlaskie',\
                            'pomorskie', 'slaskie', 'swietokrzyskie', 'warminsko-mazurskie', 'wielkopolskie','zachodniopomorskie']
        with col2:
            state_select = st.selectbox('Select a state', poland_state)
            state_name_select =  poland_state_name[poland_state.index(state_select)]
            osm_geofabrik_state('europe','poland',state_name_select )
        
    ####### Russian Federation:
    elif (country =='Russian Federation' ):
        russian_federation_state = ['Central Federal District','Crimean Federal District','Far Eastern Federal District','North Caucasus Federal District','Northwestern Federal District',\
                'Siberian Federal District','South Federal District','Ural Federal District','Volga Federal District','Kaliningrad']
        russian_federation_state_name = []
        for state in russian_federation_state:
            state_name = state.replace('Federal','fed').replace(' ','-').lower()
            russian_federation_state_name.append(state_name)
        with col2:
            state_select = st.selectbox('Select a state', russian_federation_state)
            state_name_select =  russian_federation_state_name[russian_federation_state.index(state_select)]
            osm_geofabrik_state('','russia',state_name_select )

    ####### United States of America:
    elif (country =='United States of America' ):
        us_state = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','District of Columbia','Florida',\
                'Georgia (US State)','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine',\
                'Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire',\
                'New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Puerto Rico',\
                'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia',\
                'Wisconsin','Wyoming']        
        us_state_name = []
        for state in us_state:
            state_name = state.replace('Georgia (US State)','georgia').replace(' ','-').lower()
            us_state_name.append(state_name)
        with col2:
            state_select = st.selectbox('Select a state', us_state)
            state_name_select =  us_state_name[us_state.index(state_select)]
            osm_geofabrik_state('north-america','us',state_name_select )

     ##################### Canada
    elif (country =='Canada' ):
        canada_state = ['Alberta','British Columbia','Manitoba','New Brunswick','Newfoundland and Labrador','Northwest Territories','Nova Scotia','Nunavut','Ontario','Prince Edward Island',\
                'Quebec','Saskatchewan','Yukon']
        canada_state_name = []
        for state in canada_state:
            state_name = state.replace(' ','-').lower()
            canada_state_name.append(state_name)
        with col2:
            state_select = st.selectbox('Select a state', canada_state)
            state_name_select =  canada_state_name[canada_state.index(state_select)]
            osm_geofabrik_state('north-america','canada',state_name_select )

   ##################### South America
    elif (country =='Brazil' ):
        brazil_state = ['centro-oeste','nordeste','norte','sudeste','sul']        
        with col2:
            state_select = st.selectbox('Select a state', brazil_state)
            osm_geofabrik_state('south-america','brazil',state_select )

def filter_countries(region):
    if region == 'Africa':  ##################### Africa
        africa =['Algeria','Angola','Benin','Botswana','Burkina Faso','Burundi','Cameroon','Canary Islands','Cape Verde','Central African Republic',\
                'Chad','Comores','Congo (Republic/Brazzaville)','Congo (Democratic Republic/Kinshasa)','Djibouti','Egypt','Equatorial Guinea','Eritrea','Ethiopia','Gabon',\
                'Ghana','Guinea','Guinea-Bissau','Ivory Coast','Kenya','Lesotho','Liberia','Libya','Madagascar','Malawi',\
                'Mali','Mauritania','Mauritius','Morocco','Mozambique','Namibia','Niger','Nigeria','Rwanda','Saint Helena, Ascension, and Tristan da Cunha',\
                'Sao Tome and Principe','Senegal and Gambia','Seychelles','Sierra Leone','Somalia','South Africa','South Sudan','Sudan','Swaziland',\
                'Tanzania','Togo','Tunisia','Uganda','Zambia','Zimbabwe',\
                'South Africa (includes Lesotho)'] #special region
        africa_name = []
        for country in africa:
            country_name = country.replace('Congo (Republic/Brazzaville)','congo-brazzaville').replace('Congo (Democratic Republic/Kinshasa)','congo-democratic-republic')\
            .replace('South Africa (includes Lesotho)','south-africa-and-lesotho').replace(' ','-').replace(',','').lower()
            africa_name.append(country_name)
        
        with col2:
            country_select = st.selectbox('Select a country', africa)
            country_name_select =  africa_name[africa.index(country_select)]
            osm_geofabrik('africa',country_name_select)	

    elif region == 'Antarctica':  ##################### Antarctica
        with col2:
            osm_geofabrik('','antarctica')	

    elif region == 'Asia':
        asia = ['Afghanistan','Armenia','Azerbaijan','Bangladesh','Bhutan','Cambodia','China','GCC States','India','Indonesia',\
                    'Iran','Iraq','Israel and Palestine','Japan','Jordan','Kazakhstan','Kyrgyzstan','Laos','Lebanon','Malaysia, Singapore, and Brunei',\
                    'Maldives','Mongolia','Myanmar','Nepal','North Korea','Pakistan','Philippines','Russian Federation','South Korea','Sri Lanka',\
                    'Syria','Taiwan','Tajikistan','Thailand','Turkmenistan','Uzbekistan','Vietnam','Yemen']
        asia_name= []
        for country in asia:
            country_name = country.replace('Israel and Palestine','israel-and-palestine' ).replace('Malaysia, Singapore, and Brunei','malaysia-singapore-brunei').replace('Russian Federation','russia').replace(' ','-').lower()
            asia_name.append(country_name)
        with col2:
            country_select = st.selectbox('Select a country', asia) 
            country_name_select =  asia_name[asia.index(country_select)]
            if country_select == 'Russian Federation':
                osm_geofabrik('',country_name_select)	
            else:
                osm_geofabrik('asia',country_name_select)	
            filter_states(country_select)      
    
    ##################### Australia
    elif region == 'Australia and Oceania':

        australia = ['Australia','Cook Islands','Fiji','Kiribati','Marshall Islands','Micronesia','Nauru','New Caledonia','New Zealand','Niue',\
                    'Palau','Papua New Guinea','Samoa','Solomon Islands','Tonga','Tuvalu','Vanuatu']
        australia_name = []
        for country in australia:
            country_name = country.replace(' ','-').lower()
            australia_name.append(country_name)
        with col2:
            country_select = st.selectbox('Select a country', australia)  
            country_name_select =  australia_name[australia.index(country_select)]  
            osm_geofabrik('australia-oceania',country_name_select)	

    ##################### Central America
    elif region == 'Central America':
        centralamerica= ['Bahamas','Belize','Cuba','Guatemala','Haiti and Dominican Republic','Jamaica','Nicaragua']
        centralamerica_name = []
        for country in centralamerica:
            country_name = country.replace('Dominican Republic','domrep').replace(' ','-').lower()
            centralamerica_name.append(country_name)    
        with col2:
            country_select = st.selectbox('Select a country', centralamerica)  
            country_name_select =  centralamerica_name[centralamerica.index(country_select)]  
            osm_geofabrik('central-america',country_name_select)               

    ##################### Europe
    elif region == 'Europe':
        europe= ['Albania','Andorra','Austria','Azores','Belarus','Belgium','Bosnia-Herzegovina','Bulgaria','Croatia','Cyprus',\
                'Czech Republic','Denmark','Estonia','Faroe Islands','Finland','France','Georgia (Eastern Europe)','Germany','Great Britain','Greece',\
                'Hungary','Iceland','Ireland and Northern Ireland','Isle of Man','Italy','Kosovo','Latvia','Liechtenstein','Lithuania','Luxembourg',\
                'Macedonia','Malta','Moldova','Monaco','Montenegro','Netherlands','Norway','Poland','Portugal','Romania',\
                'Russian Federation','Serbia','Slovakia','Slovenia','Spain','Sweden','Switzerland','Turkey','Ukraine (with Crimea)',\
                'Alps','Britain and Ireland','Germany, Austria, Switzerland']#special regions        
        europe_name = []
        for country in europe:
            country_name = country.replace('Georgia (Eastern Europe)','georgia').replace('Ukraine (with Crimea)','ukraine').replace('Germany, Austria, Switzerland','dach').\
                replace('Russian Federation','russia').replace(' ','-').lower()
            europe_name.append(country_name)
        with col2:
            country_select = st.selectbox('Select a country', europe)
            country_name_select =  europe_name[europe.index(country_select)] 
            if country_select == 'Russian Federation':
                osm_geofabrik('',country_name_select)	
            else:
                osm_geofabrik('europe',country_name_select)	
            filter_states(country_select)
    
    ##################### North America
    elif region == 'North America':
        northamerica= ['Canada','Greenland','Mexico','United States of America',\
            'US Midwest','US Northeast','US Pacific','US South','US West']# special regions of US
        northamerica_name = []
        for country in northamerica:
            country_name = country.replace('United States of America','us').replace(' ','-').lower()
            northamerica_name.append(country_name)
        with col2:
            country_select = st.selectbox('Select a country', northamerica)
            country_name_select =  northamerica_name[northamerica.index(country_select)] 
            osm_geofabrik('north-america',country_name_select)	
            filter_states(country_select)

    elif region == 'South America':
        southamerica= ['Argentina','Bolivia','Brazil','Chile','Colombia','Ecuador','Paraguay','Peru','Suriname','Uruguay','Venezuela']
        southamerica_name = []
        for country in southamerica:
            country_name = country.replace(' ','-').lower()
            southamerica_name.append(country_name)
        with col2:
            country_select = st.selectbox('Select a country', southamerica)
            country_name_select =  southamerica_name[southamerica.index(country_select)] 
            osm_geofabrik('south-america',country_name_select)	
            filter_states(country_select)

col1, col2 = st.columns(2)
with col1:
    regions = ['Africa','Antarctica','Asia','Australia and Oceania','Central America','Europe','North America','South America']
    region_name = []
    for reg in regions:
        reg_name = reg.replace(' and ','-').replace(' ','-').lower()
        region_name.append(reg_name)
    region_select = st.selectbox('Select a region', regions)
    filter_countries(region_select)