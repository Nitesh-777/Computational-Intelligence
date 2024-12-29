import es_algs

# Practice test case 1
# stock_lengths = [40, 50]
# stock_costs = [100, 120]
# piece_lengths = [10, 15, 20, 30]
# quantities = [2, 2, 3, 4]

# Practice test case 2
# stock_lengths3 = [10, 13, 15]
# stock_costs3 = [100, 130, 150]
# piece_lengths3 = [3, 4, 5, 6, 7, 8, 9, 10]
# quantities3 = [5, 2, 1, 2, 4, 2, 1, 3]

# Practice test case 3
# stock_lengths4 = [4300, 4250, 4150, 3950, 3800, 3700, 3550, 3500]
# stock_costs4 = [86, 85, 83, 79, 68, 66, 64, 63]
# piece_lengths4 = [2350, 2250, 2200, 2100, 2050, 2000, 1950, 1900, 1850, 1700, 1650, 1350, 1300, 1250, 1200, 1150, 1100, 1050]
# quantities4 = [2, 4, 4, 15, 6, 11, 6, 15, 13, 5, 2, 9, 3, 6, 10, 4, 8, 3]

# Official Test Case
stock_lengths = [120, 115, 110, 105, 100]
stock_costs = [12, 11.5, 11, 10.5, 10]
piece_lengths = [21, 22, 24, 25, 27, 29, 30, 31, 32, 33, 34, 35, 38, 39, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 59, 60, 61, 63, 65, 66, 67]
quantities = [13, 15, 7, 5, 9, 9, 3, 15, 18, 17, 4, 17, 20, 9, 4, 19, 4, 12, 15, 3, 20, 14, 15, 6, 4, 7, 5, 19, 19, 6, 3, 7, 20, 5, 10, 17]



activities = es_algs.group_based_rep(stock_lengths, piece_lengths, quantities, 37)


# fitness method using given stock costs
def fitness(solution):
    return es_algs.fitness(solution, stock_costs)

# Algorithms run using official test case
es_algs.baseline_ea(piece_lengths, quantities, stock_lengths, activities, fitness, 50, 50, 20, 60)
es_algs.my_ea(piece_lengths, quantities, stock_lengths, activities, fitness, 50, 50, 20, 60)
