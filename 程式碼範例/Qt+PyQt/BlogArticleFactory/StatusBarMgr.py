import os
import sys
import time
from pprint import pprint as echo

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer


class StatusBarMgr():
    def __init__(self, MainWindow: QtWidgets):
        self.MW = MainWindow
        self.OriginalText = ''

        self.FlashTextTimer = QTimer(self.MW)
        self.FlashTextTimer.timeout.connect(self.setRestore)

    def set(self, text='無狀態'):
        self.MW.StatusBar.setText(text)

    def get(self):
        return self.MW.StatusBar.text()

    def setRestore(self):
        self.FlashTextTimer.stop()
        self.set(self.OriginalText)

    def setFlash(self, text='無狀態', second=3, restore_text=None):
        self.OriginalText = self.get() if not restore_text else restore_text
        self.set(text)
        self.FlashTextTimer.start(second*1000)


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
