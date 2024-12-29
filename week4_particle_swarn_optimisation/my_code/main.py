from pso import pso , r_candidate
from week4_particle_swarn_optimisation.my_code.antenna_array.antennaarray import AntennaArray
from week4_particle_swarn_optimisation.my_code.particle import Particle

aa = AntennaArray(4, 35)

# r = r_candidate(aa)
# random_search(aa, 10)


# def fill_swarm(n_particles):
#     swarm = []
#     for _ in range(n_particles):
#         particle = Particle(aa)
#         swarm.append(particle)
#     return swarm


# swarm_pop = fill_swarm(10)
# print(swarm_pop)
#
# swarm2 = [Particle(aa) for _ in range(10)]
# print(swarm2)

pso(aa, 20, 25)

# p1 = Particle(aa)
# p2 = Particle(aa)
# print(p1)
# print(p2)
# p2.updateGB()
# print(p1)

# pop = []
# i = 0
# for _ in range(25):
#     r = r_candidate(aa)
#     if aa.is_valid(r):
#         pop.append(r)
#         i += 1
#         print(i)
#         print(r)
# print(i)