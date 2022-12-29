import random
from abc import ABC, abstractmethod

from PyQt5.QtGui import QPixmap
from numpy import argmax

import interface
from neural_network import NeuralNetwork

cells = []
preys = []
predators = []
food_units = []
initial_energy = 0
mutation_rate = 0
likelihood_reproduction = 0
food_energy = 0
reproduction_energy = 0
max_preys = 0


class Item(ABC):
    def __init__(self, x, y):
        self.image = None
        self.x = x
        self.y = y
        self.set_orientation("up")
        self.active = True

    def get_coordinates(self):
        return self.x, self.y

    def set_coordinates(self, x, y):
        self.x, self.y = x, y

    @abstractmethod
    def set_orientation(self, orientation):
        pass

    def move(self, x, y):
        if x < 0:
            x = 9
        if x > 9:
            x = 0
        if y < 0:
            y = 14
        if y > 14:
            y = 0

        if not cells[x][y].get_occupant():
            print(f"self = {type(self)}, cells[x][y] = {type(cells[x][y].get_occupant())}")
            cells[self.x][self.y].setPixmap(QPixmap("images/void.png"))
            cells[self.x][self.y].set_occupant(None)
            self.set_coordinates(x, y)
            self.lose_mov_energy()
        else:
            if isinstance(self, Prey) and isinstance(cells[x][y].get_occupant(), Prey):
                print(f"self = {type(self)}, cells[x][y] = {type(cells[x][y].get_occupant())}")
                # Preys mate with probability 50%
                if self.gender != cells[x][y].get_occupant().gender and random.randint(0, 100) < 50:
                    self.mate(cells[x][y].get_occupant())

            # Prey eats food
            elif isinstance(self, Prey) and isinstance(cells[x][y].get_occupant(), Food):
                print(f"self = {type(self)}, cells[x][y] = {type(cells[x][y].get_occupant())}")
                self.lose_mov_energy()
                self.eat_food(cells[x][y].get_occupant())
                cells[x][y].set_occupant(None)
                cells[self.x][self.y].set_occupant(self)
                self.set_coordinates(x, y)

            # Prey is eaten by Predator
            elif isinstance(self, Prey) and isinstance(cells[x][y].get_occupant(), Predator):
                print(f"self = {type(self)}, cells[x][y] = {type(cells[x][y].get_occupant())}")
                cells[self.x][self.y].set_occupant(None)
                cells[x][y].get_occupant().eat_prey(self)

            # Predator eats food
            elif isinstance(self, Predator) and isinstance(cells[x][y].get_occupant(), Food):
                print(f"self = {type(self)}, cells[x][y] = {type(cells[x][y].get_occupant())}")
                self.eat_food(cells[x][y].get_occupant())
                cells[x][y].set_occupant(None)
                cells[self.x][self.y].set_occupant(None)
                self.set_coordinates(x, y)
                cells[self.x][self.y].set_occupant(None)
                self.lose_mov_energy()

            # Predator finds predator
            elif isinstance(self, Predator) and isinstance(cells[x][y].get_occupant(), Predator):
                print(f"self = {type(self)}, cells[x][y] = {type(cells[x][y].get_occupant())}")
                self.stop()

            elif isinstance(self, Predator) and isinstance(cells[x][y].get_occupant(), Prey):
                print(f"self = {type(self)}, cells[x][y] = {type(cells[x][y].get_occupant())}")
                self.lose_mov_energy()
                cells[self.x][self.y].set_occupant(None)
                self.set_coordinates(x, y)
                cells[self.x][self.y].set_occupant(self)
                self.eat_prey(cells[x][y].get_occupant())
        if self.energy <= 0:
            cells[self.x][self.y].set_occupant(None)
            if isinstance(self, Prey):
                preys.remove(self)
            elif isinstance(self, Predator):
                predators.remove(self)

    def set_image(self, image):
        self.image = QPixmap(image)
        cells[self.x][self.y].set_occupant(self)

    def get_image(self):
        return self.image


class Food(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        food_units.append(self)
        self.energy = food_energy

    def set_orientation(self, orientation):
        self.set_image("images/Food.png")

    def get_energy(self):
        return self.energy


class Being(Item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.energy = initial_energy
        self.neighbours = []
        self.vision = []
        self.neural_network = NeuralNetwork()
        self.gender = random.choice(['m', 'f'])
        self.move_cost = 5
        self.outputs = None
        self.best_move = None
        self.random_move = None

    @abstractmethod
    def set_orientation(self, orientation):
        pass

    def lose_mov_energy(self):
        self.energy -= self.move_cost

    def eat_food(self, food):
        self.energy += food.get_energy()

    def make_best_move(self):
        self.see()
        self.outputs = self.neural_network.learn(self.vision)
        self.best_move = argmax(self.outputs)

        if self.best_move == 0:
            self.move_left()
        elif self.best_move == 1:
            self.move_forward_left()
        elif self.best_move == 2:
            self.move_forward()
        elif self.best_move == 3:
            self.move_forward_right()
        elif self.best_move == 4:
            self.move_right()
        elif self.best_move == 5:
            self.move_back()
        elif self.best_move == 6:
            self.rotate()
        else:
            self.stop()

    def make_random_move(self):
        self.random_move = random.randint(0, 7)
        if self.random_move == 0:
            self.move_left()
        elif self.random_move == 1:
            self.move_forward_left()
        elif self.random_move == 2:
            self.move_forward()
        elif self.random_move == 3:
            self.move_forward_right()
        elif self.random_move == 4:
            self.move_right()
        elif self.random_move == 5:
            self.move_back()
        elif self.random_move == 6:
            self.rotate()
        else:
            self.stop()

    def see(self):
        self.vision.clear()
        if self.orientation == "down":
            neighbours = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        elif self.orientation == "up":
            neighbours = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        elif self.orientation == "right":
            neighbours = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]
        else:
            neighbours = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]

        for x, y in neighbours:
            x, y = self.x + x, self.y + y
            if x < 0:
                x = 9

            if x > 9:
                x = 0

            if y < 0:
                y = 14

            if y > 14:
                y = 0

            type_ = cells[x][y].get_occupant_type_code()

            self.vision.append(type_)

    def move_left(self):
        if self.orientation == "down":
            self.move(self.x, self.y + 1)
            self.set_orientation("right")
        elif self.orientation == "up":
            self.move(self.x, self.y - 1)
            self.set_orientation("left")
        elif self.orientation == "right":
            self.move(self.x - 1, self.y)
            self.set_orientation("up")
        else:
            self.move(self.x + 1, self.y)
            self.set_orientation("down")

    def move_right(self):
        if self.orientation == "down":
            self.move(self.x, self.y - 1)
            self.set_orientation("left")
        elif self.orientation == "up":
            self.move(self.x, self.y + 1)
            self.set_orientation("right")
        elif self.orientation == "right":
            self.move(self.x + 1, self.y)
            self.set_orientation("down")
        else:
            self.move(self.x - 1, self.y)
            self.set_orientation("up")

    def move_forward(self):
        if self.orientation == "down":
            self.move(self.x + 1, self.y)
            self.set_orientation("down")
        elif self.orientation == "up":
            self.move(self.x - 1, self.y)
            self.set_orientation("up")
        elif self.orientation == "right":
            self.move(self.x, self.y + 1)
            self.set_orientation("right")
        else:
            self.move(self.x, self.y - 1)
            self.set_orientation("left")

    def move_back(self):
        if self.orientation == "down":
            self.move(self.x - 1, self.y)
            self.set_orientation("up")
        elif self.orientation == "up":
            self.move(self.x + 1, self.y)
            self.set_orientation("back")
        elif self.orientation == "right":
            self.move(self.x, self.y - 1)
            self.set_orientation("left")
        else:
            self.move(self.x, self.y + 1)
            self.set_orientation("right")

    def move_forward_left(self):
        self.move_left()
        self.move_right()

    def move_forward_right(self):
        self.move_left()
        self.move_right()

    def stop(self):
        pass

    def rotate(self):
        if self.orientation == "down":
            self.set_orientation("up")
        elif self.orientation == "up":
            self.set_orientation("down")
        elif self.orientation == "right":
            self.set_orientation("left")
        else:
            self.set_orientation("right")


class Prey(Being):
    def __init__(self, x, y):
        super().__init__(x, y)
        preys.append(self)
        self.dna = [self.gender, self.neural_network.synaptic_weights]

    def set_orientation(self, orientation):
        self.orientation = orientation
        if orientation == "down":
            self.set_image("images/prey_down.png")
        elif orientation == "up":
            self.set_image("images/prey_up.png")
        elif orientation == "right":
            self.set_image("images/prey_right.png")
        else:
            self.set_image("images/prey_left.png")

    def mate(self, prey):
        self.energy -= reproduction_energy
        prey.energy -= reproduction_energy

        # Prey reproduce with probability equal to likelihood_reproduction
        if random.randint(0, 100) < likelihood_reproduction:
            while True:
                x, y = random.randint(0, 9), random.randint(0, 14)
                if not cells[x][y].get_occupant():
                    a = Prey(x, y)
                    interface.child_preys += 1
                    break


class Predator(Being):
    def __init__(self, x, y):
        super().__init__(x, y)
        predators.append(self)

    def set_orientation(self, orientation):
        self.orientation = orientation

        if orientation == "down":
            self.set_image("images/predator_down.png")
        elif orientation == "up":
            self.set_image("images/predator_up.png")
        elif orientation == "right":
            self.set_image("images/predator_right.png")
        else:
            self.set_image("images/predator_left.png")

    def eat_prey(self, prey):
        self.energy += 15
        cells[prey.x][prey.y].set_occupant(None)
        preys.remove(prey)
