from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import random 
from numpy import *
from neural_network import *

"""
For simplicity:
zizoid = prey
wsiloids = predator

"""

cells= []
preys = []
predators = []
food_units = []
initial_energy = 0
mutation_rate = 0
likelihood_reproduction = 0
food_energy = 0
reproduction_energy = 0
max_preys = 0

class cell(QLabel):
    def __init__(self, x, y):
        super().__init__()
        self.setFixedWidth(40)
        self.setFixedHeight(40)
        self.setScaledContents(True)
        self.setPixmap(QPixmap("images/void.png"))
        self.coordinates = (x, y)
        self.occupant = None
        
    def set_occupant(self, occupant):
        self.occupant = occupant
        if occupant:
            self.setPixmap(occupant.get_image())
        else:                                                                                
            self.setPixmap(QPixmap("images/void.png"))
    
    def get_occupant(self):
        return self.occupant

    def get_coordinates(self):
        return self.coordinates

    def get_occupant_type_code(self):
        if isinstance(self.occupant, food):
            return 3
        elif isinstance(self.occupant, predator):
            return 2
        elif isinstance(self.occupant, prey):
            return 1
        else:
            return 0

class item():
    def __init__(self, x, y):
        self.coordinates = (x, y)
        self.cell = cells[x][y]
        self.set_orientation("up")
    def get_coordinates(self):
        return self.coordinates

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
            if isinstance(self, prey) and isinstance(cells[x][y].get_occupant(), prey):
                self.stop()
            if isinstance(self, prey) and isinstance(cells[x][y].get_occupant(), food):
                self.lose_mov_energy()
                self.eat_food(cells[x][y].get_occupant())
                cells[x][y].set_occupant(None)
                self.cell.setPixmap(QPixmap("images/void.png"))
                self.cell.set_occupant(None)
                self.coordinates = (x, y)
                self.cell = cells[x][y]
            if isinstance(self, prey) and isinstance(cells[x][y].get_occupant(), predator):
                cells[x][y].eat_prey(self)
                self.cell.setPixmap(QPixmap("images/void.png"))
                self.cell.set_occupant(None)
                self.die()
            
            
            if isinstance(self, predator) and isinstance(cells[x][y].get_occupant(), food):
                self.eat_food(cells[x][y].get_occupant())
                cells[x][y].set_occupant(None)
                self.cell.setPixmap(QPixmap("images/void.png"))
                self.cell.set_occupant(None)
                self.coordinates = (x, y)
                self.cell = cells[x][y]
                self.lose_mov_energy()
            
            if isinstance(self, predator) and isinstance(cells[x][y].get_occupant(), predator):
                self.stop()

            if isinstance(self, predator) and isinstance(cells[x][y].get_occupant(), prey):
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

class food(item):
    def __init__(self, x, y):
        super().__init__(x, y)
        food_units.append(self)
        self.energy = food_energy
    def set_orientation(self, orientation):
        self.set_image("images/food.png")
    def get_energy(self):
        return self.energy

class being(item):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.energy = initial_energy
        self.vision = []
        self.neural_network = neural_network()
        self.gender = random.choice(['m', 'f'])
        self.move_cost = 10


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
            neighbours = [(0,1), (1, 1), (1, 0), (1, -1), (0, -1)]
        elif self.orientation == "up":
            neighbours = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)]
        elif self.orientation == "right":
            neighbours = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0)]
        else: 
            neighbours = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0)]
        
        for x, y in neighbours:
            x, y = self.coordinates[0]+x, self.coordinates[1]+y
            if x < 0:
                x = 9
            if x > 9:
                x = 0
            if y < 0:
                y = 14  
            if y > 14:
                y = 0
            type = cells[x][y].get_occupant_type_code()
            self.vision.append(type)
    def move_left(self):
        if self.orientation == "down":
            self.move(self.coordinates[0], self.coordinates[1]+1)
            self.set_orientation("right")
        elif self.orientation == "up":
            self.move(self.coordinates[0], self.coordinates[1]-1)
            self.set_orientation("left")
        elif self.orientation == "right":
            self.move(self.coordinates[0]-1, self.coordinates[1])
            self.set_orientation("up")
        else:
            self.move(self.coordinates[0]+1, self.coordinates[1])
            self.set_orientation("down")
    def move_right(self):
        if self.orientation == "down":
            self.move(self.coordinates[0], self.coordinates[1]-1)
            self.set_orientation("left")
        elif self.orientation == "up":
            self.move(self.coordinates[0], self.coordinates[1]+1)
            self.set_orientation("right")
        elif self.orientation == "right":
            self.move(self.coordinates[0]+1, self.coordinates[1])
            self.set_orientation("down")
        else:
            self.move(self.coordinates[0]-1, self.coordinates[1])
            self.set_orientation("up")
    def move_forward(self):
        if self.orientation == "down":
            self.move(self.coordinates[0]+1, self.coordinates[1])
            self.set_orientation("down")
        elif self.orientation == "up":
            self.move(self.coordinates[0]-1, self.coordinates[1])
            self.set_orientation("up")
        elif self.orientation == "right":
            self.move(self.coordinates[0], self.coordinates[1]+1)
            self.set_orientation("right")
        else:
            self.move(self.coordinates[0], self.coordinates[1]-1)
            self.set_orientation("left")
    def move_back(self):
        if self.orientation == "down":
            self.move(self.coordinates[0]-1, self.coordinates[1])
            self.set_orientation("up")
        elif self.orientation == "up":
            self.move(self.coordinates[0]+1, self.coordinates[1])
            self.set_orientation("back")
        elif self.orientation == "right":
            self.move(self.coordinates[0], self.coordinates[1]-1)
            self.set_orientation("left")
        else:
            self.move(self.coordinates[0], self.coordinates[1]+1)
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
    
class prey(being):
    def __init__(self, x, y):
        super().__init__(x, y)
        preys.append(self)
        
    def set_orientation(self, orientation):
        self.orientation = orientation
        if orientation =="down":
            self.set_image("images/prey_down.png")
        elif orientation == "up":
            self.set_image("images/prey_up.png")
        elif orientation == "right":
            self.set_image("images/prey_right.png")
        else:
            self.set_image("images/prey_left.png")

class predator(being):
    def __init__(self, x, y):
        super().__init__(x, y)
        predators.append(self)

    def set_orientation(self, orientation):
        self.orientation = orientation
        if orientation =="down":
            self.set_image("images/predator_down.png")
        elif orientation == "up":
            self.set_image("images/predator_up.png")
        elif orientation == "right":
            self.set_image("images/predator_right.png")
        else:
            self.set_image("images/predator_left.png")

class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("ui/gui.ui", self)
        self.active = False
        self.items_created = False
        self.initialize_grid()

        self.start_btn.clicked.connect(self.start)
        self.pause_btn.clicked.connect(self.pause)
        self.stop_btn.clicked.connect(self.stop)

        self.timer = QTimer()
        self.timer.timeout.connect(self.iterate)
        self.timer.start(1000)

    def start(self):
        if not self.items_created:
            self.initialize_items()
            self.items_created = True
        self.active = True

    def pause(self):
        if self.active:
            self.active = False
        else: 
            self.active = True
    def stop(self):
        self.active = False
        for row in cells:
            for cell in row:
                cell.setPixmap(QPixmap("images/void.png"))
                cell.set_occupant(None)
        preys.clear()
        predators.clear()
        food_units.clear()

        self.items_created = False

    def initialize_grid(self):
        for i in range(0, 10):
            cell_row = []
            for j in range(0,15):
                mycell = cell(i, j)
                cell_row.append(mycell)
                self.table.addWidget(mycell, i, j)
            cells.append(cell_row)
    
    def initialize_items(self):
        prey_initial_count = self.prey_sb.value()
        for i in range(prey_initial_count):
            while True:
                x, y = random.randint(0, 9), random.randint(0, 14)
                if not cells[x][y].get_occupant():
                    a = prey(x, y)
                    break
        predator_initial_count = self.predator_sb.value()
        for i in range(predator_initial_count):
            while True:
                x, y = random.randint(0, 9), random.randint(0, 14)
                if not cells[x][y].get_occupant():
                    a = predator(x, y)
                    break
        for i in range(6):
            while True:
                x, y = random.randint(0, 9), random.randint(0, 14)
                if not cells[x][y].get_occupant():
                    a = food(x, y)
                    break
        
    def iterate(self):
        if self.active:
            random.shuffle(preys)
            random.shuffle(predators)
            for prey in preys:
                prey.make_best_move()
            for predator in predators:
                predator.make_random_move()

def main():
    app = QApplication([])
    window = MyGUI()
    window.show()
    app.exec_()
    
if __name__ == '__main__':
    main()