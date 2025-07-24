import googlemaps
import pandas as pd
import time
from time import sleep

# Initialize Google Maps API client with your API key
gmaps = googlemaps.Client(key='AIzaSyBvsoaaPuY-l4Txn3e6tesRGUs96rQi6rI')

# List of 50 places with their coordinates (latitude, longitude)
places = {
    "HITEC City": (17.4499, 78.3762),
    "Nampally": (17.3895, 78.4728),
    "Ameerpet": (17.4350, 78.4460),
    "Balanagar": (17.4892, 78.4382),
    "KPHB Colony": (17.4850, 78.3976),
    "Mehdipatnam": (17.3850, 78.4372),
    "Kukatpally": (17.4864, 78.3735),
    "Khairatabad": (17.4144, 78.4730),
    "Madhapur": (17.4483, 78.3792),
    "Peddamma Temple": (17.4191, 78.4103),
    "Panjagutta": (17.4194, 78.4424),
    "Uppal": (17.3972, 78.5552),
    "Ameerpet": (17.4350, 78.4460),
    "Begumpet": (17.4436, 78.4466),
    "Amberpet": (17.4133, 78.5226),
    "Habsiguda": (17.4066, 78.5438),
    "Tarnaka": (17.4301, 78.5416),
    "Rail Nilayam": (17.4386, 78.5108),
    "Paradise": (17.4435, 78.4850),
    "Bowenpally": (17.4686, 78.4811),
    "Himayatnagar": (17.4021, 78.4840),
    "Punjagutta": (17.4254, 78.4505),
    "Banjara Hills": (17.4169, 78.4387),
    "Jubilee Hills": (17.4326, 78.4071)
}

# Create an empty list to store data
data = []


# Function to calculate traffic density with error handling and rate-limiting
def get_traffic_data(source, destination):
    try:
        # Make the API call
        directions = gmaps.directions(source, destination, departure_time="now")

        # Extract the necessary information
        duration_in_traffic = directions[0]['legs'][0]['duration_in_traffic']['value']  # in seconds
        distance = directions[0]['legs'][0]['distance']['value']  # in meters

        # Calculate traffic density: duration/distance ratio (time per meter)
        traffic_density = duration_in_traffic / distance

        # Categorize traffic density
        if traffic_density < 1:
            traffic_level = 'Low'
        elif 1 <= traffic_density < 2:
            traffic_level = 'Medium'
        else:
            traffic_level = 'High'

        return traffic_level, traffic_density, duration_in_traffic, distance
    except Exception as e:
        print(f"Error retrieving data for {source} to {destination}: {e}")
        return None, None, None, None


# Iterate over pairs of places and calculate distances, traffic, and road types
for place1, coords1 in places.items():
    for place2, coords2 in places.items():
        if place1 != place2:
            # Get traffic data between place1 and place2
            traffic_level, traffic_density, duration, distance = get_traffic_data(coords1, coords2)

            # Only append data if we successfully retrieved it
            if traffic_level is not None:
                data.append([place1, place2, traffic_level, traffic_density, duration, distance])

            # Delay to prevent rate-limiting errors
            sleep(1)  # Adjust sleep time if needed

# Create DataFrame
df = pd.DataFrame(data, columns=["source_place", "destination_place", "traffic_level", "traffic_density",
                                 "duration_in_traffic_seconds", "distance_meters"])

# Save to CSV
df.to_csv('hyderabad_road_network_with_traffic.csv', index=False)

# Show the first few rows
print(df.head())
