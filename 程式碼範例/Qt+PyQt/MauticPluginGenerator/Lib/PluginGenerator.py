import os
import sys
import time
from functools import partial
from pprint import pprint as echo

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWidgets import QComboBox, QMenu
from StatusBarMgr import StatusBarMgr

from Lib.PluginManipulator import PluginManipulator


class PluginGenerator():
    def __init__(self, MainWindow: QtWidgets):
        self.MW = MainWindow
        self.StatusBarMgr = StatusBarMgr(self.MW)
        self.Clipboard = QtWidgets.QApplication.clipboard()

        self.PluginName = ''
        self.PluginShortName = ''

        self.PreviewPluginName()

    def LayListener(self):
        self.MW.PluginName.textChanged.connect(self.PreviewPluginName)
        self.MW.PluginShortName.textChanged.connect(self.PreviewPluginName)
        self.MW.PluginChNameCopyBtn.clicked.connect(
            partial(self.CopyTextInBox, 'PluginChName_Preview'))
        self.MW.PluginDescCopyBtn.clicked.connect(
            partial(self.CopyTextInBox, 'PluginDesc_Preview'))
        self.MW.PNNoSpaceCopyBtn.clicked.connect(
            partial(self.CopyTextInBox, 'PluginName_NoSpace'))
        self.MW.PNLowerCopyBtn.clicked.connect(
            partial(self.CopyTextInBox, 'PluginName_Lower'))
        self.MW.PNLowerNoSpaceCopyBtn.clicked.connect(
            partial(self.CopyTextInBox, 'PluginName_LowerNoSpace'))
        self.MW.UnderlineCopyBtn.clicked.connect(
            partial(self.CopyTextInBox, 'PluginName_Underline'))
        self.MW.GeneratePluginBtn.clicked.connect(self.GeneratePlugin)

    def LoadPriorInput(self):
        self.PluginName = self.MW.PluginName.text().strip()
        self.PluginShortName = self.MW.PluginShortName.text().strip()

    def PreviewPN_NoSpace(self):
        StripTarget = self.PluginName

        PNNoSpace = StripTarget.replace(' ', '')
        self.MW.PluginName_NoSpace.setText(PNNoSpace)

    def PreviewPN_Lower(self):
        LowerTarget = self.PluginShortName if self.PluginShortName else self.PluginName

        PNLower = LowerTarget.lower()
        self.MW.PluginName_Lower.setText(PNLower)

    def PreviewPN_LowerNoSpace(self):
        LNSTarget = self.PluginShortName if self.PluginShortName else self.PluginName

        PNLowerNoSpace = (LNSTarget.lower()).replace(' ', '')
        self.MW.PluginName_LowerNoSpace.setText(PNLowerNoSpace)

    def PreviewPN_Underline(self):
        UdrlineTarget = self.PluginShortName if self.PluginShortName else self.PluginName

        PNUnderline = (UdrlineTarget.lower()).replace(' ', '_')
        self.MW.PluginName_Underline.setText(PNUnderline)

    def PreviewPluginName(self):
        self.LoadPriorInput()

        self.PreviewPN_NoSpace()
        self.PreviewPN_Lower()
        self.PreviewPN_LowerNoSpace()
        self.PreviewPN_Underline()

    def CopyTextInBox(self, BoxName='PureExcerptBox'):
        BoxInstance = getattr(self.MW, BoxName)

        self.Clipboard.setText(BoxInstance.text())

        self.StatusBarMgr.setFlash(text='已複製預覽值！', second=1)

    def GeneratePlugin(self):
        PM = PluginManipulator(self.MW)
        PM.Generate()


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
