import pandas as pd
import re
import string
import datetime
import numpy as np
import scipy.interpolate as spi
import scipy.sparse as spp
import matplotlib.pyplot as plt
import math

LOC_FORMAT_FLOAT  = re.compile("[a-zA-Z]+\d+\.\d+")
LOC_FORMAT_INT    = re.compile("[a-zA-Z]+\d+")
HUM_FORMAT        = re.compile("\d+\.\d+")
GROUP_FORMAT      = re.compile("\d+")
X_FORMAT          = re.compile("[a-zA-Z]+")
Y_FORMAT          = re.compile("\d+\.\d+")
ALPHABET_POSITION = {string.ascii_lowercase[i]:i for i in xrange(len(string.ascii_lowercase))}

def parse_location(location):
    parsed = LOC_FORMAT_FLOAT.match(location)
    if parsed == None:
        parsed = LOC_FORMAT_INT.match(location)
        if parsed == None:
            return float("NaN")
        else:
            return location[parsed.start():parsed.end()] + ".0"
    else:
        return location[parsed.start():parsed.end()]

def parse_humidity(humidity):
    parsed = HUM_FORMAT.match(humidity)
    if parsed == None:
        return float("NaN")
    else:
        return float(humidity[parsed.start():parsed.end()])
    
def x_coordinate(location):
    parsed = X_FORMAT.match(location)
    if parsed == None:
        return float("NaN")
    else:
        x = location[parsed.start():parsed.end()]
        tot = 0
        for char in x.lower():
            tot += ALPHABET_POSITION[char]
        return tot/float(len(x))
    
def y_coordinate(location):
    parsed = Y_FORMAT.search(location)
    if parsed == None:
        return float("NaN")
    else:
        return float(location[parsed.start():parsed.end()])
    
def td_to_sec(td):
    return td.seconds
    
def get_data(fname=None):
    if fname == None or type(fname) != str:
        fname = raw_input("data file path: ")
    try:
	    with open(fname, "rt") as csvfile:
	        data = pd.read_csv(csvfile).fillna("")
	    data.columns = ["group", "time", "temperature", "humidity", "location", "notes"]
	    data["time"] = pd.to_datetime(data["time"])
	    data["location"] = data["location"].apply(parse_location)
	    data["humidity"] = data["humidity"].apply(parse_humidity)
	    data = data.dropna()
	    data["x"] = data["location"].apply(x_coordinate)
	    data["y"] = data["location"].apply(y_coordinate) - 1
	    data["t"] = ((data["time"] - pd.datetime(2016,11,12)).apply(td_to_sec)/60).astype(int)
	    data["t_tod"] = (data["t"]%(60*60)/60).astype(int)
	    return data
    except:
        print "Error: invalid or nonexistent data file"
        get_data()
      
def fill_missing_grids(grids, xdim, ydim):
    for y in xrange(ydim):
        for x in xrange(xdim):            
            for i in xrange(24):
                if math.isnan(grids[i][y][x]):
                    p = (i-1)%24
                    n = (i+1)%24
                    while (math.isnan(grids[p][y][x]) and p != i): p = (p-1)%24
                    while (math.isnan(grids[n][y][x]) and n != i): n = (n+1)%24
                    if p != n:
                        inc = float(grids[n][y][x] - grids[p][y][x])/((n-p)%24)
                        j = 1
                        k = (p+1)%24
                        while k != n:
                            grids[k][y][x] = grids[p][y][x] + j*inc
                            k = (k+1)%24
                            j += 1
    return grids
        
def create_grids(data):
    points = dict()
    for pt, vals in data.groupby("point"):
        points[pt] = vals["value"].mean()
    grid = np.array([[float("NaN") for i in xrange(12)] for j in xrange(8)])
    for pt in points:
        grid[int(2*pt[1])][int(2*pt[0])] = points[pt]
    return grid
        
def plottable_data(fname=None):
    raw_data = get_data(fname)
    df = pd.DataFrame()
    df["point"], df["value"], df["t"] = zip(raw_data["x"], raw_data["y"]), raw_data["temperature"], raw_data["t_tod"]
    grids = dict()
    for t, data in df.groupby("t"):
        grids[t] = create_grids(data)
    for i in xrange(24):
        if not i in grids:
            grids[i] = np.array([[float("NaN") for j in xrange(12)] for k in xrange(8)])
    grids = fill_missing_grids(grids, 12, 8)
    return grids

if __name__ == "__main__":
    grids = plottable_data()
    i = 0
    plt.imshow(plt.imread("ta.png"), extent=[-0.5,8,6.5,-0.5])
    p = plt.imshow(grids[0], cmap="YlOrRd", interpolation="bilinear", alpha=10)
    fig = plt.gcf()
    plt.axis("off")
    plt.clim(20,27)
    plt.title("Temperature in Tung Au at 0:00")
    while(True):
        p.set_data(grids[i])
        plt.title("Temperature in Tung Au at %d:00"%i)
        plt.pause(0.1)
        i = (i+1)%24
