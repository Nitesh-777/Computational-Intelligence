from week4_particle_swarn_optimisation.my_code.antenna_array.antennaarray import AntennaArray
import random
import time
from particle import Particle

N_ANTENNAE = 4
STEERING_ANGLE = 35
MIN_SPACING = 0.25

antenna_array = AntennaArray(N_ANTENNAE, STEERING_ANGLE)


# print(antenna_array.evaluate([0.5, 1.2, 1.5]))


def r_candidate(aa):
    while True:
        des = []
        for _ in range(N_ANTENNAE - 1):
            r = random.uniform(0, (N_ANTENNAE / 2) - MIN_SPACING)
            des.append(r)
        des.sort()
        des.append(N_ANTENNAE / 2)
        # print(des)
        # if aa.is_valid(des):
        #     return des
        if aa.is_valid(des):
            # print("######## VALID ############")
            # return True
            # print(aa.evaluate(des))
            return des
        # else:
        # print("######## INVALID ########")
        #     return False

    # des = []
    # r = random.uniform(0, aa.n_antennae / 2 - MIN_SPACING)
    # des.append(r)
    # for _ in range(N_ANTENNAE - 2):
    #     spaces = []
    #     for i in range(len(des) - 1):
    #         if des[i + 1] - des[i] >= MIN_SPACING:
    #             spaces.append([des[i] + MIN_SPACING, des[i + 1] - MIN_SPACING])
    #     if des[0] > MIN_SPACING:
    #         spaces.insert(0, [0, des[0] - MIN_SPACING])
    #     if des[-1] + MIN_SPACING < aa.n_antennae / 2 - MIN_SPACING:
    #         spaces.append([des[-1] + MIN_SPACING, aa.n_antennae / 2 - MIN_SPACING])
    #     # print(f"SPACES:  {spaces}")
    #     r_space = random.choice(spaces)
    #     r = random.uniform(*r_space)
    #     des.append(r)
    #     des.sort()
    # des.append(aa.n_antennae / 2)

    # print(f"DESIGN:   {des}")
    # if aa.is_valid(des):
    #     print("######## VALID ############")
    #     # return True
    #     # print(aa.evaluate(des))
    # else:
    #     print("######## INVALID ########")
    # #     return False
    # return des


# x = 0
# for _ in range(100):
#     if r_candidate(antenna_array):
#         x += 1
#         print(x)


def random_search(aa, t):
    end_time = time.time() + t
    best_design = r_candidate(aa)
    best_peak = aa.evaluate(best_design)
    while time.time() < end_time:
        d = r_candidate(aa)
        d_peak = aa.evaluate(d)
        if d_peak < best_peak:
            best_design = d
            best_peak = aa.evaluate(d)
            print(f"Best design so far: {best_design}, Peak: {best_peak}")
    print(f"Best Design Found at end: {best_design}, Peak: {best_peak}")


# random_search(antenna_array, 30)

def pso(aa, swarm_size, itr):
    swarm = [Particle(aa) for _ in range(swarm_size)]
    Particle.totalIter = itr
    Particle.currentIter = 0
    for _ in range(itr):
        for particle in swarm:
            particle.updatePosition()
            particle.updateVelocity()
            if aa.is_valid(particle.position):
                # print(Particle.globalBest)
                particle.updateGB()
                particle.updatePB()
        Particle.currentIter += 1

        print(
            f"Iteration: {Particle.currentIter}/{Particle.totalIter} Current Global Best: {Particle.globalBest}, Cost: {aa.evaluate(Particle.globalBest)}")
    print(f"Final Global Best: {Particle.globalBest}, Cost: {aa.evaluate(Particle.globalBest)}")
