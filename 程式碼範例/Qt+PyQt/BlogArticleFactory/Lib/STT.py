import os
import sys
import time
from functools import partial
from pprint import pprint as echo

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWidgets import QComboBox, QMenu
from StatusBarMgr import StatusBarMgr

from Lib.STTWorker import STTWorker
from Lib.TextProcessor import TextProcessor


class STT():
    def __init__(self, MainWindow: QtWidgets):
        self.MW = MainWindow
        self.StatusBarMgr = StatusBarMgr(self.MW)
        self.TextProcessor = TextProcessor()
        self.STTQThread = None
        self.STTThreadCounter = 0

    def LayListener(self):
        self.MW.action_STT_Toggle.triggered.connect(self.ToggleSpeechToText)
        self.MW.CutSTTBtn.clicked.connect(self.CutText)
        self.MW.CutSTTBtn.setShortcut('Ctrl+0')
        self.MW.ClearSTTBtn.clicked.connect(self.ClearSTTText)
        self.MW.RefToYDBtn.clicked.connect(self.ReferenceToYahooDict)
        self.MW.RefToYDBtn.setShortcut('Ctrl+1')
        self.MW.GTranslateBtn.clicked.connect(self.GTranslateFromClipboard)
        self.MW.GTranslateBtn.setShortcut('Ctrl+2')

        for i in range(1, 3):
            BtnName = 'WrapTextBtn_{}'.format(i)
            BtnInstance = getattr(self.MW, BtnName)
            BtnInstance.clicked.connect(
                partial(self.WrapSelectedText, BtnName)
            )

            BtnInstance.setShortcut(
                self.TextProcessor.WrapperShortcutMap.get(BtnName)
            )

    def CutText(self):
        Clipboard = QtWidgets.QApplication.clipboard()
        Clipboard.setText(self.MW.STTTextArea.toPlainText())
        self.MW.STTTextArea.setText('')
        self.StatusBarMgr.setFlash(text='已剪下語音辨識區裡的文字！', second=1)

    def ClearSTTText(self):
        self.MW.STTTextArea.setText('')
        self.StatusBarMgr.setFlash(text='已清除語音辨識區裡的文字！', second=1)

    def ReferenceToYahooDict(self):
        CbText = QtWidgets.QApplication.clipboard().text()

        if CbText:
            self.MW.YDView.load(
                QUrl(
                    'https://tw.dictionary.search.yahoo.com/search?p={}'.format(CbText))
            )
            self.MW.AppTabWidget.setCurrentIndex(2)
        else:
            self.StatusBarMgr.setFlash(text='沒有已複製的文字，無法前往查詢字典。', second=1)

    def GTranslateFromClipboard(self):
        CbText = QtWidgets.QApplication.clipboard().text().strip()

        if CbText:
            self.MW.GTView.load(
                QUrl(
                    'https://translate.google.com.tw/?hl=zh-TW#view=home&op=translate&sl=en&tl=zh-TW&text={}'.format(
                        CbText)
                )
            )
            self.MW.AppTabWidget.setCurrentIndex(1)
        else:
            self.StatusBarMgr.setFlash(
                text='沒有已複製的文字，無法使用 Google 翻譯。', second=1)

    def ToggleSpeechToText(self):
        if not self.STTQThread:
            self.STTQThread = STTWorker(
                self.MW, self.StatusBarMgr, self, self.STTThreadCounter)
            self.STTQThread.start()
            self.MW.action_STT_Toggle.setText('停止語音辨識並轉成文字(&R)')
            self.MW.STTStatus.setText('語音辨識狀態：已啟用 O')
            self.StatusBarMgr.set('語音辨識中，請開始說話...')
        else:
            self.STTThreadCounter += 1
            self.StatusBarMgr.set('正在停止語音辨識...')
            QTimer.singleShot(0.1*1000, self.StopSpeechToText)

    def StopSpeechToText(self):
        self.STTQThread.quit_flag = True
        self.STTQThread.requestInterruption()
        self.STTQThread = None
        self.StatusBarMgr.setFlash(text='已停止語音辨識', restore_text='無狀態')
        self.MW.action_STT_Toggle.setText('開始語音辨識並轉成文字(&R)')
        self.MW.STTStatus.setText('語音辨識狀態：未啟用 X')

    def WrapSelectedText(self, BtnName):
        SelectedText = self.MW.STTTextArea.textCursor().selectedText()

        if SelectedText:
            WrappedText = self.TextProcessor.WrapText(SelectedText, BtnName)
            self.MW.STTTextArea.textCursor().removeSelectedText()
            self.MW.STTTextArea.textCursor().insertText(WrappedText)
        else:
            self.StatusBarMgr.setFlash(text='沒有選取字詞，無法為字詞加上包圍符號。', second=1)

    # def InsertJquery(self):
    #     self.Page.runJavaScript(
    #         """
    # 	var script = document.createElement("SCRIPT");
    # 	script.src = 'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js';
    # 	script.type = 'text/javascript';
    # 	script.onload = function() {
    # 		var $ = window.jQuery;
    # 		// Use $ here...
    # 	};
    # 	document.getElementsByTagName("head")[0].appendChild(script);
    # 	"""
    #     )
    #     self.Page.runJavaScript(F.InitSTT.Read())


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
