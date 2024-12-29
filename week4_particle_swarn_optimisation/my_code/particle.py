import random

import pso
import numpy as np


class Particle:
    globalBest = None
    totalParticles = 0
    totalIter = None
    currentIter = None

    def __init__(self, aa):
        self.antenna_array = aa
        self.position = pso.r_candidate(self.antenna_array)
        self.cost = self.antenna_array.evaluate(self.position)
        self.personal_best_pos = self.position
        self.personal_best_cost = self.cost
        random_particle = pso.r_candidate(self.antenna_array)
        self.velocity = [random_particle[i] / 2 for i in range(len(random_particle) - 1)]
        self.inertial = 0.721
        self.cognitive = 1.1193
        self.social = 1.1193
        Particle.totalParticles += 1
        Particle.globalBest = self.personal_best_pos

    def updateVelocity(self):
        # print(f"####### POSITION{self.position} TYPE: {type(self.position)}")
        # print(f"####### VELOCITY{self.velocity} TYPE: {type(self.velocity)}")
        # new_position = [self.position[i] + self.velocity[i] for i in range(len(self.velocity))]
        # new_position.sort()
        # new_position.append(self.antenna_array.n_antennae / 2)
        # # print(new_position)
        # # if self.antenna_array.is_valid(new_position):
        # self.position = new_position
            # print("NORMAl VALID")

        # else:
        #     if new_position[1] < 0 and new_position[0] < 0:
        #         print(new_position)
        #     # print(f"INVALID POSITION{new_position}")
        #     if new_position[-2] > (self.antenna_array.n_antennae / 2) - self.antenna_array.MIN_SPACING:
        #         overshoot = new_position[-2] - ((self.antenna_array.n_antennae / 2) - self.antenna_array.MIN_SPACING)
        #         # print(f"OVERSHOOT {overshoot}")
        #         new_position[-2] = ((self.antenna_array.n_antennae / 2) - self.antenna_array.MIN_SPACING) - overshoot
        #     elif new_position[-2] < 0:
        #         new_position[-2] *= -1
        #     # print(f"INVALID POSITION AFTER FIXING POS[-2]{new_position}")
        #     counter = 0
        #     print(new_position)
        #     while not self.antenna_array.is_valid(new_position):
        #         # print(new_position)
        #         for i in range(len(new_position) - 3, -1, -1):
        #             if i == 0 and new_position[i] < 0:
        #                 new_position[i] *= -1
        #             elif new_position[i] < 0:
        #                 new_position[i] *= -1
        #             elif new_position[i] > new_position[i+1] - self.antenna_array.MIN_SPACING:
        #                 overshoot = new_position[i] - (new_position[i+1] - self.antenna_array.MIN_SPACING)
        #                 new_position[i] = (new_position[i+1] - self.antenna_array.MIN_SPACING) - overshoot
        #             elif new_position[i] < new_position[i-1] + self.antenna_array.MIN_SPACING:
        #                 overshoot = (new_position[i-1] + self.antenna_array.MIN_SPACING) - new_position[i]
        #                 new_position[i] = (new_position[i-1] + self.antenna_array.MIN_SPACING) + overshoot
        #             new_position.sort()
        #         # new_position.append(self.antenna_array.n_antennae / 2)
        #         print(f"INFINITE LOOP {new_position}")
        #         counter += 1
        #         if counter > 15:
        #             print("UNSUCCESSFUL INFINITE LOOP")
        #             break
        #
        #     # for i in range(len(new_position) - 3, 0, -1):
        #     #     if new_position[i] > new_position[i+1] - self.antenna_array.MIN_SPACING:
        #     #         overshoot = new_position[i] - (new_position[i+1] - self.antenna_array.MIN_SPACING)
        #     #         new_position[i] = (new_position[i+1] - self.antenna_array.MIN_SPACING) - overshoot
        #     #     if i > 0 and new_position[i] < new_position[i-1] + self.antenna_array.MIN_SPACING:
        #     #         overshoot = (new_position[i-1] + self.antenna_array.MIN_SPACING) - new_position[i]
        #     #         new_position[i] = new_position[i-1] + self.antenna_array.MIN_SPACING + overshoot
        #     if self.antenna_array.is_valid(new_position):
        #         # new_position.append(self.antenna_array.n_antennae / 2)
        #         new_position.sort()
        #         self.position = new_position
        #         print(f"OVERSHOOT CORRECTION VALID $$$$$$$$$$$ {new_position}")
        #     else:
        #         print(f"OVERSHOOT CORRECTION INVALID !!!!!!!!! {new_position}")
        inertia_max = 0.9
        inertia_min = 0.4
        iter_ratio = Particle.currentIter / Particle.totalIter
        self.inertial = inertia_max - ((inertia_max - inertia_min) * iter_ratio)

        r1 = np.random.sample()
        r2 = np.random.sample()

        self.cognitive = 2.15
        self.social = 2.15
        x = self.cognitive + self.social
        k = 2 / abs(2 - x - (x**2 - 4*x)**0.5)

        # self.velocity = [(self.inertial * self.velocity[i]) +
        #                  (self.cognitive * r1 * (self.personal_best_pos[i] - self.position[i])) +
        #                  (self.social * r2 * (Particle.globalBest[i] - self.position[i])) for i in
        #                  range(len(self.velocity))]
        v_max = 0.5
        for i in range(len(self.velocity)):
            # new_position.sort()
            cognitive_velocity = self.cognitive * r1 * (self.personal_best_pos[i] - self.position[i])
            social_velocity = self.social * r2 * (Particle.globalBest[i] - self.position[i])
            self.velocity[i] = k * ((self.inertial * self.velocity[i]) + cognitive_velocity + social_velocity)
            self.velocity[i] = max(min(self.velocity[i], v_max), -v_max)

        # print(f"####### VELOCITY{self.velocity} TYPE: {type(self.velocity)}")

    def updatePosition(self):
        new_position = [self.position[i] + self.velocity[i] for i in range(len(self.velocity))]
        new_position.sort()
        new_position.append(self.antenna_array.n_antennae / 2)
        self.position = new_position

    def updatePB(self):
        self.cost = self.antenna_array.evaluate(self.position)
        if self.cost < self.personal_best_cost:
            self.personal_best_pos = self.position
            self.personal_best_cost = self.cost

    def updateGB(self):
        if self.personal_best_cost < self.antenna_array.evaluate(Particle.globalBest):
            Particle.globalBest = self.personal_best_pos

    def __str__(self):
        return f"Current Postion: {self.position}, Cost: {self.cost}\n" \
               f"Personal Best Position: {self.personal_best_pos}, Cost: {self.personal_best_cost}\n" \
               f"Global Best Position: {Particle.globalBest}, Cost: {self.antenna_array.evaluate(Particle.globalBest)}"

    def __repr__(self):
        return f"\n\nCurrent Postion: {self.position}, Cost: {self.cost}\n" \
               f"Personal Best Position: {self.personal_best_pos}, Cost: {self.personal_best_cost}\n" \
               f"Global Best Position: {Particle.globalBest} , Cost: {self.antenna_array.evaluate(Particle.globalBest)}"
