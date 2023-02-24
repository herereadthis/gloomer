"""
ChatGPT prompt
write a pep-8 valid and pylint valid python script that takes in a list of dictionaries containing a location, latitude,
and longitude, and a predefined reference coordinate, and returns a list of location distances using haversine formula,
sorted by closest location first

ChatGPT explanation
This script defines two functions: calculate_distance() and get_sorted_distances(). The calculate_distance() function
takes in two tuples of latitude and longitude coordinates and uses the Haversine formula to calculate the distance
between them. The get_sorted_distances() function takes in a list of dictionaries, where each dictionary represents a
location with a name, latitude, and longitude, and a reference coordinate. It calculates the Haversine distance between
each location and the reference
"""

import math
from typing import List, Dict, Tuple

def calculate_distance(origin: Tuple[float, float], destination: Tuple[float, float]) -> float:
    """
    Calculate the Haversine distance between two points.

    Args:
        origin (Tuple[float, float]): The (latitude, longitude) of the starting location.
        destination (Tuple[float, float]): The (latitude, longitude) of the destination location.

    Returns:
        float: The distance between the two points, in kilometers.
    """
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # Earth's radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c

    return distance


def get_sorted_distances(
        locations: List[Dict[str, float]], reference: Tuple[float, float]
        ) -> List[Tuple[str, float]]:
    """
    Calculate the Haversine distance between each location and the reference
    location, and return a sorted list of tuples containing the name and 
    distance of each location.

    Args:
        locations (List[Dict[str, float]]): A list of dictionaries containing 
        the name, latitude, and longitude of each location.
        reference (Tuple[float, float]): The (latitude, longitude) of the 
        reference location.

    Returns:
        List[Tuple[str, float]]: A sorted list of tuples containing the name and
        distance of each location, sorted by distance.
    """
    distances = []
    for location in locations:
        name = location['name']
        lat = location['latitude']
        lon = location['longitude']
        distance = calculate_distance(reference, (lat, lon))
        distances.append((name, distance))
    distances.sort(key=lambda x: x[1])
    return distances

# Example usage
locations = [
    {"name": "New York City", "latitude": 40.7128, "longitude": -74.0060},
    {"name": "Los Angeles", "latitude": 34.0522, "longitude": -118.2437},
    {"name": "Chicago", "latitude": 41.8781, "longitude": -87.6298},
    {"name": "Houston", "latitude": 29.7604, "longitude": -95.3698},
    {"name": "Phoenix", "latitude": 33.4484, "longitude": -112.0740}
]
reference = (37.7749, -122.4194)  # San Francisco
sorted_distances = get_sorted_distances(locations, reference)
for name, distance in sorted_distances:
    print(f"{name}: {distance:.2f} km")
