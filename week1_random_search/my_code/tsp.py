import numpy as np
import time


def random_route(n_cities):
    route = np.arange(1, n_cities)
    np.random.shuffle(route)
    route = np.insert(route, 0, 0)
    route = np.append(route, 0)
    return route


def adjacency_matrix_from_city_coords(coords):
    def distance(x, y):
        return np.sqrt(np.square(x[0] - y[0]) + np.square(x[1] - y[1]))

    adjacency_matrix = [[distance(x, y) for x in coords] for y in coords]
    return np.array(adjacency_matrix)


def evaluate_tsp(matrix, route_array):
    cost = np.sum([matrix[route_array[i], route_array[i + 1]] for i in range(len(route_array) - 1)])
    return cost


def random_search(matrix, t):
    best_route = random_route(len(matrix))
    lowest_cost = evaluate_tsp(matrix, best_route)
    end_time = time.time() + t
    while time.time() < end_time:
        rr = random_route(len(matrix))
        cost = evaluate_tsp(matrix, rr)
        if cost < lowest_cost:
            best_route = rr
            lowest_cost = cost
    return best_route, lowest_cost
