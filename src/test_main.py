from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys
from navigator import Navigator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    navi = Navigator.Navigator()
    navi.show()
    app.exec_()
