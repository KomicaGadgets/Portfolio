import os
import sys
import time
from pprint import pprint as echo

from SharedMgr import F
from StatusBarMgr import StatusBarMgr


class LocalWordConverter():
    def __init__(self):
        self.ConvertMap = None
        self.LoadCNTWMap()

    def LoadCNTWMap(self):
        MapWordList = list(filter(None, F.CNTWMapFile.SafeRead().splitlines()))

        for key, map_item in enumerate(MapWordList):
            MapWordList[key] = map_item.split()

        self.ConvertMap = MapWordList

    def Convert(self, Text):
        Text = Text.strip()

        for ConvItem in self.ConvertMap:
            if ConvItem[0] in Text:
                Text = Text.replace(ConvItem[0], ConvItem[1])

        return Text


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
