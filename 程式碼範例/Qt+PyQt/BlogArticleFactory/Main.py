import json
import os
import shlex
import sys
import time
from os import system as scmd
from pathlib import Path
from pprint import pprint as echo
from shutil import copyfile

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

import QtUI as ui
from CoreLib import CoreLib as Core


class Main(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    C = Core(window)
    C.Launch()
    sys.exit(app.exec_())
