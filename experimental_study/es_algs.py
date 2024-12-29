import copy
import random
import numpy as np


# Creates groups of activities based on given constraints and available resources
def group_based_rep(sl, pl, q, cutoff):

    # Generates all valid activities based on the pieces, their quantities, and constraints
    def stock_activities(pl, quantities, max_length, cutoff):

        # Recursively builds valid activities while adhering to constraints
        def check_activity(activity, start, remaining_q):
            total_length = sum(activity)
            max_unused = max_length - total_length

            # Check if activity is valid based on length constraints
            if total_length <= max_length and max_unused <= cutoff:
                yield activity

            # Stop recursion if total length exceeds the max allowed length
            if total_length >= max_length:
                return

            # Iterate through available pieces to construct new activities
            for i in range(start, len(pl)):
                if remaining_q[i] > 0:
                    next_remaining_quantities = remaining_q.copy()
                    next_remaining_quantities[i] -= 1
                    yield from check_activity(activity + [pl[i]], i, next_remaining_quantities)

        # Initialise quantities for available pieces
        initial_quantities = [quantities[pl.index(x)] for x in pl]
        yield from check_activity([], 0, initial_quantities)

    final_activities = []
    for length in sl:

        # Generate activities for each stock length in 'sl'
        activities = list(stock_activities(pl, q, length, cutoff))
        final_activities.append(activities)

    # Calculate the total number of activities generated
    activities_length = sum(len(activities) for activities in final_activities)
    return final_activities


# Calculates the total cost of a given solution
def fitness(solution, sc):
    t_cost = 0
    for i in range(len(solution)):

        # Cost is calculated as the sum of activities multiplied by the stock cost
        cost = sum(solution[i]) * sc[i]
        t_cost += cost
    return t_cost


# Selects the best solutions to move to the next generation
def select_survivors(pop, fitness, n_pop):

    # Compute fitness for all solutions in the population
    costs = [fitness(c) for c in pop]

    # Sort population by fitness (lower cost is better)
    sorted_pop = sorted(zip(pop, costs), key=lambda x: x[1])

    # Retain the top 'n_pop' solutions
    best_pop = sorted_pop[:n_pop]
    new_pop, best_costs = zip(*best_pop)
    return list(new_pop)


# Selects parents for crossover using roulette selection
def parent_selection(pop, fitness, n_offspring):

    # Calculate the fitness cost for each solution
    costs = [fitness(c) for c in pop]

    # Compute probabilities proportional to fitness
    p_costs = [c / np.sum(costs) for c in costs]
    pop_indexes = np.arange(len(pop))

    # Select 'n_offspring' parents based on the probabilities
    winner_indexes = np.random.choice(pop_indexes, replace=False, size=n_offspring, p=p_costs)
    parents = [pop[i] for i in winner_indexes]

    return parents


# Performs partial crossover between two solutions
def partially_crossover(p1, p2):

    # Crossover a single stock set by swapping segments
    def stock_crossover(p1, p2):
        sol_length = len(p1)

        # Randomly select a segment to swap
        start_i, end_i = sorted(random.sample(range(sol_length), 2))
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1[start_i:end_i], c2[start_i:end_i] = p2[start_i:end_i], p1[start_i:end_i]
        return c1, c2

    # Apply the stock crossover to each stock in the solution
    child1 = []
    child2 = []
    for p1_stock, p2_stock in zip(p1, p2):
        child1_stock, child2_stock = stock_crossover(p1_stock, p2_stock)
        child1.append(child1_stock)
        child2.append(child2_stock)

    return child1, child2


# Performs bit-level crossover between two solutions
def bits_crossover(p1, p2):
    def stock_crossover(p1, p2):

        # Select a random index to swap
        i = random.randint(0, len(p1) - 1)
        c1 = copy.deepcopy(p1)
        c2 = copy.deepcopy(p2)
        c1[i], c2[i] = p2[i], p1[i]
        return c1, c2

    # Apply the stock crossover to each stock in the solution
    child1 = []
    child2 = []
    for p1_stock, p2_stock in zip(p1, p2):
        child1_stock, child2_stock = stock_crossover(p1_stock, p2_stock)
        child1.append(child1_stock)
        child2.append(child2_stock)
    return child1, child2


# Mutates a solution by introducing random changes
def mutation(solution):
    m_sol = copy.deepcopy(solution)
    for _ in range(3):  # Perform 3 mutations
        r1 = random.randint(0, len(m_sol) - 1)  # Select a random stock
        r2 = random.randint(0, len(m_sol[r1]) - 1)  # Select a random activity
        if m_sol[r1][r2] > 0:

            # Randomly decide to add or subtract
            add_sub = random.randint(0, 2)
            if add_sub > 0:
                m_sol[r1][r2] -= 1
            else:
                m_sol[r1][r2] += 1
        else:
            m_sol[r1][r2] += 1
    return m_sol

# Mutates a solution to reduce wastage by targeting inefficient activities
def wastage_mutation(solution, activities, sl):
    m_sol = copy.deepcopy(solution)
    l_activities = []  # List to store activities with wastage information
    t_wastage_power = 0  # Total wastage to compute probabilities

    # Identify activities with wastage and calculate wastage power
    for stock_i, stock_activities in enumerate(solution):
        for activity_i, count in enumerate(stock_activities):
            if count > 0:  # Only consider activities that exist in the solution
                l_activity = [stock_i, activity_i]
                corresponding_activity = activities[stock_i][activity_i]
                wastage = sl[stock_i] - sum(corresponding_activity)
                wastage_power = wastage
                t_wastage_power += wastage_power
                l_activities.append([l_activity, corresponding_activity, wastage_power])

    # Compute probabilities proportional to wastage for mutation
    p_wastage = [w[2] / t_wastage_power for w in l_activities]
    r_indexes = np.random.choice(range(len(l_activities)), size=3, replace=False, p=p_wastage)

    # Mutate by removing activities with high wastage
    for i in r_indexes:
        r_location = l_activities[i][0]
        m_sol[r_location[0]][r_location[1]] = 0

    return m_sol


# Repairs a solution to ensure it adheres to constraints
def repair_solution(solution, activities, pl, remaining_q, q):

    # Fix overuse of resources by removing excessive activities
    def repair_overuse(solution, activities, pl, q):
        remaining_q = copy.deepcopy(q)

        # Identify pieces that are overused
        pieces_overused = {pl[i]: abs(remaining_q[i]) for i in range(len(remaining_q)) if remaining_q[i] < 0}
        over_sol = copy.deepcopy(solution)
        for piece, overuse_amount in pieces_overused.items():
            while overuse_amount > 0:

                # Find activities that overuse the piece
                over_activities = [(i, j) for i in range(len(over_sol)) for j in range(len(over_sol[i]))
                                   if over_sol[i][j] > 0 and piece in activities[i][j]]
                if over_activities:
                    i, j = random.choice(over_activities)
                    contribution = activities[i][j].count(piece)
                    over_sol[i][j] -= 1
                    overuse_amount -= contribution
                    remaining_q[pl.index(piece)] += contribution
                else:
                    break
        return over_sol

    # Fix underuse by adding valid activities to meet constraints
    def repair_underuse(solution, activities, pl, remaining_q, q):
        max_trys = 20  # Maximum attempts to repair
        trys = 0
        p_activities = []

        # Identify potential activities that can be added
        for i, activity in enumerate(activities):
            for j, s_activity in enumerate(activity):
                change_q = [s_activity.count(x) for x in pl]
                if all(remaining_q[pl.index(x)] - count >= 0 for x, count in zip(pl, change_q)):
                    p_activities.append((i, j, change_q))

        # Attempt to repair underuse by adding valid activities
        while trys < max_trys:
            temp_q = np.copy(remaining_q)
            under_sol = copy.deepcopy(solution)
            valid_activities = copy.deepcopy(p_activities)

            while True:

                # Filter valid activities based on remaining quantities
                valid_activities = [(i, j, change_q) for i, j, change_q in valid_activities if
                                    all(temp_q[y] - change_q[y] >= 0 for y in range(len(pl)))]
                if not valid_activities:
                    valid, test_q = is_valid(under_sol, activities, pl, q)
                    if valid:
                        return under_sol
                    break
                r1, r2, _ = random.choice(valid_activities)
                under_sol[r1][r2] += 1
                for x in activities[r1][r2]:
                    temp_q[pl.index(x)] -= 1
                valid2, test_q2 = is_valid(under_sol, activities, pl, q)
                if valid2:
                    return under_sol
                if any(x < 0 for x in temp_q):
                    under_sol[r1][r2] -= 1
                    for x in activities[r1][r2]:
                        temp_q[pl.index(x)] += 1
                    break
            trys += 1
        return random_candidate(activities, pl, q)

    # Repair the solution to address overuse and underuse
    sol = repair_overuse(solution, activities, pl, remaining_q)
    valid, recalculated_q = is_valid(sol, activities, pl, q)
    final_sol = repair_underuse(sol, activities, pl, recalculated_q, q)

    return final_sol


# Generates a random valid solution using the given activities and constraints
def random_candidate(activities, pl, q):
    pl_indices = {piece: i for i, piece in enumerate(pl)}
    p_activities = [[i, j] for i, acts in enumerate(activities) for j in range(len(acts))]
    while True:

        # Start with an empty solution and available quantities
        solution = [[0] * len(s_activities) for s_activities in activities]
        remaining_q = q.copy()
        valid_activities = p_activities.copy()

        while True:

            # Filter valid activities based on remaining quantities
            valid_activities = [activity for activity in valid_activities if all(
                remaining_q[pl_indices[x]] - activities[activity[0]][activity[1]].count(x) >= 0 for x in
                activities[activity[0]][activity[1]])]
            if not valid_activities:
                break
            r1, r2 = random.choice(valid_activities)
            solution[r1][r2] += 1
            for x in activities[r1][r2]:
                remaining_q[pl_indices[x]] -= 1
            valid, test_q = is_valid(solution, activities, pl, q)
            if valid:
                return solution
            if any(x < 0 for x in test_q):
                solution[r1][r2] -= 1
                for x in activities[r1][r2]:
                    remaining_q[pl_indices[x]] += 1


# Checks if a solution is valid by verifying resource constraints
def is_valid(solution, activities, pl, q):
    test_q = q.copy()  # Start with available quantities
    test_pl = pl
    finish_q = [0] * len(q)

    # Adjust quantities based on the solution
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            for _ in range(solution[i][j]):
                for x in activities[i][j]:
                    test_q[test_pl.index(x)] -= 1

    # A solution is valid if all resources are used exactly as available
    if test_q == finish_q:
        return True, test_q

    return False, test_q


# Initialises a population of random valid solutions
def fill_pop(n_pop, activities, pl, q):

    # Create 'n_pop' random candidates
    pop = [random_candidate(activities, pl, q) for _ in range(n_pop)]

    return pop


# Baseline Evolutionary Algorithm
def baseline_ea(pl, q, sl, activities, fitness, n_pop, iterations, p_crossover, p_mutation):

    # Initialise the population with random valid solutions
    pop = fill_pop(n_pop, activities, pl, q)
    best_sol = None  # Variable to store the best solution found
    best_cost = float('inf')  # Initialise the best cost as infinity

    for counter in range(iterations):
        # Select parents for crossover
        n_parents = int(np.floor(len(pop) / 2))  # Half the population will be parents
        parents = parent_selection(pop, fitness, n_parents)  # Select parents using fitness-based probability
        children = []  # Initialise list to store children

        # Generate offspring through crossover
        for _ in range(n_parents):
            r_crossover = random.randint(0, 99)  # Random number to decide if crossover happens
            r1, r2 = random.sample(range(n_parents), 2)  # Randomly select two parents
            if r_crossover < p_crossover:  # Perform crossover if probability threshold is met
                child1, child2 = bits_crossover(parents[r1], parents[r2])  # Baseline crossover
                children.extend([child1, child2])
            else:
                children.extend([parents[r1], parents[r2]])  # Retain parents if no crossover

        new_pop = pop + children  # Combine existing population with new children
        mutated_pop = []  # Initialise list to store mutated individuals

        # Apply mutation to introduce variation
        for individual in new_pop:
            r_mutation = random.randint(0, 99)  # Random number to decide if mutation happens
            if r_mutation < p_mutation:  # Perform mutation if probability threshold is met
                m_sol = mutation(individual)  # Basic mutation strategy
                mutated_pop.append(m_sol)
            else:
                mutated_pop.append(individual)  # Retain individual if no mutation

        # Repair and filter invalid solutions
        valid_pop = []
        for individual in mutated_pop:
            valid, remaining_q = is_valid(individual, activities, pl, q)
            if not valid:  # Repair invalid solutions
                repaired = repair_solution(individual, activities, pl, remaining_q, q)
                valid_pop.append(repaired)
            else:
                valid_pop.append(individual)

        # Select survivors to form the next generation
        pop = select_survivors(valid_pop, fitness, n_pop)

        # Update the best solution found so far
        if fitness(pop[0]) < best_cost:
            best_cost = fitness(pop[0])
            best_sol = pop[0]

        # Log the best solution for the current iteration
        print(f"Iteration {counter + 1}: Best solution: {best_sol}, cost: {best_cost}")

    # Output the final best solution and its cost
    print(f"Baseline EA: Best solution found: {best_sol}, cost: {best_cost}")


# Custom Evolutionary Algorithm
def my_ea(pl, q, sl, activities, fitness, n_pop, iterations, p_crossover, p_mutation):

    # Initialise the population with random valid solutions
    pop = fill_pop(n_pop, activities, pl, q)
    best_sol = None  # Variable to store the best solution found
    best_cost = float('inf')  # Initialise the best cost as infinity

    for counter in range(iterations):
        # Select parents for crossover
        n_parents = int(np.floor(len(pop) / 2))  # Half the population will be parents
        parents = parent_selection(pop, fitness, n_parents)  # Select parents using fitness-based probability
        children = []  # Initialise list to store children

        # Generate offspring through crossover
        for _ in range(n_parents):
            r_crossover = random.randint(0, 99)  # Random number to decide if crossover happens
            r1, r2 = random.sample(range(n_parents), 2)  # Randomly select two parents
            if r_crossover < p_crossover:  # Perform crossover if probability threshold is met
                child1, child2 = partially_crossover(parents[r1], parents[r2])  # Advanced crossover
                children.extend([child1, child2])
            else:
                children.extend([parents[r1], parents[r2]])  # Retain parents if no crossover

        new_pop = pop + children  # Combine existing population with new children
        mutated_pop = []  # Initialise list to store mutated individuals

        # Apply mutation to introduce variation
        for individual in new_pop:
            r_mutation = random.randint(0, 99)  # Random number to decide if mutation happens
            if r_mutation < p_mutation:  # Perform mutation if probability threshold is met
                m_sol = wastage_mutation(individual, activities, sl)  # Advanced mutation strategy
                mutated_pop.append(m_sol)
            else:
                mutated_pop.append(individual)  # Retain individual if no mutation

        # Repair and filter invalid solutions
        valid_pop = []
        for individual in mutated_pop:
            valid, remaining_q = is_valid(individual, activities, pl, q)
            if not valid:  # Repair invalid solutions
                repaired = repair_solution(individual, activities, pl, remaining_q, q)
                valid_pop.append(repaired)
            else:
                valid_pop.append(individual)

        # Select survivors to form the next generation
        pop = select_survivors(valid_pop, fitness, n_pop)

        # Update the best solution found so far
        if fitness(pop[0]) < best_cost:
            best_cost = fitness(pop[0])
            best_sol = pop[0]

        # Log the best solution for the current iteration
        print(f"Iteration {counter + 1}: Best solution: {best_sol}, cost: {best_cost}")

    # Output the final best solution and its cost
    print(f"My EA: Best solution found: {best_sol}, cost: {best_cost}")