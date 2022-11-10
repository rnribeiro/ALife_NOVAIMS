from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import time
"""
For simplicity:
zizoid = prey
wsiloids = predator

"""

cells= []


class cell(QLabel):
    def __init__(self, x, y):
        super().__init__()
        self.setFixedWidth(40)
        self.setFixedHeight(40)
        self.setScaledContents(True)
        self.setPixmap(QPixmap("void.png"))
        self.coordinates = (x, y)
        
    def set_ocupant(self, ocupant):
        self.ocupant = ocupant
        self.setPixmap(ocupant.get_image())
    
    def get_ocupant(self):
        return self.ocupant

    def get_coordinates(self):
        return self.coordinates

    def ocupant_type_code():
        if isinstance(self.ocupant, food):
            return 3
        elif isinstance(self.ocupant, predator):
            return 2
        elif isinstance(self.ocupant, prey):
            return 1
        else:
            return 0

class item():
    def __init__():
        self.cell = cells[x][y]
        self.coordinates = (x, y)
        self.set_orientation("left")


class food():
    def __init__():
        self.energy = 10
        

preys = []
predators = []
food_units = []

class being(item):
    def __init__(self, x, y):
        self.energy = 100
        
        vision = []
        

    def move(self, x, y):
        print(x, y)
        self.cell.setPixmap(QPixmap("void.png"))
        if x < 0:
            x = 9
        if x > 9:
            x = 0
        if y < 0:
            y = 14  
        if y > 14:
            y = 0
        print(x, y)
        self.coordinates = (x, y)
        self.cell = cells[x][y]
        print(self.cell.get_coordinates())

        
    
    def vision():
        if self.orientation == "down":

        elif self.orientation == "up":
        elif self.orientation == "right":
        else:



        
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
    def set_image(self, image):
        self.image = QPixmap(image)
        self.cell.set_ocupant(self)
    def get_image(self):
        return self.image


    



  

class prey(being):
    def __init__(self, x, y):
        super().__init__(x, y)
        preys.append(self)
        

    def set_orientation(self, orientation):
        self.orientation = orientation
        if orientation =="down":
            self.set_image("predator_down.png")
        elif orientation == "up":
            self.set_image("predator_up.png")
        elif orientation == "right":
            self.set_image("predator_right.png")
        else:
            self.set_image("predator_left.png")

    


class predator(being):
    def __init__(self):
        super().__init__(x, y)
        predators.append(self)
        

    def set_orientation(self, orientation):
        self.orientation = orientation
        if orientation =="down":
            self.set_image("predator_down.png")
        elif orientation == "up":
            self.set_image("predator_up.png")
        elif orientation == "right":
            self.set_image("predator_right.png")
        else:
            self.set_image("predator_left.png")




class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("gui.ui", self)
        self.initialize()

        self.timer = QTimer()
        self.timer.timeout.connect(self.iterate)
        self.timer.start(500)

    def initialize(self):
        for i in range(0, 10):
            cell_row = []
            for j in range(0,15):
                mycell = cell(i, j)
                cell_row.append(mycell)
                self.table.addWidget(mycell, i, j)
            cells.append(cell_row)

        prey_1 = prey(0, 5)
        preys.append(prey_1)

        

    def iterate(self):
        preys[0].move_forward_right()

    

def main():
    app = QApplication([])
    window = MyGUI()
    window.show()
    
    app.exec_()
    
    
if __name__ == '__main__':
    main()


