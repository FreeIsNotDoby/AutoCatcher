import sys
from PyQt5.QtWidgets import *
from mainScreenBridge import mainScreenBridge


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = mainScreenBridge()
    window.show()
    app.exec_()

