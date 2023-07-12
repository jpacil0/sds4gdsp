def get_coord_sequence(G, route):
    route_coords = []
    for node in route:
        route_coords.append((G.nodes[node]["x"], G.nodes[node]["y"]))
    return route_coords