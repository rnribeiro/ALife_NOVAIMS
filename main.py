from PyQt5.QtWidgets import *

from interface import MyGUI

"""
For simplicity:
zizoid = Prey
wsiloids = Predator

"""


def main():
    app = QApplication([])
    window = MyGUI()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
