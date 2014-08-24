#!/usr/bin/env python3

import pickle
import numpy as np

f = open("requests.pickle", "rb")
data = pickle.load(f)

TIME_UNIT = "usec"

statistics_data = [r["statistics_data"] for r in data if r["statistics_data"]["input_length"] > 0]

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

