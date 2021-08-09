import os
import sys
import time
from functools import partial
from pprint import pprint as echo

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtWidgets import QComboBox, QMenu
from StatusBarMgr import StatusBarMgr

from Lib.TextProcessor import TextProcessor


class ExcerptGenerator():
    def __init__(self, MainWindow: QtWidgets):
        self.MW = MainWindow
        self.StatusBarMgr = StatusBarMgr(self.MW)
        self.TextProcessor = TextProcessor()
        self.Clipboard = QtWidgets.QApplication.clipboard()

    def LayListener(self):
        self.MW.MakeExcerptBtn.clicked.connect(self.MakeExcerpt)
        self.MW.FormatSlugBtn.clicked.connect(self.FormatSlug)
        self.MW.CopyPureExcerptBtn.clicked.connect(
            partial(self.CopyTextInBox, 'PureExcerptBox'))
        self.MW.CopyFBExcerptBtn.clicked.connect(
            partial(self.CopyTextInBox, 'FBExcerptBox'))

    def MakeExcerpt(self):
        RawExcerpt = self.MW.ExcerptBox.toPlainText()

        if RawExcerpt:
            ExcerptList = []
            ExcerptSegment = RawExcerpt.splitlines()

            for line in ExcerptSegment:
                if line:
                    ExcerptList.append(line)

            FormattedExcerpt = '\n'.join(ExcerptList)
            self.MW.PureExcerptBox.setText(FormattedExcerpt)

            ContinueReadText = None

            PostSlug = self.MW.SlugBox.text().strip()

            if PostSlug:
                ContinueReadText = '繼續閱讀：https://blog.netsowl.com/{}/'.format(
                    PostSlug)
                FormattedExcerpt += '\n'+ContinueReadText
                self.MW.FBExcerptBox.setText(FormattedExcerpt)

            self.StatusBarMgr.setFlash(text='摘要產生完成！', second=1)
        else:
            self.StatusBarMgr.setFlash(text='沒有輸入摘要，無法產生格式化過的摘要！', second=1)

    def CopyTextInBox(self, BoxName='PureExcerptBox'):
        BoxInstance = getattr(self.MW, BoxName)

        self.Clipboard.setText(BoxInstance.toPlainText())

        self.StatusBarMgr.setFlash(text='已複製摘要！', second=1)

    def FormatSlug(self):
        PostSlug = self.MW.SlugBox.text()

        if PostSlug:
            FormattedSlug = self.TextProcessor.Slugify(PostSlug)
            self.MW.SlugBox.setText(FormattedSlug)
            self.Clipboard.setText(FormattedSlug)
            self.StatusBarMgr.setFlash(text='已格式化並複製文章代稱！', second=1)


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
