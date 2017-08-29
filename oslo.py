
# Standard library
import json
import calendar
import urllib.request
import math
import os.path
from datetime import datetime
from io import BytesIO
from zipfile import ZipFile

# External dependencies
import pandas
import geopy.distance
import numpy
from mpl_toolkits.basemap import Basemap
from sklearn.cluster import SpectralClustering
import matplotlib.pyplot as plt
from graphviz import Digraph

# Tools for downloading dataset
def trips_basename(year, month):
    firstday, lastday = (1, calendar.monthrange(year, month)[1])
    return "trips-{year}.{month}.{firstday}-{year}.{month}.{lastday}".format(**locals())
def trips_url(year, month):
    base = trips_basename(year, month)
    extension = '.csv.zip'
    server_dir = 'http://oslo-citybike.s3.amazonaws.com/exports/'
    return server_dir + base + extension

def download_trip(year, month):    
    url = trips_url(year, month)
    filename = trips_basename(year, month) + '.csv'
    outpath = "data/"+filename
    if os.path.exists(outpath):
        print('skipping existing %s' % (url))
        return outpath
    
    print('downloading %s' % (url,))
    
    # Download ZIP to memory
    # ZipFile requires seek() which urlib does not implement
    temp = BytesIO()
    temp.write(urllib.request.urlopen(url).read())
    zipfile = ZipFile(temp)

    # Write to disk
    csvfile = open(outpath, 'wb+')
    csvfile.write(zipfile.read(filename))

    csvfile.close()
    zipfile.close()
    return outpath

def months_between(start, end):
    periods = []
    current = list(start)
    while (current != list(end)):
        periods.append(tuple(current))

        # calculate next
        if current[1] == 12:
            # end of year
            current[0] += 1
            current[1] = 1
        else:
           # just new month
           current[1] += 1
    return periods


# Station information
def read_stations():
    stations = json.loads(open('data/oslo_stations.json', 'r').read())

    stations_by_id = {} # id -> data
    for station in stations['stations']:
        station_id = station['id']
        # sanity checking
        if not isinstance(station_id, int):
            raise ValueError("Station identifier not an integer: %s" % repr(station_id))
        if stations_by_id.get(station_id):
            raise ValueError("Duplicate station id: %d" % (station_id,))
        stations_by_id[station_id] = station

    return stations_by_id


# Enrich trip data with distance of the trip
def station_location(stations_by_id, station_id):
    station = stations_by_id.get(station_id, None)
    if not station:
        return None
    point = station['center']
    return (point['latitude'], point['longitude'])

def calculate_distance(row):
    start = station_location(int(row['Start station']))
    end = station_location(int(row['End station']))
    if start is None or end is None:
        return math.nan
    dist = geopy.distance.great_circle(start, end)
    return dist.meters

## Map plotting
def create_map():
    # http://spatialreference.org/ref/epsg/27393/
    epsg=27393 # Oslo III
    epsg=3857 # Implies some Mercator projection, need to set upper/lower corners and lat_ts

    m = Basemap(resolution='l', epsg=epsg,
                llcrnrlon=10.70, urcrnrlon=10.80, llcrnrlat=59.90, urcrnrlat=59.94,
                lat_ts=59.93)

    m.arcgisimage()
    return m


## Clustering
def cluster_connected(frame, n_clusters=9):
    # Create affinity matrix
    outbound = pandas.crosstab(frame['Start station'], frame['End station'])
    inbound = pandas.crosstab(frame['End station'], frame['Start station'])

    connectivity = inbound + outbound
    numpy.fill_diagonal(connectivity.values, 0)
    connectivity[:4]

    # Perform clustering
    cluster = SpectralClustering(n_clusters=n_clusters, affinity='precomputed')
    labels = cluster.fit_predict(connectivity)
    labels

    # Map back to station IDs
    station_clusters = [ [] for n in range(0, n_clusters) ]
    for idx, label in enumerate(labels):
        station = connectivity.columns[idx]
        #print(idx, station, label)
        station_clusters[label].append(station)

    station_clusters = sorted(station_clusters, key=len, reverse=True)
    return station_clusters

def plot_station_groups(stations, station_groups):
    colors = ['red', 'blue', 'orange', 'magenta', 'yellow', 'aqua', 'darkblue', 'orangered', 'pink', 'black', 'grey' ]
    assert len(colors) >= len(station_groups), "Missing colors %d" % (len(colors)-len(station_clusters),)

    connecivity_map = create_map()
        
    for idx, cluster in enumerate(station_groups):
        for station_id in cluster:
            station = stations.get(station_id, None)
            if not station:
                continue
            center = station['center']
            lon, lat = center['longitude'], center['latitude']
            color = colors[idx]
            poly = connecivity_map.tissot(lon,lat,0.0004,64,facecolor=color,zorder=10,alpha=1.0)

    ax = plt.gca()
    return ax

# Calculate connenectivity within clusters, and between them
def cluster_id_for_station(clusters, station_id):
    for cluster_idx, cluster in enumerate(clusters):
        if station_id in cluster:
            return cluster_idx
    return None
            
    
def cluster_series(stations, clusters):
    s = {}
    for station_id in stations.keys():
        cluster_id = cluster_id_for_station(clusters, station_id)
        if cluster_id is not None:
            s[station_id] = cluster_id
    series = pandas.Series(s, dtype='int64')
    return series

def cluster_stats(stations, df, clusters):

    def trips_for_cluster(counts, cluster_id):
        return counts[counts['Cluster'] == cluster_id].sum()[1:]
    
    self_trips = df[df['End station'] == df['Start station']]
    without_self = df[df['End station'] != df['Start station']]
    trips_by_end = without_self.groupby('End station').count()['Start station']
    trips_by_start = without_self.groupby('Start station').count()['End station']
    trip_counts = pandas.DataFrame.from_dict({
        'Outbound': trips_by_start,
        'Inbound': trips_by_end,
        'Internal': self_trips.count()['Start station'],
        'Cluster': cluster_series(stations, clusters),
    })
    clustered_trips = [trips_for_cluster(trip_counts, idx) for idx, _ in enumerate(clusters)]

    return pandas.DataFrame(data=clustered_trips)


# Return a graphviz showing cluster connectivity
def cluster_digraph(stats, title=None, label_threshold=3):
    # FIXME: need to have data for which cluster edge goes to
    total_trips = stats.sum().sum()
    dot = Digraph(comment=title)
    for cluster_id, data in stats.iterrows():
        node_name = str(cluster_id)
        dot.node(str(cluster_id), node_name)
        
        for target_id in range(0, len(stats)):
            if target_id == cluster_id:
                n = data['Internal']/total_trips * 100
                dot.edge(str(cluster_id), str(cluster_id), label="%d%%" % (n,))
            else:
                n = data['Outbound']/total_trips * 100
                label = None
                if n >= label_threshold:
                    label = "%d%%" % (n,)
                dot.edge(str(cluster_id), str(target_id), label=label)

    return dot
