import copy
import random
import time
from week1_travelling_salesman.my_code import tsp
import numpy as np

# r = tsp.random_route(16)


def representation(route):
    route = route[1:-1]
    return route


def unrepresented(route):
    route.insert(0, 0)
    route.append(0)
    return route


def maximisation(cost):
    cost = 1 / cost
    return cost


def maximisation_power(cost, power):
    cost = 1 / (cost ** power)
    return cost


def fill_population(n_pop, n_cities):
    pop = [list(tsp.random_route(n_cities)) for i in range(n_pop)]
    return pop


def select_parents(pop, evaluate, N_OFFSPRING, power):
    # costs = [evaluate(c) for c in pop]
    # print(costs)
    # costs_maxed = [maximisation(evaluate(c)) for c in pop]
    # p_costs = [c / (np.sum(costs_maxed)) for c in costs_maxed]
    # print(costs_maxed)
    # print(p_costs)
    # print(np.sum(p_costs))
    costs_maxed_power = [maximisation_power(evaluate(c), power) for c in pop]
    p_costs_power = [c / (np.sum(costs_maxed_power)) for c in costs_maxed_power]
    # print(costs_maxed_power)
    # print(p_costs_power)
    # print(np.sum(p_costs_power))
    pop_indexes = np.arange(len(pop))
    # print(pop_indexes)
    winners_indexes = np.random.choice(pop_indexes, replace=False, size=N_OFFSPRING, p=p_costs_power)
    # print(winners_indexes)
    # parents_costs = [evaluate(pop[i]) for i in winners_indexes]
    parents = [pop[i] for i in winners_indexes]
    # print(parents)
    # print(parents_costs)
    return parents


def select_survivors(pop, evaluate, n_pop):
    costs = [evaluate(c) for c in pop]
    sorted_pop = sorted(zip(pop, costs), key=lambda x: x[1])
    # print(sorted_pop)
    lowest_pop = sorted_pop[:n_pop]
    new_pop, lowest_costs = zip(*lowest_pop)
    # print(new_pop)
    # print(lowest_costs)
    return new_pop


def mutation(route, p_mutation):
    p = p_mutation / 100
    if random.random() < p:

        # print(np.arange(1, len(route) - 1))
        swap_numbers = np.random.choice(np.arange(1, len(route) - 1), size=2, replace=False)
        # print(swap_numbers)
        # print(route)
        mutated_route = copy.deepcopy(route)
        mutated_route[swap_numbers[0]], mutated_route[swap_numbers[1]] = mutated_route[swap_numbers[1]], mutated_route[
            swap_numbers[0]]
        # print(mutated_route)
    else:
        mutated_route = route
    return mutated_route


def crossover(p1, p2, p_crossover):
    def cutting(p1, p2):
        cut_length = int(np.floor(len(p1) / 2))
        # print(cut_length)
        start_index = np.random.randint(0, len(p1))
        end_index = int((start_index + cut_length) % len(p1))
        # print(start_index, end_index)
        cut2 = []
        if start_index < end_index:
            cut = p1[start_index:end_index]
            # print(p2[end_index:])
        else:
            cut = p1[start_index:] + p1[:end_index]

        # cut2 = []
        # for i in range(end_index, len(p2)):
        #     if p2[i] not in cut:
        #         cut2.append(p2[i])
        # for i in range(0, end_index):
        #     if p2[i] not in cut:
        #         cut2.append(p2[i])
        cut2 = [i for i in p2[end_index:] + p2[:end_index] if i not in cut]
        # print(p1)
        # print(p2)
        # print(cut)
        # print(cut2)

        if end_index == 0:
            # child = cut2 + cut
            child = cut2 + cut
        elif start_index < end_index:
            end = len(p1) - end_index
            # print(end)
            # child = cut2[end:] + cut + cut2[:end]
            child = cut2[end:] + cut + cut2[:end]
        else:
            start = len(p1) - start_index
            # print(start)
            # child = cut[start:] + cut2 + cut[:start]
            child = cut[start:] + cut2 + cut[:start]
        child = unrepresented(child)
        return child
        # print(child)
    p = p_crossover / 100
    if random.random() < p:
        p1 = representation(p1)
        p2 = representation(p2)
        child1 = cutting(p1, p2)
        child2 = cutting(p2, p1)
    else:
        child1, child2 = p1, p2
    return child1, child2


def run(n_pop, n_cities, evaluate, p_mutation, p_crossover,f_power, t):
    iter = 0
    pop = fill_population(n_pop, n_cities)
    end_time = time.time() + t
    while time.time() < end_time:
        n_parents = int(np.floor(len(pop) / 2))
        # print(n_parents)
        parents = select_parents(pop, evaluate, n_parents, f_power)
        # print(parents)
        children = []
        for i in range(0, len(parents) - 1, 2):
            child1, child2 = crossover(parents[i], parents[i + 1], p_crossover)
            child3, child4 = crossover(parents[i + 1], parents[i], p_crossover)
            child5, child6 = crossover(parents[i], parents[len(parents) - 1 - i], p_crossover)
            children.extend([child1, child2, child3, child4, child5, child6])
            # children.append(child2)
            # children.append(child3)
            # children.append(child4)
            # children.append(child5)
            # children.append(child6)
        # children1 = [crossover(parents[i], parents[i + 1]) for i in range(0, len(parents) - 1, 2)]
        # print(children1)
        # children2 = [crossover(parents[i + 1], parents[i]) for i in range(0, len(parents) - 1, 2)]
        # children3 = [crossover(parents[i], parents[len(parents) - 1 - i]) for i in range(0, len(parents) - 1, 2)]
        # children4 = [crossover(parents[len(parents) - 1 - i], parents[i]) for i in range(0, len(parents) - 1, 2)]
        # children5 = [crossover(parents[i], parents[(i + 5) % len(parents)]) for i in range(len(parents))]
        # print(len(children1))
        # print(len(children2))
        # print(len(children3))
        # print(len(children4))
        # print(len(children5))
        # children = children1 + children2 + children3
        # print(len(children))
        # print(children)
        new_pop = parents + children
        # print(len(new_pop))
        # print(new_pop)
        mutated_pop = [mutation(c, p_mutation) for c in new_pop]
        # print(len(mutated_pop))
        # pop = select_survivors()
        # def same(c1, c2):
        #     if np.array_equal(c1, c2):
        #         return c1
        # print(mutated_pop)
        # l = [len(mutated_pop[i]) for i in range(len(mutated_pop))]
        # print(l)
        # same_pop = [same(new_pop[i], mutated_pop[i]) for i in range(len(new_pop))]
        # print(len(same_pop))
        # print(same_pop)
        pop = select_survivors(mutated_pop, evaluate, n_pop)
        # print(len(pop))
        iter += 1
        print(f"Best route so far: {pop[0]}, cost: {evaluate(pop[0])} ITERATION:{iter}")
    print(f"Best route in {t} seconds was {pop[0]}, cost: {evaluate(pop[0])} ")
