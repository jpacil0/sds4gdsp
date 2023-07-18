import math
import numpy as np
import pandas as pd
from shapely.geometry import Point
from typing import List
from shapely.wkt import loads
from itertools import combinations
from networkx import Graph
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=False)

def get_coords_from_graph(G: Graph, nodes: List[int]):
    """Fetch lat/lng coords from graph given a list of nodes."""
    coords = []
    for node in nodes:
        coords.append((G.nodes[node]["x"], G.nodes[node]["y"]))
    return coords

def dedupe_points(points: List[Point], distance_threshold: int):
    """Naive way to dedupe a points dataset given a distance threshold in meters."""
    pointpairs_df = pd.DataFrame(list(combinations(points, 2)), columns=["p1", "p2"])
    pointpairs_df = pointpairs_df.applymap(lambda x: x.wkt)
    pointpairs_df["distance"] = pointpairs_df.parallel_apply(lambda x: calc_haversine_distance(x.p1, x.p2), axis=1)
    points_df = pointpairs_df.groupby("p1").distance.min().reset_index(name="min_distance")
    pass_threshold = points_df.min_distance >= distance_threshold
    points_df = points_df.loc[pass_threshold].reset_index(drop=True)
    deduped_points = points_df.p1.tolist()
    return deduped_points

def calc_haversine_distance(p1: str, p2: str) -> float:
    """Compute for the great circle distance between two points on the earth."""
    p1, p2 = loads(p1), loads(p2)
    lng1, lat1 = p1.x, p1.y
    lng2, lat2 = p2.x, p2.y
    R = 6371 # radius of earth in kilometers
    # convert decimal degrees to radians
    lng1, lat1, lng2, lat2 = map(math.radians, [lng1, lat1, lng2, lat2])
    # haversine formula
    dlon = lng2 - lng1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    d = c * R * 1_000 # convert back to meters
    return d

def softmax(arr: np.ndarray) -> np.ndarray:
    # subtracting the max value for numerical stability
    e_x = np.exp(arr - np.max(arr))
    return e_x / np.sum(e_x)

def z_score(col):
    return (col - col.mean()) / col.std()