import xml.etree.ElementTree as ET
import requests

osm_file_path = 'map.osm'

def getAddresses(osm_file_path):
    # Parse the XML file
    tree = ET.parse(osm_file_path)

    # Get the root element
    root = tree.getroot()

    # Initialize a list to store the address information
    addresses = []

    # Iterate over all 'way' elements
    for way in root.findall('way'):
        # Find 'tag' elements with 'k' attributes for house number, street, and building type
        house_number_tag = way.find(".//tag[@k='addr:housenumber']")
        street_tag = way.find(".//tag[@k='addr:street']")
        building_type_tag = way.find(".//tag[@k='building']")
        
        if house_number_tag is not None and street_tag is not None and building_type_tag is not None:
            house_number = house_number_tag.get('v')
            street_address = street_tag.get('v')
            building_type = building_type_tag.get('v')
            full_address = f"{house_number} {street_address}, {building_type}"
            addresses.append(full_address)

    # Print the list of addresses
    print(addresses)
    return addresses

def getBounds(osmFilePath):
    """Returns a dictionary of the bounding box of an OSM file."""
    # Parse the XML file
    tree = ET.parse(osmFilePath)

    # Get the root element
    root = tree.getroot()

    # Find the 'bounds' element
    bounds = root.find('bounds')

    # If the 'bounds' element exists, extract its attributes into a dictionary
    if bounds is not None:
        bounds_dict = bounds.attrib
        
    else:
        bounds_dict = {}
    print(bounds_dict)
    return bounds_dict

def calculate_center(min_lat, min_lon, max_lat, max_lon):
    # Calculate the center point
    min_lat = float(min_lat)
    min_lon = float(min_lon)
    max_lat = float(max_lat)
    max_lon = float(max_lon)
    center_lat = round((min_lat + max_lat) / 2, 7)
    center_lon = round((min_lon + max_lon) / 2, 7)
    center = [center_lat, center_lon]
    return center

def getPlace(bounds):
    url = "https://api.mapbox.com/geocoding/v5/mapbox.places/" +str(bounds[1])+ "," +str(bounds[0])+ ".json?access_token=pk.eyJ1IjoidGZhbGNvbmdyZWVuIiwiYSI6ImNsb2pwb3U3eDI0NjMyam12cHlqZDFvb2UifQ.1ApwRy1LvS6B2TuQEh4ssw" 
    # print(url)
    # Make a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data from the response
        data = response.json()  
        # print(data)

        # Extract the postcode and town (city) from the data
        for feature in data["features"]:
            if "place_type" in feature and "context" in feature:
                if "postcode" in feature["place_type"]:
                    postcode = feature["text"]
                if "place" in feature["place_type"]:
                    town = feature["text"]

        # Print the postcode and town
        print("Postcode:", postcode)
        print("Town:", town)
        place = [postcode, town]
        return place
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
    
def appendPlace(place):
    # Open the file in append mode
    with open('addresses.csv', 'a') as file:
        # Write the postcode and town to the file
        file.write(f"{place[0]}, {place[1]}\n")


getAddresses(osm_file_path)

bounds = getBounds(osm_file_path)
center = calculate_center(bounds['minlat'], bounds['minlon'], bounds['maxlat'], bounds['maxlon']) 
print(center)

place = getPlace(center)
appendPlace(place)

