import numpy as np
import pandas as pd
from week1_travelling_salesman.my_code import tsp
from week2_local_search.my_code import ls

coords = pd.read_csv("cities48_10.csv").values
distances = tsp.adjacency_matrix_from_city_coords(coords)
# print(distances)
tour = ls.greedy(distances)
print(tour)

cost = tsp.evaluate_tsp(distances, tour)
print(cost)
# rr, cost = tsp.random_search(distances, 120)
# routes = ls.city_swap_neighbourhood(rr)
# print(routes)
# print(f"Random route: {rr}. cost: {cost}")
# best_route, lowest_cost = ls.best_neighbour_step(rr, routes, distances)
t = 30
# print(f"Local Search vs Random Search - {t} Seconds")
print(f"Local Search - {t} Seconds")
r, c = ls.local_search(distances, t)
# print(f"Local Search: best route: {r}, cost: {c}")
# r2, c2 = tsp.random_search(distances, t)
# print(f"Random Search: best route: {r2}, ost: {c2}")
# r3 = np.array([0, 7, 3, 1, 2, 15, 12, 11, 6, 5, 9, 8, 10, 4, 14, 13, 0])
# c3 = tsp.evaluate_tsp(distances, r3)
# print(r3, c3)




