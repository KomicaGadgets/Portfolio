import os
import re
import sys
import time
from pprint import pprint as echo


class TextProcessor():
    def __init__(self):
        self.WrapperMap = {
            'WrapTextBtn_1': '「」',
            'WrapTextBtn_2': '（）'
        }

        self.WrapperShortcutMap = {
            'WrapTextBtn_1': 'Ctrl+=',
            'WrapTextBtn_2': 'Ctrl+9'
        }

        self.KebabPatn = {
            'space': {
                'patn': re.compile(r' '),
                'to': '-'
            },
            'redundant': {
                'patn': re.compile(r'\?|,'),
                'to': ''
            }
        }

    def WrapText(self, Text, BtnName='WrapTextBtn_1'):
        WrapChars = self.WrapperMap.get(BtnName)
        Output = '{}{}{}'.format(
            WrapChars[0],
            Text,
            WrapChars[1]
        )

        return Output

    def Slugify(self, Text):
        Output = Text

        for key in self.KebabPatn:
            ReplaceInfo = self.KebabPatn.get(key)
            Output = ReplaceInfo['patn'].sub(ReplaceInfo['to'], Output)

        return Output.lower()


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
