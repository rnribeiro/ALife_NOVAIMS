import random

from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from cell import Cell
from items import Prey, Predator, Food
from items import cells, preys, predators, food_units, initial_energy, mutation_rate, likelihood_reproduction, food_energy, reproduction_energy, max_preys



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

        self.iterations_sb.setValue(100)
        self.initial_energy_sb.setValue(100)
        self.mutation_rate_sb.setValue(2)
        self.prey_sb.setValue(10)
        self.predator_sb.setValue(10)
        self.likelihood_repro_sb.setValue(50)
        self.food_energy_db.setValue(5)
        self.repro_energy_sb.setValue(20)
        self.max_preys_sb.setValue(20)

        
    # Start timer
    def start(self):
        if not self.items_created:
            self.initialize_items()
            self.items_created = True
            self.iterations = 0
            self.max_iterations = self.iterations_sb.value()
            initial_energy = self.initial_energy_sb.value()
            mutation_rate = self.mutation_rate_sb
            likelihood_reproduction = self.likelihood_repro_sb.value()
            food_energy = self.food_energy_db.value()
            reproduction_energy = self.repro_energy_sb.value()
            max_preys = self.max_preys_sb.value()
        self.active = True

    #Pause/resume timer
    def pause(self):
        self.active = not self.active

    
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
            for j in range(0, 15):
                my_cell = Cell(i, j)
                cell_row.append(my_cell)
                self.table.addWidget(my_cell, i, j)
            cells.append(cell_row)

    def initialize_items(self):
        prey_initial_count = self.prey_sb.value()
        for i in range(prey_initial_count):
            while True:
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
        for i in range(6):
            while True:
                x, y = random.randint(0, 9), random.randint(0, 14)
                if not cells[x][y].get_occupant():
                    a = Food(x, y)
                    break

    def iterate(self):
        if self.active and self.iterations<=self.max_iterations:
            random.shuffle(preys)
            random.shuffle(predators)
            for prey in preys:
                prey.make_best_move()
            for predator in predators:
                predator.make_random_move()
            self.iterations +=1
            self.iterations_sb.setValue(self.iterations)
        