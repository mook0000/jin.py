from kiwoom.kiwoom import *
import sys
from PyQt5.QtWidgets import *

class Main():
    def __init__(self):
        print("실행할 메인 클라스")

        self.app=QApplication(sys.argv)
        self.kiwoom=Kiwoom()
        self.app.exec_()

if __name__ =='__main__':
    Main()