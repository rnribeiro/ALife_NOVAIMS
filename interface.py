import random

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow

import items
from cell import Cell
from items import Prey, Predator, Food
from items import cells, preys, predators, food_units

child_preys = 0


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("ui/gui.ui", self)
        self.active = False
        self.items_created = False

        self.initialize_grid()

        # Set Predefine Values
        self.iterations_sb.setValue(10000)
        self.initial_energy_sb.setValue(100)
        self.mutation_rate_sb.setValue(2)
        self.prey_sb.setValue(10)
        self.predator_sb.setValue(10)
        self.likelihood_repro_sb.setValue(50)
        self.food_energy_db.setValue(5)
        self.repro_energy_sb.setValue(20)
        self.max_preys_sb.setValue(20)
        self.current_preys_sb.setValue(0)
        self.current_predators_sb.setValue(0)
        self.child_preys_sb.setValue(0)

        self.start_btn.clicked.connect(self.start)
        self.pause_btn.clicked.connect(self.pause)
        self.stop_btn.clicked.connect(self.stop)

        self.timer = QTimer()
        self.timer.timeout.connect(self.iterate)
        # Timer in milliseconds, the lower the timer, the faster the simulation runs
        self.timer.start(100)

    def start(self):
        if not self.items_created:
            # Get values from spin boxes
            items.initial_energy = self.initial_energy_sb.value()
            items.mutation_rate = self.mutation_rate_sb.value()
            items.likelihood_reproduction = self.likelihood_repro_sb.value()
            items.food_energy = self.food_energy_db.value()
            items.reproduction_energy = self.repro_energy_sb.value()
            items.max_preys = self.max_preys_sb.value()
            items.log = ""
            self.items_created = True
            self.iterations = 0
            self.max_iterations = self.iterations_sb.value()
            self.current_preys = 0
            self.current_predators = 0
            # Initialize Preys and Predators in the grid
            self.initialize_items()
        self.active = True

    # Pause/resume timer
    def pause(self):
        self.active = not self.active

    # Clear the grid
    def stop(self):
        self.active = False
        for row in cells:
            for cell in row:
                cell.setPixmap(QPixmap("images/void.png"))
                cell.set_occupant(None)
        preys.clear()
        predators.clear()
        food_units.clear()

        self.iterations_sb.setValue(10000)
        self.initial_energy_sb.setValue(100)
        self.mutation_rate_sb.setValue(2)
        self.prey_sb.setValue(10)
        self.predator_sb.setValue(10)
        self.likelihood_repro_sb.setValue(50)
        self.food_energy_db.setValue(5)
        self.repro_energy_sb.setValue(20)
        self.max_preys_sb.setValue(20)
        self.current_preys_sb.setValue(0)
        self.current_predators_sb.setValue(0)
        self.child_preys_sb.setValue(0)
        items.log = ""
        self.log_label.setText(items.log)

        self.items_created = False

    def initialize_grid(self):
        for i in range(0, 10):
            cell_row = []
            for j in range(0, 15):
                my_cell = Cell(i, j)
                cell_row.append(my_cell)
                self.table.addWidget(my_cell, i, j)
            cells.append(cell_row)

    def initialize_items(self):
        prey_initial_count = self.prey_sb.value()
        for i in range(prey_initial_count):
            while True and len(preys)<= items.max_preys:
                x, y = random.randint(0, 9), random.randint(0, 14)
                if not cells[x][y].get_occupant():
                    a = Prey(x, y)
                    break
        predator_initial_count = self.predator_sb.value()
        for i in range(predator_initial_count):
            while True:
                x, y = random.randint(0, 9), random.randint(0, 14)
                if not cells[x][y].get_occupant():
                    a = Predator(x, y)
                    break
        # Create food units
        for i in range(6):
            while True:
                x, y = random.randint(0, 9), random.randint(0, 14)
                if not cells[x][y].get_occupant():
                    a = Food(x, y)
                    break

    def iterate(self):
        if self.active and self.iterations < self.max_iterations and predators and preys:
            # Create a food item in the grid every "food_creation_rate" iterations
            food_creation_rate = 4
            if self.iterations % food_creation_rate == 0 and food_units.__len__() < 30:
                x, y = random.randint(0, 9), random.randint(0, 14)
                if not cells[x][y].get_occupant():
                    a = Food(x, y)

            for prey in preys:
                if prey.energy <= 0:
                    preys.remove(prey)
                    cells[prey.get_coordinates()[0]][prey.get_coordinates()[1]].setPixmap(QPixmap("images/void.png"))
                    cells[prey.get_coordinates()[0]][prey.get_coordinates()[1]].set_occupant(None)
                    del prey
                    continue
                else:
                    prey.make_move()

            for predator in predators:
                if predator.energy <= 0:
                    predators.remove(predator)
                    cells[predator.get_coordinates()[0]][predator.get_coordinates()[1]].setPixmap(QPixmap("images/void.png"))
                    cells[predator.get_coordinates()[0]][predator.get_coordinates()[1]].set_occupant(None)
                    del predator
                    continue
                else:
                    predator.make_move()

            self.iterations += 1
            items.log = f"-----  Iteration {self.iterations}  ----- \n{items.log}"
            self.log_label.setText(items.log)
            items.log = "\n" + items.log
            self.iterations_sb.setValue(self.iterations)
            self.current_preys_sb.setValue(len(preys))
            self.current_predators_sb.setValue(len(predators))
            self.child_preys_sb.setValue(child_preys)

        elif not preys and self.active:
            items.log = f"Predators won \n{items.log}"
            self.log_label.setText(items.log)
            self.active = False

        elif not predators and self.active:
            items.log = f"Preys won \n{items.log}"
            self.log_label.setText(items.log)
            self.active = False