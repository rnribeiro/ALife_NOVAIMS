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
log = "Events log"


# Item defines any object in a grid cell (food, prey or predator)
class Item(ABC):
    def __init__(self, x, y):
        self.energy = None
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
        self.orientation = "up"
        self.energy = initial_energy
        self.neighbours = []
        self.vision = []
        self.neural_network = NeuralNetwork()
        self.move_cost = 3
        self.outputs = None
        self.best_move = None
        self.random_move = None

    @abstractmethod
    def set_orientation(self, orientation):
        pass

    @abstractmethod
    def make_move(self):
        pass

    def update(self, x, y):
        global log
        # Handle indexes outside the grid
        if x < 0:
            x = 9
        if x > 9:
            x = 0
        if y < 0:
            y = 14
        if y > 14:
            y = 0

        if not cells[x][y].get_occupant():
            cells[self.x][self.y].set_occupant(None)
            cells[self.x][self.y].setPixmap(QPixmap("images/void.png"))
            self.set_coordinates(x, y)
            cells[self.x][self.y].set_occupant(self)
            self.lose_move_energy()
            log = f"{self.__class__.__name__} moved\n" + log
        else:
            # Prey finds another prey
            if isinstance(self, Prey) and cells[x][y].get_occupant() in preys:
                self.mate(cells[x][y].get_occupant())

            # Prey finds food
            elif isinstance(self, Prey) and cells[x][y].get_occupant() in food_units:
                self.lose_move_energy()
                self.eat_food(cells[x][y].get_occupant())
                cells[self.x][self.y].set_occupant(None)
                cells[self.x][self.y].setPixmap(QPixmap("images/void.png"))
                self.set_coordinates(x, y)
                cells[self.x][self.y].set_occupant(self)
                log = "Prey ate food\n" + log

            # Prey finds a Predator
            elif isinstance(self, Prey) and cells[x][y].get_occupant() in predators:
                self.stop()

            # Predator eats food
            elif isinstance(self, Predator) and cells[x][y].get_occupant() in food_units:
                self.lose_move_energy()
                self.eat_food(cells[x][y].get_occupant())
                cells[self.x][self.y].set_occupant(None)
                cells[self.x][self.y].setPixmap(QPixmap("images/void.png"))
                self.set_coordinates(x, y)
                cells[self.x][self.y].set_occupant(self)
                log = "Predator ate food\n" + log

            # Predator finds predator
            elif isinstance(self, Predator) and (cells[x][y].get_occupant() in predators):
                self.stop()

            # Predator finds a prey
            elif isinstance(self, Predator) and (cells[x][y].get_occupant() in preys):
                self.lose_move_energy()
                if self.energy <= 85:
                    self.energy += 10
                else:
                    self.energy = 100
                preys.remove(cells[x][y].get_occupant())
                cells[self.x][self.y].set_occupant(None)
                cells[self.x][self.y].setPixmap(QPixmap("images/void.png"))
                self.set_coordinates(x, y)
                cells[self.x][self.y].set_occupant(self)
                log = "Predator ate Prey\n" + log

    def lose_move_energy(self):
        self.energy -= self.move_cost

    def eat_food(self, food):
        self.energy += food.get_energy()
        del food_units[-1]

    # Get indexes of neighbours according to the orientation
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
            # Add occupant type to the input layer
            self.vision.append(type_)

    def move_left(self):
        if self.orientation == "down":
            self.update(self.x, self.y + 1)
            self.set_orientation("right")
        elif self.orientation == "up":
            self.update(self.x, self.y - 1)
            self.set_orientation("left")
        elif self.orientation == "right":
            self.update(self.x - 1, self.y)
            self.set_orientation("up")
        else:
            self.update(self.x + 1, self.y)
            self.set_orientation("down")

    def move_right(self):
        if self.orientation == "down":
            self.update(self.x, self.y - 1)
            self.set_orientation("left")
        elif self.orientation == "up":
            self.update(self.x, self.y + 1)
            self.set_orientation("right")
        elif self.orientation == "right":
            self.update(self.x + 1, self.y)
            self.set_orientation("down")
        else:
            self.update(self.x - 1, self.y)
            self.set_orientation("up")

    def move_forward(self):
        if self.orientation == "down":
            self.update(self.x + 1, self.y)
            self.set_orientation("down")
        elif self.orientation == "up":
            self.update(self.x - 1, self.y)
            self.set_orientation("up")
        elif self.orientation == "right":
            self.update(self.x, self.y + 1)
            self.set_orientation("right")
        else:
            self.update(self.x, self.y - 1)
            self.set_orientation("left")

    def move_back(self):
        if self.orientation == "down":
            self.update(self.x - 1, self.y)
            self.set_orientation("up")
        elif self.orientation == "up":
            self.update(self.x + 1, self.y)
            self.set_orientation("back")
        elif self.orientation == "right":
            self.update(self.x, self.y - 1)
            self.set_orientation("left")
        else:
            self.update(self.x, self.y + 1)
            self.set_orientation("right")

    def move_forward_left(self):
        if self.orientation == "down":
            self.update(self.x + 1, self.y+1)
            self.set_orientation("down")
        elif self.orientation == "up":
            self.update(self.x -1, self.y-1)
            self.set_orientation("up")
        elif self.orientation == "left":
            self.update(self.x-1, self.y + 1)
            self.set_orientation("left")
        else:
            self.update(self.x+1, self.y - 1)
            self.set_orientation("right")


    def move_forward_right(self):
        if self.orientation == "down":
            self.update(self.x - 1, self.y + 1)
            self.set_orientation("down")
        elif self.orientation == "up":
            self.update(self.x + 1, self.y - 1)
            self.set_orientation("up")
        elif self.orientation == "left":
            self.update(self.x - 1, self.y - 1)
            self.set_orientation("left")
        else:
            self.update(self.x + 1, self.y + 1)
            self.set_orientation("right")

    def stop(self):
        if self.orientation == "down":
            self.set_orientation("down")
        elif self.orientation == "up":
            self.set_orientation("up")
        elif self.orientation == "right":
            self.set_orientation("right")
        else:
            self.set_orientation("left")

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
        self.set_orientation("up")
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

    def make_move(self):
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

    def mate(self, prey):
        self.energy -= reproduction_energy
        prey.energy -= reproduction_energy

        # Preys reproduce with probability equal to likelihood_reproduction
        if random.randint(0, 100) < likelihood_reproduction:
            reproduce(self, prey)
            global log
            log = f"Two preys reproduced\n" + log


# Create a new prey in a random place
def reproduce(prey1, prey2):
    while True and max_preys >= len(preys):
        x, y = random.randint(0, 9), random.randint(0, 14)
        if not cells[x][y].get_occupant():
            a = Prey(x, y)

            # Child gets left ([0]) and forward left ([1]) vision from prey 1
            # and forward right ([4]) vision from prey 2

            a.neural_network.synaptic_weights[0] = prey1.neural_network.synaptic_weights[0]
            a.neural_network.synaptic_weights[1] = prey1.neural_network.synaptic_weights[1]
            a.neural_network.synaptic_weights[4] = prey2.neural_network.synaptic_weights[4]

            if random.randint(0, 1000) < mutation_rate:
                i, j = random.randint(0, 4), random.randint(0, 7)
                l, k = random.randint(0, 4), random.randint(0, 7)
                a.neural_network.synaptic_weights[i][j], a.neural_network.synaptic_weights[l][k] = a.neural_network.synaptic_weights[l][k], a.neural_network.synaptic_weights[i][j]

            interface.child_preys += 1
            break


class Predator(Being):
    def __init__(self, x, y):
        super().__init__(x, y)
        predators.append(self)
        self.set_orientation("up")

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

    def make_move(self):
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
