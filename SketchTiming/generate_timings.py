#!/usr/bin/env python3

import pickle
import numpy as np
import polyline
from intersection import num_self_intersections

f = open("requests.pickle", "rb")
data = [r for r in pickle.load(f) if r["statistics_data"]["input_length"] > 0]

TIME_UNIT = "usec"
SHUFFLE_CONSTANT = 0.000001

statistics_data = [r["statistics_data"] for r in data]

print("Decoding...")
routes = [polyline.decode(r["route_geometry"]) for r in data]
sketches = [polyline.decode(r["schematized_geometry"]) for r in data]

more_intersections = 0
less_intersections = 0
same_intersections = 0

less_diffs = []
more_diffs = []

print("Testing intersection..")
for r, s in zip(routes, sketches):
    num_r = num_self_intersections(r)
    num_s = num_self_intersections(s)
    if num_r == num_s:
        same_intersections += 1
    if num_r > num_s:
        less_intersections += 1
        less_diffs.append(num_r - num_s)
    if num_r < num_s:
        more_intersections += 1
        more_diffs.append(num_s - num_r)

print("Self-Intersections")
print("less: #%i -%.02f" % (less_intersections, len(less_diffs) and np.average(less_diffs)))
print("same: #%i" % same_intersections)
print("more: #%i +%.02f" % (more_intersections, len(more_diffs) and np.median(more_diffs) or 0))

series = {}
for i, d in enumerate(statistics_data):
    for s in d:
        if s not in series:
            if s.startswith("time_"):
                series[s] = np.zeros((len(statistics_data), 1), np.float32)
            else:
                series[s] = np.zeros((len(statistics_data), 1), np.int32)
        series[s][i] = d[s]

def compute_statistics(data):
    avg = np.average(data)
    var = np.var(data)
    max = np.max(data)
    min = np.min(data)
    hist = np.histogram(data, 10, (0, max))
    return (avg, var, min, max, hist)

series = { s: compute_statistics(series[s]) for s in series}

print("Used %i samples." % len(statistics_data))
for k in sorted(series):
    (avg, var, min, max, hist) = series[k]
    if k.startswith("time_"):
        print("%s: ~%f (+- %f) [%f - %f] %s" % (k, avg, var, min, max, TIME_UNIT))
    else:
        print("%s: ~%f (+- %f) [%f - %f]" % (k, avg, var, min, max))
    #print(hist)

