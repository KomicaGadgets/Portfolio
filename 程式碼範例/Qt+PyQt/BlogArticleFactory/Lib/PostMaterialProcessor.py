import os
import sys
import time
from functools import partial
from pprint import pprint as echo

import opencc
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWidgets import QComboBox, QMenu
from StatusBarMgr import StatusBarMgr

from Lib.LocalWordConverter import LocalWordConverter


class PostMaterialProcessor():
    def __init__(self, MainWindow: QtWidgets):
        self.MW = MainWindow
        self.StatusBarMgr = StatusBarMgr(self.MW)
        self.Clipboard = QtWidgets.QApplication.clipboard()

        self.OCC = opencc.OpenCC('t2tw.json')
        self.LWC = LocalWordConverter()

    def LayListener(self):
        self.MW.FormatParagraphBtn.clicked.connect(self.FormatPostMaterial)
        self.MW.TranslateResultBtn.clicked.connect(self.GTranslateResult)
        self.MW.OpenCCBtn.clicked.connect(self.OpenCCProcess)
        self.MW.ClearPostMaterialBtn.clicked.connect(self.ClearPostMaterial)
        self.MW.UpdateCNTWMapBtn.clicked.connect(self.UpdateCNTWMap)

    def FormatPostMaterial(self):
        RawMat = self.MW.PostMaterialBox.toPlainText()

        if RawMat:
            FormattedText = RawMat.replace('\n', ' ').replace(
                '. ', '.\n').replace('\n ', '\n').replace('? ', '?\n').replace(
                '! ', '!\n')
            OriginalResultBoxText = self.MW.PostProcessResultBox.toPlainText()
            ResultBoxText = FormattedText

            if OriginalResultBoxText:
                ResultBoxText = OriginalResultBoxText+'\n'+FormattedText

            self.MW.PostProcessResultBox.setPlainText(ResultBoxText)

            self.StatusBarMgr.setFlash(text='文章素材格式化完成！', second=1)

    def GTranslateResult(self):
        self.Clipboard.setText(self.MW.PostProcessResultBox.toPlainText())
        self.MW.GTranslateBtn.click()

    def OpenCCProcess(self):
        RawResult = self.MW.PostProcessResultBox.toPlainText()

        if RawResult:
            ConvertedText = self.OCC.convert(RawResult)
            ConvertedText = self.LWC.Convert(ConvertedText)
            self.MW.PostProcessResultBox.setPlainText(ConvertedText)

            self.StatusBarMgr.setFlash(text='OpenCC 轉換完成！', second=1)

    def ClearPostMaterial(self):
        self.MW.PostMaterialBox.setPlainText('')
        self.MW.PostProcessResultBox.setPlainText('')

    def UpdateCNTWMap(self):
        self.LWC.LoadCNTWMap()
        self.StatusBarMgr.setFlash(text='支語替換表更新完成！', second=1)


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
