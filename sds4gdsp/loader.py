import random
import numpy as np
import osmnx as ox
from shapely.geometry import (
    Point, LineString, Polygon
)

def make_points(num_points, lng_min, lng_max, lat_min, lat_max):
    coords = []
    for _ in range(num_points):
        lng = random.uniform(lng_min, lng_max)
        lat = random.uniform(lat_min, lat_max)
        coords.append((lng, lat))
    return coords

def make_lines(points):
    random.shuffle(points)
    lines = []
    for orig, dest in zip(points, points[1:]):
        if random.choices([True, False], [30, 70], k=1)[0]:
            lines.append(LineString([orig, dest]))
    return lines

def make_polygon(points):
    return Polygon(points)

def make_spatial_data(n):
    coords = np.random.random((n, 2))
    points = list(map(lambda z: Point(z), coords))
    lines = LineString(points)
    lines = list(map(lambda x: LineString(x), list(zip(points, points[1:]))))
    polygon = Polygon(points)
    return points, lines, polygon

def make_graph(
    origin, network_type, dist=500, dist_type="bbox", retain_all=False, simplify=True
):
    # query the road network using OSMNx
    G = ox.graph_from_point(
        center_point=origin, # origin point of query
        dist=dist, # radius in meters from the origin
        dist_type=dist_type, # examples is `bbox`
        retain_all=retain_all, # filter connected components?
        simplify=simplify, # simplify network topology
        network_type=network_type # filter to <insert type from OSM> roads
    )
    return G

def get_coord_sequence(G, route):
    route_coords = []
    for node in route:
        route_coords.append((G.nodes[node]["x"], G.nodes[node]["y"]))
    return route_coords