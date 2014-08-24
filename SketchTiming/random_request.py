#!/usr/bin/env python3

import json
import urllib.request
import random
import hashlib
import pickle

# min_lon, min_lat, max_lon, max_lat
#BOUNDING_BOX = [[5.8680205345,47.4621802938],[15.0623626709,54.6570114861],]
BOUNDING_BOX = [[8.2521,48.7822],[9.3055,49.6417]]
SERVER = "127.0.0.1:5000"
REQUEST = "http://%(server)s/sketch?z=%(zoom)i&output=json&loc=%(start_lat)f,%(start_lon)f&loc=%(end_lat)f,%(end_lon)f"

NUM_REQUESTS = 10000
# use first 8 bytes of SHA2 hash of OSRM as seed
RANDOM_SEED = int.from_bytes(hashlib.sha224("OSRM".encode("utf-8")).digest()[:8], 'big')

random.seed(RANDOM_SEED)

def get_random_lat():
    return random.uniform(BOUNDING_BOX[0][1], BOUNDING_BOX[1][1])
def get_random_lon():
    return random.uniform(BOUNDING_BOX[0][0], BOUNDING_BOX[1][0])

data = []

inc = NUM_REQUESTS / 20

print("Sending %i request" % NUM_REQUESTS)

for i in range(NUM_REQUESTS):
    if i % inc == 0:
        print(".", end="")
    start_lat = get_random_lat()
    start_lon = get_random_lon()
    end_lat = get_random_lat()
    end_lon = get_random_lon()

    config = {'server': SERVER, 'zoom': 6,
              'start_lat': start_lat,
              'start_lon': start_lon,
              'end_lat': end_lat,
              'end_lon': end_lon
             }

    try:
        request = urllib.request.urlopen(REQUEST % config)
    except urllib.error.HTTPError:
        continue
    reply = request.read().decode("utf-8")
    try:
        obj = json.loads(reply)
    except ValueError:
        print(reply)
    data.append(obj)

f = open("requests.pickle", "wb")
pickle.dump(data, f)

print("\nFinished.")

