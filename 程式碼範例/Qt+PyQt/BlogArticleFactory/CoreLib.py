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
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *

from Lib.ExcerptGenerator import ExcerptGenerator
from Lib.STT import STT
from Lib.PostMaterialProcessor import PostMaterialProcessor
from StatusBarMgr import StatusBarMgr
from TabWidgetMgr import TabWidgetMgr


class CoreLib():
    def __init__(self, MainWindow: QtWidgets):
        self.MW = MainWindow
        self.STT = STT(self.MW)
        self.ExcerptGenerator = ExcerptGenerator(self.MW)
        self.PostMaterialProcessor = PostMaterialProcessor(self.MW)
        self.TabWidgetMgr = TabWidgetMgr(self.MW)
        self.StatusBarMgr = StatusBarMgr(self.MW)

    def LayShortcut(self):
        self.Shortcut_NextTab = QShortcut(
            QKeySequence('Ctrl+Right'), self.MW.AppTabWidget)
        self.Shortcut_NextTab.activated.connect(self.TabWidgetMgr.NextTab)

        self.Shortcut_NextTab = QShortcut(
            QKeySequence('Ctrl+Left'), self.MW.AppTabWidget)
        self.Shortcut_NextTab.activated.connect(self.TabWidgetMgr.PreviousTab)

    def Launch(self):
        self.MW.showMaximized()

        self.LayShortcut()
        self.STT.LayListener()
        self.ExcerptGenerator.LayListener()
        self.PostMaterialProcessor.LayListener()

        self.MW.GTView.load(QUrl(
            'https://translate.google.com.tw/?hl=zh-TW#view=home&op=translate&sl=en&tl=zh-TW'))
        self.MW.YDView.load(QUrl(
            'https://tw.dictionary.search.yahoo.com/'))
        # self.MW.STTView.loadFinished.connect(self.STT.InsertJquery)


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
