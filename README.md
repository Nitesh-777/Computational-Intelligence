# Computational Intelligence 

This repository contains the work developed for the Computational Intelligence (CS3CI) module. It includes six weekly labs focused on applying search algorithms and developing novel computational intelligence methods to solve various problems. Additionally, it contains an experimental study where two computational algorithms were created, tested, and analysed to solve the Cutting Stock Problem (CSP).

## Labs

Labs provided hands-on experience with foundational and advanced computational intelligence techniques. The labs involved working on problems such as the Travelling Salesman Problem (TSP) and the 3-Antenna Array Problem. Below is a summary of each lab:


### Week 1: Random Search
- Implemented a **Random Search** algorithm.
  - Applied to the **Travelling Salesman Problem (TSP)**.
  - Evaluated the effectiveness of random search for finding approximate solutions.

### Week 2: Local Search
- Developed a **Local Search** algorithm using a greedy approach.
  - Applied to optimise TSP routes.
  - Compared performance to the random search method.

### Week 3: Evolutionary Algorithm
- Introduced and implemented an **Evolutionary Algorithm (EA)**.
  - Applied the EA to solve the **Travelling Salesman Problem (TSP)**.
  - Key components:
    - **Selection:** Choosing the best candidates based on fitness.
    - **Crossover:** Combining parts of parent solutions to create offspring.
    - **Mutation:** Randomly altering solutions to explore new possibilities.
  - Evaluated the algorithm's ability to iteratively improve solutions.

### Week 4: Particle Swarm Optimisation
- Designed a **Particle Swarm Optimisation (PSO)** algorithm.
  - Optimised the **3-Antenna Array Problem**.
  - Explored parameter tuning for swarm size and inertia.

### Week 6: Genetic Programming
- Experimented with **Genetic Programming (GP)** using the `gplearn` API.
  - Created and evolved symbolic programs.
  - Assessed program performance on a custom-defined problem.

## Experimental Study
 
The experimental study focuses on the Cutting Stock Problem (CSP). Two computational algorithms were implemented and compared for this study:

1. Base Algorithm:
    - A straightforward algorithm using a random bits crossover and simple random mutation.
    - Focused on feasibility and simplicity in solving the CSP.

2. Custom Algorithm:
    - A more sophisticated and optimised approach.
    - Introduced partial crossover and wastage-based mutation to minimise material wastage and improve cost efficiency.

The primary goal of the was to evaluate the cost-effectiveness of the algorithms in solving the cutting stock problem. 