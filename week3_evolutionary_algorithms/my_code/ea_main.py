import ea
from week1_travelling_salesman.my_code import tsp
import pandas as pd

coords = pd.read_csv("cities48_10.csv").values
distances = tsp.adjacency_matrix_from_city_coords(coords)

def evaluate(route):
    return tsp.evaluate_tsp(distances, route)

# pop = ea.fill_population(10, 16)
# children = ea.fill_population(5, 16)
# print(pop)
# parents = ea.select_parents(pop, evaluate, 3, 5)
# new_pop = ea.select_survivors(pop, children, evaluate, 5)
# ea.mutation(pop[0])
# pop2 = ea.fill_population(2, 16)
# ea.combination(pop2)
ea.run(67, 10, evaluate, 60, 15, 4, 10)


