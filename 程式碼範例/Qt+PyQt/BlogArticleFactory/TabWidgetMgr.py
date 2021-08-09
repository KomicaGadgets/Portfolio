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


class TabWidgetMgr():
    def __init__(self, MainWindow: QtWidgets):
        self.MW = MainWindow
        self.TabWidget = self.MW.AppTabWidget
        # self.StatusBarMgr = StatusBarMgr(self.MW)

    def PreviousTab(self):
        CurrentIndex = self.TabWidget.currentIndex()
        PreviousIndex = self.TabWidget.count()-1 if CurrentIndex == 0 else CurrentIndex-1

        self.TabWidget.setCurrentIndex(PreviousIndex)

    def NextTab(self):
        CurrentIndex = self.TabWidget.currentIndex()
        NextIndex = 0 if CurrentIndex == self.TabWidget.count()-1 else CurrentIndex+1

        self.TabWidget.setCurrentIndex(NextIndex)


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
