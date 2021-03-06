import sys
from math import asin, sin, cos, sqrt, radians
from time import sleep

import urllib.request
import urllib.response

from datetime import datetime, timedelta
from google.transit import gtfs_realtime_pb2
from phue import Bridge

"""
Route and arrival data used in this product or service is provided by permission of TransLink. 
TransLink assumes no responsibility for the accuracy or currency of the Data used in this product or service.
"""


# Function definitions
# TODO: store the last two unique GPS points and calculate the speed of the bus to forward prop the position
#       Use the timestamp field to determine if the GPS point is unique.
# REQUIRES: a list of valid latitude, longitude, and time tuples. The list should be of length three.
# EFFECTS: Calculates the naive average speed given the last three unique GPS positions and their times
def gps_bus_speed(lat_lon_pairs):
    # data [(lat, lon, datetime), (lat, lon, datetime), (lat, lon, datetime)]
    # stub
    return 0.0


# EFFECTS: Loads a text file or returns an error if the file cannot be found.
def load_file(path):
    try:
        with open(path) as f:
            d = f.readlines()
            d = list(map(lambda s: s.strip(), d))
            return d
    except IOError:
        sys.exit(f"Error: file [{path}] not found. Check that the path is correct and the file exists.")


# TODO: check initial Earth radius estimate. Differences are too high between this function and more precise
#       iterative solutions.
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


# Constants
data = load_file(r"data\my_location.txt")
lat_me = float(data[0])
lon_me = float(data[1])
API_KEY = data[2]
bridge_ip = data[3]
westbound = 1
eastbound = 0
lights_flag = False

if lights_flag:
    # connect to the bridge
    b = Bridge(bridge_ip)
    b.connect()
    # create a light grouping and turn them on
    lr_lamp = [1]
    command = {'on': True, 'bri': 127}
    b.set_light(lr_lamp, command)
    # print(b.get_api())

for n in range(500):

    feed = gtfs_realtime_pb2.FeedMessage()
    response = urllib.request.urlopen('https://gtfs.translink.ca/v2/gtfsposition?apikey=' + API_KEY)
    feed.ParseFromString(response.read())
    green_dist = []
    red_dist = []

    for entity in feed.entity:
        if (entity.HasField('vehicle') and
                (entity.vehicle.trip.route_id == "16718") and
                (entity.vehicle.trip.direction_id == westbound)):
            # print(entity)
            lat_1 = entity.vehicle.position.latitude
            lon_1 = entity.vehicle.position.longitude
            busID = entity.vehicle.vehicle.id
            now = datetime.now()
            bus_checkin_time = datetime.fromtimestamp(int(entity.vehicle.timestamp))

            time_diff = now - bus_checkin_time
            dist_meters = haversine_dist(lat_1, lon_1, lat_me, lon_me)
            # TODO: set light color logic using traffic light system.
            # TODO: incorporate RTTI as GPS data might not be frequent enough to be reliable at this scale of prediction
            if ((lon_1 > lon_me) and
                    (dist_meters < 1300) and
                    (dist_meters > 500) and
                    (time_diff < datetime.timedelta(seconds=90))):
                green_dist.append(dist_meters)
            # print("A westbound 14 is close! Leave now!")
            if lon_1 > lon_me:
                print(
                    f'The 14 bus with ID {busID} is {dist_meters} meters away.\n'
                    f'GPS-data received {round(time_diff.total_seconds(), 0)} seconds ago.\n'
                )
    print(green_dist)
    if lights_flag:
        if not len(green_dist):
            b.set_light(lr_lamp, 'xy', [0.6679, 0.2969])
            print('turn red')
        else:
            b.set_light(lr_lamp, 'xy', [0.2206, 0.662])
            print('turn green')

    print('------------------------------------------------------------------------')

    sleep(20)
