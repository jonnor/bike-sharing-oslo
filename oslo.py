
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
from sklearn.cluster import AffinityPropagation
import matplotlib.pyplot as plt
from graphviz import Digraph
import folium

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
    try:    
        station_id = int(station_id)
    except ValueError as e:
        return None

    station = stations_by_id.get(station_id, None)
    if not station:
        return None
    point = station['center']
    return (point['latitude'], point['longitude'])

def calculate_distance(stations, row):
    start = station_location(stations, row['Start station'])
    end = station_location(stations, row['End station'])
    if start is None or end is None:
        return math.nan
    dist = geopy.distance.great_circle(start, end)
    return dist.meters

## Map plotting
def create_map(**kwargs):
    map_center = [59.925, 10.75]
    map_zoom = 12
    base_map = folium.Map(location=map_center, zoom_start=map_zoom, control_scale=False, **kwargs)
    return base_map


## Clustering
def cluster_connected(frame, n_clusters=9, method='spectral'):
    # Create affinity matrix
    outbound = pandas.crosstab(frame['Start station'], frame['End station'])
    inbound = pandas.crosstab(frame['End station'], frame['Start station'])

    connectivity = inbound + outbound
    numpy.fill_diagonal(connectivity.values, 0)

    # Perform clustering
    cluster = method
    if method == 'affinitypropagation':
        cluster = AffinityPropagation(affinity='precomputed')
    elif method == 'spectral':
        cluster = SpectralClustering(n_clusters=n_clusters, affinity='precomputed')        

    labels = cluster.fit_predict(connectivity)
    no_clusters = len(set(labels))

    # Map back to station IDs
    station_clusters = [ [] for n in range(0, no_clusters) ]
    for idx, label in enumerate(labels):
        station = connectivity.columns[idx]
        #print(idx, station, label)
        station_clusters[label].append(station)

    station_clusters = sorted(station_clusters, key=len, reverse=True)

    if method == 'affinitypropagation':
        return (station_clusters, cluster.cluster_centers_indices_, inbound.columns)
    else:
        return station_clusters

colors = ['red', 'blue', 'green', 'orange', 'magenta', 'yellow', 'black', 'grey', 'darkblue', 'orangered', 'pink', 'aqua', 'white', 'white', 'white' ]


def plot_station_groups(stations, station_groups, center_stations=None, station_size=4.0):
    assert len(colors) >= len(station_groups), "Missing colors %d" % (len(colors)-len(station_groups),)

    connectivity_map = create_map()
        
    for idx, cluster in enumerate(station_groups):
        for station_id in cluster:
            station = stations.get(station_id, None)
            if not station:
                continue
            center = station['center']
            lon, lat = center['longitude'], center['latitude']
            color = colors[idx]
    
            edge_color = color
            size = station_size
            if center_stations and station_id in center_stations: 
                size *= 2.0
                edge_color = '#000000'

            folium.CircleMarker([lat, lon],
                        weight=2.0,
                        radius=size, popup=station['title'],
                        color=edge_color, fill_color=color,
            ).add_to(connectivity_map)

    return connectivity_map

# Calculate connenectivity within clusters, and between them
def cluster_id_for_station(clusters, station_id):
    for cluster_idx, cluster in enumerate(clusters):
        if station_id in cluster:
            return cluster_idx
    return None


def cluster_stats(stations, df, clusters):

    out = numpy.empty((len(clusters), len(clusters)))

    for from_cluster in range(0, len(clusters)):
        for to_cluster in range(0, len(clusters)):

            to_stations = clusters[to_cluster]
            from_stations = clusters[from_cluster]

            is_outbound = df['Start station'].isin(from_stations) & df['End station'].isin(to_stations)
            is_inbound = df['End station'].isin(from_stations) & df['Start station'].isin(to_stations)
            inbound, outbound = df[is_inbound], df[is_outbound]
            
            out[from_cluster][to_cluster] = inbound.shape[0]
            out[to_cluster][from_cluster] = outbound.shape[0]           

    return pandas.DataFrame(data=out)


# Return a graphviz showing cluster connectivity
def cluster_digraph(clusters, stats, title=None, label_threshold=0.03, nodesize=1.0):
    total_trips = stats.sum().sum()
    dot = Digraph(comment=title)

    biggest = len(clusters[0])

    # Add nodes
    for cluster_id, data in stats.iterrows():
        node_name = str(cluster_id)
        dot.attr('node', fontcolor='white')
        # Color node to same as plots
        dot.attr('node', style='filled', fillcolor=colors[cluster_id])
        # Area proportional to size of cluster
        size = math.sqrt((len(clusters[cluster_id]) / biggest)) * nodesize
        dot.attr('node', fixedsize='true', width=str(size))
        dot.node(str(cluster_id), node_name, shape='circle')

    def rel_trips(from_, to):
        rel = (stats.values[from_][to])/total_trips
        return rel

    def label_edge(val):
        # Only put number on label if big enough
        if val < label_threshold:
            return None
        else:
            return "%d%%" % (val*100,)

    def create_edge(f, t):
        from_id = str(f)
        to_id = str(t)

        if from_cluster == to_cluster:
            label = label_edge(rel_trips(f, t))
            dot.edge(from_id, to_id, label=label)
        else:
            dot.edge(from_id, to_id, label=label_edge(rel_trips(f, t)))
            dot.edge(to_id, from_id, label=label_edge(rel_trips(t, f)))

    no_clusters = len(clusters)
    for from_cluster in range(0, no_clusters):
        for to_cluster in range(from_cluster, no_clusters):
            create_edge(from_cluster, to_cluster)

    return dot
