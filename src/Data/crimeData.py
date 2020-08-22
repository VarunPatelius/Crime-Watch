# Import the necessary libraries
import requests
import pandas as pd
import json
from geopy.geocoders import Nominatim
import ipinfo
import folium
import configparser
import cufflinks as cf
import numpy as np
import plotly.graph_objects as go
import plotly
from folium.plugins import MarkerCluster

# Create a ConfigParser instance in order to read the configure.ini file with all the API keys
configReader = configparser.ConfigParser()
configReader.read("configure.ini")

# Create a Nominatim instance to use for geocoding
geolocator = Nominatim(user_agent="Mozilla/5.0")


def getKey(funcName):
    """
    The purpose of this function is to read the configure.ini file and return the API keys based on
    the arguments given, in this case I am using the functions name for the majority
    """
    return configReader[funcName]["key"]


def getStateCurrent():
    """
    This function uses the ipinfo handler to return the current state that a person is residing in currently
    """
    ACCESS_TOKEN = getKey("ipInfo")

    handler = ipinfo.getHandler(ACCESS_TOKEN)
    details = handler.getDetails()

    # Returns state name: "Florida"
    return details.region


def getStateLatLon(lat, lon):
    """
    This function is used for reverse geocoding to return the state that coordinates fall into using the
    Big Data Clout API
    """
    url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={lat}&longitude={lon}&localityLanguage=en"

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    data = response.json()
    return data["principalSubdivision"]


def stateData(state):
    """
    Using the FBI-NIBRS system, this function uses the FBI database to return a states estimated crime statistics
    for several years
    """
    key = getKey("stateData")
    url = f"https://api.usa.gov/crime/fbi/sapi/api/estimates/states/{state}/2000/2018?API_KEY={key}"
    results = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    data = results.json()
    # All the data years are sorted - [1979, 1985, 2000...]
    data_years = sorted([s["year"] for s in data["results"]])

    # The data is returned along with all the years that the data covers
    return [d for d in data["results"]], data_years


def cityData(state):
    """
    Using the opendatanetwork API and a CSV file containing the census IDs for major cities the crime data for those
    cities within a certain state is returned
    """
    ids = pd.read_csv("src/Data/cityData.csv")

    # Only return the id if it is within the state argument given
    state_ids = ids[ids["states"] == state.title()]

    state_city_data = {}
    for i in range(len(state_ids)):
        state_city_data[state_ids.iloc[i]["city"]] = state_ids.iloc[i]["description"]

    return state_city_data


def surroundAddress(address, distance="0.04"):
    """
    This function is used to return crime data from a given address using the spotcrime API. The data and current coords
    can then be fed into the mapper function to create a Folium map for the application
    """
    try:
        located = geolocator.geocode(address)
        if located == None:
            return {"crimes": []}, (0, 0)
        lat, lon = located.latitude, located.longitude

        url = f"https://api.spotcrime.com/crimes.json"
        key = getKey("spotCrime")
        params = {"lat": lat,
                  "lon": lon,
                  "radius": distance,
                  "callback": "jQuery213008995550240819228_1593813722897",
                  "key": key}

        # Always ensure that a user-agent is set otherwise a 403 Forbidden error will be returned
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)
        data = response.text

        # Since the data is returned as a jQuery in its raw form, in order to turn in into a JSON format from string, we
        # need to get rid of some extra characters are the front and back
        p = data.index("(")
        data = data[p + 1:-1]
        d = json.loads(data)

        CURR_COORDS = (lat, lon)

        return d, CURR_COORDS

    except:
        return {"crimes": []}, (0, 0)


def surroundLatLon(lat, lon, distance="0.04"):
    """
    This function word the same way as the surroundAddress function by using the spotcrime API, returning a
    jQuery, cleaning the string and then converting it into a JSON format. The data and the current coordinates are
    then returned and can be fed into the mapper function. It is intended to work with just a given lat and lon
    """
    url = f"https://api.spotcrime.com/crimes.json"
    key = getKey("spotCrime")
    params = {"lat": lat,
              "lon": lon,
              "radius": distance,
              "callback": "jQuery213008995550240819228_1593813722897",
              "key": key}

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)
    data = response.text

    p = data.index("(")
    data = data[p + 1:-1]
    d = json.loads(data)

    CURR_COORDS = (lat, lon)

    return d, CURR_COORDS


def surroundCurrent(distance="0.04"):
    """
    This function works a bit differently than the other two crime functions as it uses the users current location
    """
    key = getKey("ipInfo")

    handler = ipinfo.getHandler(key)
    details = handler.getDetails()

    # This block returns returns the current latitude and longitude
    coords = details.loc.split(",")
    lat, lon = coords[0], coords[1]
    CURR_COORDS = (lat, lon)

    # The rest of the function works the same as the other two
    url = f"https://api.spotcrime.com/crimes.json"
    key = getKey("spotCrime")
    params = {"lat": lat,
              "lon": lon,
              "radius": distance,
              "callback": "jQuery213008995550240819228_1593813722897",
              "key": key}

    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, params=params)
    data = response.text

    p = data.index("(")
    data = data[p + 1:-1]
    d = json.loads(data)

    CURR_COORDS = (lat, lon)

    return d, CURR_COORDS


def mapper(data, CURR_COORDS, clustering=False):
    """
    This function is intended to work seamlessly with the surroundAddress, surroundLatLon, and the surroundCurrent
    function in order to create a embeddable Folium map using the data adn the current coordinates
    """
    main_icon = folium.Icon(color="darkred", icon="home", prefix="fa")
    # The data returnd stats for several different crime types, this dictionary ensures that each type gets it own
    # marker color
    type_to_color = {"Arrest": "darkgreen", "Arson": "orange", "Assault": "darkpurple", "Vandalism": "lightgreen",
                     "Theft": "blue", "Other": "lightgray", "Burglary": "black", "Robbery": "beige", "Shooting": "pink"}

    # Basic settings for the main map
    main_map = folium.Map(location=CURR_COORDS, min_zoom=7, max_zoom=14, zoom_start=11.5)
    folium.Marker(CURR_COORDS, tooltip="Current Location", popup="Current Location", icon=main_icon).add_to(main_map)
    marker_cluster = MarkerCluster().add_to(main_map)

    for i in data["crimes"]:
        coords = (i["lat"], i["lon"])
        tooltip = i["type"]
        popup = f'<b>Date:</b><br>{i["date"]}<br><br><b>Address:</b><br>{i["address"]}'

        color = type_to_color.get(i["type"], "blue")
        icon = folium.Icon(color=color)

        mark = folium.Marker(coords, tooltip=tooltip, popup=popup, icon=icon)
        mark.add_to(marker_cluster) if clustering else mark.add_to(main_map)

    # Return a folium Map object
    return main_map


def crimeScore(data, area=0.04):
    """
    A simple function that is intended to take the amount of crimes and to divide them by the total search radius (0.04)
    to return a sort of "crime score"
    """
    return int(len(data["crimes"]) / area)


def stateToStateAbbr(state):
    """
    Used to convert between state names to state abbreviation
    """
    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }

    return us_state_abbrev[state].lower()


def stateGraphMaker(data, dataYears):
    """
    This function is used to generate the html for a plotly graph which can be embedded within a QWebEngineWidget
    """
    cf.go_offline(connected=True)
    data.sort(key=lambda x: x["year"])
    categories = ["violent_crime", "homicide", "rape_revised", "robbery", "aggravated_assault", "property_crime",
                  "burglary", "larceny", "motor_vehicle_theft", "arson"]

    allY = {c: [] for c in categories}

    for year in data:
        for key in allY:
            allY[key].append(year[key])

    df = pd.DataFrame()
    df["years"] = dataYears
    for keys in allY:
        df[keys] = allY[keys]

    fig = go.Figure()
    x = np.array(df["years"])
    yS = df.drop("years", axis=1)

    title = "Crime Occurances from 2000 to 2018"
    xLabel = "Year - Gregorian Calendar"
    yLabel = "Occurances"
    fig.update_layout(autosize=True, margin=dict(l=50, r=50, b=70, t=70, pad=1), title=title, xaxis_title=xLabel,
                      yaxis_title=yLabel, legend_title="Crime Categories")

    for columns in yS.columns:
        y = np.array(df[columns])
        name = columns.replace("_", " ").title()
        fig.add_trace(go.Scatter(x=x, y=y, line_shape='linear', name=name))

    html = '<html><body>'
    html += plotly.offline.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'

    return html