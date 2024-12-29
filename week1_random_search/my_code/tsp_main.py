import numpy as np
import pandas as pd
import tsp


# 4 City TSP Adjacency Matrix
data = np.array([
    [0, 20, 42, 35],
    [20, 0, 30, 34],
    [42, 30, 0, 12],
    [35, 34, 12, 0]
])

routes = ["0123", "0132", "0213", "0231", "0312", "0321"]
routes_2d = np.array([list(map(int, item)) for item in routes])
print(routes_2d)

coords = pd.read_csv("ulysses16.csv").values
print(coords)

# Adjacency Matrix from ulysses.csv coordinates
distances = tsp.adjacency_matrix_from_city_coords(coords)
print(distances)

# 4 City TSP random route cost
rr = tsp.random_route(4)
print(f"route: {rr}, cost: {tsp.evaluate_tsp(data, rr)}")

# 16 City TSP random route cost from coords given
rr2 = tsp.random_route(16)
print(rr2)
print(f"route: {rr2}, cost: {tsp.evaluate_tsp(distances, rr2)}")
t = 60
print(f"{t/60} minute(s)")
route, cost = tsp.random_route_timed(distances, t)
print(f"Best timed random route: {route}, cost: {cost}, time: {t} seconds")
