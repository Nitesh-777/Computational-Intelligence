import copy
import time

import numpy as np
from week1_travelling_salesman.my_code import tsp

def find_start_end_cities_greedy(matrix):
    min_args = [np.argsort(x)[1] for x in matrix]
    min_list = [matrix[i, min_args[i]] for i in range(len(min_args))]
    closest_city1 = np.argmin(min_list)
    closest_city2 = min_args[closest_city1]
    c1_min = np.argsort(matrix[closest_city1])[2]
    c2_min = np.argsort(matrix[closest_city2])[2]
    start_city = None
    end_city = None
    current_city = None
    if matrix[closest_city1, c1_min] < matrix[closest_city2, c2_min]:
        start_city = closest_city1
        end_city = closest_city2
        current_city = c1_min
    else:
        start_city = closest_city2
        end_city = closest_city1
        current_city = c2_min
    return start_city, end_city, current_city


def greedy(matrix):
    n_cities = len(matrix)
    tour = []
    visited = [False] * n_cities
    start_city, end_city, current_city = find_start_end_cities_greedy(matrix)
    tour.extend([start_city, current_city])
    visited[start_city], visited[current_city], visited[end_city] = True, True, True
    for x in range(n_cities - 3):
        unvisited = [i for i in range(n_cities) if not visited[i]]
        nearest_city = min(unvisited, key=lambda i: matrix[current_city, i])
        current_city = nearest_city
        visited[current_city] = True
        tour.append(current_city)
    tour.append(end_city)
    tour.append(start_city)
    return np.array(tour)


def city_swap_neighbourhood(route):
    route = list(route)
    n_cities = len(route) - 1
    routes = []
    for i in range(1, len(route) - 1):
        for x in range(2, len(route) - 1):
            new_route = copy.deepcopy(route)
            new_route[i], new_route[x] = new_route[x], new_route[i]
            if new_route not in routes:
                if new_route != route:
                    routes.append(new_route)

    return routes


def best_neighbour_step(route, neighbourhood, matrix):
    best_route = route
    lowest_cost = tsp.evaluate_tsp(matrix, route)
    for r in neighbourhood:
        cost = tsp.evaluate_tsp(matrix, r)
        if cost < lowest_cost:
            lowest_cost = cost
            best_route = r
            print(f"Best route so far: {best_route}, cost: {lowest_cost}")
    return best_route, lowest_cost


def local_search(matrix, t):
    n_cities = len(matrix)
    # best_route = tsp.random_route(n_cities)
    best_route = greedy(matrix)
    routes = city_swap_neighbourhood(best_route)
    best_route, lowest_cost = best_neighbour_step(best_route, routes, matrix)
    end_time = time.time() + t
    while time.time() < end_time:
        neighbourhood = city_swap_neighbourhood(best_route)
        r, c = best_neighbour_step(best_route, neighbourhood, matrix)
        if c < lowest_cost:
            best_route = r
            lowest_cost = c
            print(f"Best route from neighbourhood: {best_route}, cost: {lowest_cost}")
    return best_route, lowest_cost








