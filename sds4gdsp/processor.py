import math
import numpy as np
import pandas as pd
from functools import reduce
from shapely.geometry import Point
from typing import List
from shapely.wkt import loads
from itertools import combinations
from networkx import Graph
from pandarallel import pandarallel
pandarallel.initialize(verbose=0, progress_bar=False)
from scipy.stats import truncnorm

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd
    )

def get_coords_from_graph(G: Graph, nodes: List[int]):
    """Fetch lat/lng coords from graph given a list of nodes."""
    coords = []
    for node in nodes:
        coords.append((G.nodes[node]["x"], G.nodes[node]["y"]))
    return coords

def convert_cel_to_point(cel_id: str, ref: pd.DataFrame):
    """Convert cellsite to shapely point."""
    coord = ref.loc[ref.uid==cel_id].coords.item()
    point = loads(coord)
    return point

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

def apply_softmax(arr: np.ndarray) -> np.ndarray:
    # subtracting the max value for numerical stability
    e_x = np.exp(arr - np.max(arr))
    return e_x / np.sum(e_x)

def convert_distances_to_probas(distances) -> np.ndarray:
    reversed_distances = distances ** -1
    probas = apply_softmax(reversed_distances)
    return probas

def scale_feature(feature, scaler) -> np.ndarray:
    return scaler.fit_transform(np.array(feature).reshape(-1, 1)).flatten()

def calc_total_travel_distance(traj):
    coords = traj.coords.tolist()
    od_pairs = list(zip(coords, coords[1:]))
    total_travel_distance = reduce(
        lambda a, b: a + b,
        list(map(lambda p: calc_haversine_distance(*p), od_pairs))
    )
    return total_travel_distance

def fetch_total_travel_distance(traj):
    coords = traj.coords.tolist()
    od_pairs = list(zip(coords, coords[1:]))
    dts = traj.transaction_dt.tolist()
    hrs = traj.transaction_hr.tolist()
    cels = traj.cel_uid.tolist()
    hr_pairs = list(zip(hrs, hrs[1:]))
    travel_distances = list(map(lambda p: calc_haversine_distance(*p), od_pairs))
    dt_df = pd.DataFrame(list(zip(dts, dts[1:])), columns=["orig_dt", "dest_dt"])
    hr_df = pd.DataFrame(list(zip(hrs, hrs[1:])), columns=["orig_hr", "dest_hr"])
    cel_df = pd.DataFrame(list(zip(cels, cels[1:])), columns=["orig_cel", "dest_cel"])
    data = pd.concat([dt_df, hr_df, cel_df], axis=1)
    data["travel_distance"] = travel_distances
    return data.loc[data.travel_distance>0].reset_index(drop=True)