from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from items import Food, Predator, Prey

class Cell(QLabel):
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
        if isinstance(self.occupant, Food):
            return 3
        elif isinstance(self.occupant, Predator):
            return 2
        elif isinstance(self.occupant, Prey):
            return 1
        else:
            return 0