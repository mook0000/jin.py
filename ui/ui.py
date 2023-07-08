from kiwoom.kiwoom import *
from PyQt5.QtWidgets import *
import sys

class Ui_class():
    def __init__(self):
        print("Ui_class입니다.")

        self.app=QApplication(sys.argv)

        Kiwoom()

        self.app.exec_()