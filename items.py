import random
from abc import ABC, abstractmethod

from PyQt5.QtGui import QPixmap
from numpy import argmax

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
        self.coordinates = (x, y)
        self.cell = cells[x][y]
        self.set_orientation("up")

    def get_coordinates(self):
        return self.coordinates

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
            self.cell.setPixmap(QPixmap("images/void.png"))
            self.cell.set_occupant(None)
            self.coordinates = (x, y)
            self.cell = cells[x][y]
        else:
            if isinstance(self, Prey) and isinstance(cells[x][y].get_occupant(), Prey):
                self.stop()

            if isinstance(self, Prey) and isinstance(cells[x][y].get_occupant(), Food):
                self.lose_mov_energy()
                self.eat_food(cells[x][y].get_occupant())
                cells[x][y].set_occupant(None)
                self.cell.setPixmap(QPixmap("images/void.png"))
                self.cell.set_occupant(None)
                self.coordinates = (x, y)
                self.cell = cells[x][y]

            if isinstance(self, Prey) and isinstance(cells[x][y].get_occupant(), Predator):
                cells[x][y].eat_prey(self)
                self.cell.setPixmap(QPixmap("images/void.png"))
                self.cell.set_occupant(None)
                self.die()

            if isinstance(self, Predator) and isinstance(cells[x][y].get_occupant(), Food):
                self.eat_food(cells[x][y].get_occupant())
                cells[x][y].set_occupant(None)
                self.cell.setPixmap(QPixmap("images/void.png"))
                self.cell.set_occupant(None)
                self.coordinates = (x, y)
                self.cell = cells[x][y]
                self.lose_mov_energy()

            if isinstance(self, Predator) and isinstance(cells[x][y].get_occupant(), Predator):
                self.stop()

            if isinstance(self, Predator) and isinstance(cells[x][y].get_occupant(), Prey):
                self.eat_prey(cells[x][y].get_occupant())
                self.cell.setPixmap(QPixmap("images/void.png"))
                self.cell.set_occupant(None)
                self.coordinates = (x, y)
                self.cell = cells[x][y]
                self.lose_mov_energy()

    def set_image(self, image):
        self.image = QPixmap(image)
        self.cell.set_occupant(self)

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
        self.vision = []
        self.neural_network = NeuralNetwork()
        self.gender = random.choice(['m', 'f'])
        self.move_cost = 10
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
        self.random_move = random.randint(0, 9)

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
            x, y = self.coordinates[0] + x, self.coordinates[1] + y

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
            self.move(self.coordinates[0], self.coordinates[1] + 1)
            self.set_orientation("right")
        elif self.orientation == "up":
            self.move(self.coordinates[0], self.coordinates[1] - 1)
            self.set_orientation("left")
        elif self.orientation == "right":
            self.move(self.coordinates[0] - 1, self.coordinates[1])
            self.set_orientation("up")
        else:
            self.move(self.coordinates[0] + 1, self.coordinates[1])
            self.set_orientation("down")

    def move_right(self):
        if self.orientation == "down":
            self.move(self.coordinates[0], self.coordinates[1] - 1)
            self.set_orientation("left")
        elif self.orientation == "up":
            self.move(self.coordinates[0], self.coordinates[1] + 1)
            self.set_orientation("right")
        elif self.orientation == "right":
            self.move(self.coordinates[0] + 1, self.coordinates[1])
            self.set_orientation("down")
        else:
            self.move(self.coordinates[0] - 1, self.coordinates[1])
            self.set_orientation("up")

    def move_forward(self):
        if self.orientation == "down":
            self.move(self.coordinates[0] + 1, self.coordinates[1])
            self.set_orientation("down")
        elif self.orientation == "up":
            self.move(self.coordinates[0] - 1, self.coordinates[1])
            self.set_orientation("up")
        elif self.orientation == "right":
            self.move(self.coordinates[0], self.coordinates[1] + 1)
            self.set_orientation("right")
        else:
            self.move(self.coordinates[0], self.coordinates[1] - 1)
            self.set_orientation("left")

    def move_back(self):
        if self.orientation == "down":
            self.move(self.coordinates[0] - 1, self.coordinates[1])
            self.set_orientation("up")
        elif self.orientation == "up":
            self.move(self.coordinates[0] + 1, self.coordinates[1])
            self.set_orientation("back")
        elif self.orientation == "right":
            self.move(self.coordinates[0], self.coordinates[1] - 1)
            self.set_orientation("left")
        else:
            self.move(self.coordinates[0], self.coordinates[1] + 1)
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

    def die(self):
        pass


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

    def eat_prey(self):
        pass
