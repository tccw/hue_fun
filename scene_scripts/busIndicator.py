from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToJson
import json
import urllib.request
import urllib.response
from math import asin, sin, cos, sqrt, radians
from datetime import datetime

# Constants
with open(r"data\my_location.txt") as f:
    data = f.readlines()
    data = list(map(lambda s: s.strip(), data))
lat_me = float(data[0])
lon_me = float(data[1])
API_KEY = data[2]
westbound = 1
eastbound = 0


def haversine_dist(lat1, lon1, lat2, lon2):
    """
    http://www.faqs.org/faqs/geography/infosystems-faq/
    Haversine Formula (from R.W. Sinnott, "Virtues of the Haversine",
     Sky and Telescope, vol. 68, no. 2, 1984, p. 159)
    """
    phi_1 = radians(lat1)
    phi_2 = radians(lat2)
    lambda_1 = radians(lon1)
    lambda_2 = radians(lon2)

    r = 6378 - 21 * sin(phi_2)  # Radius of the Earth crude latitude adjustment (in km)

    term_1 = (sin((phi_2 - phi_1) / 2)) ** 2
    term_2 = cos(lat1) * cos(phi_2) * (sin((lambda_2 - lambda_1) / 2)) ** 2
    hav_term = 2 * asin(sqrt(term_1 + term_2))  # distance in radians

    distance_km = r * hav_term
    distance_m = round(distance_km * 1000, 0)
    return distance_m


feed = gtfs_realtime_pb2.FeedMessage()
response = urllib.request.urlopen('https://gtfs.translink.ca/v2/gtfsposition?apikey=' + API_KEY)
feed.ParseFromString(response.read())

for entity in feed.entity:
    if (entity.HasField('vehicle') and
            (entity.vehicle.trip.route_id == "16718") and
            (entity.vehicle.trip.direction_id == westbound)):
        lat_1 = entity.vehicle.position.latitude
        lon_1 = entity.vehicle.position.longitude
        busID = entity.vehicle.vehicle.id
        now = datetime.now()
        bus_checkin_time = datetime.fromtimestamp(int(entity.vehicle.timestamp))

        time_diff = now - bus_checkin_time
        dist_meters = haversine_dist(lat_1, lon_1, lat_me, lon_me)

        print(
            f'The 14 bus with ID {busID} is {dist_meters} meters away.\n'
            f'GPS-data received {round(time_diff.total_seconds(), 0)} seconds ago.\n'
        )
