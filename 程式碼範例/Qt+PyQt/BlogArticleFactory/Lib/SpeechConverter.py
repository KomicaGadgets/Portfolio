import os
import sys
import time
from pprint import pprint as echo


class SpeechConverter():
    def __init__(self):
        self.CommandMap = [
            {'cmd': '\n\n', 'text': ['QQ', '斷航', '斷行', '段行']},
            {'cmd': '\n\n', 'text': ['斷糧行', '斷兩行']},
        ]

        self.FormatMap = [
            {'to': '，', 'text': ['逗號', '豆號', '逗點', '豆點']},
            {'to': '。', 'text': ['句號', '具號', '句點']},
            {'to': '？', 'text': ['問號']},
            {'to': ' ', 'text': ['空格']},
            {'to': ' E-mail ', 'text': ['email']},
            {'to': ' PDF ', 'text': ['pdf']},
            {'to': '將會', 'text': ['江蕙']},
            {'to': '將要', 'text': ['江右']},
            {'to': '部份', 'text': ['部分']},
            {'to': '而非', 'text': ['阿飛']},
            {'to': '章節', 'text': ['張傑', '張捷']},
        ]

    def TextToCmd(self, Text):
        Text = Text.strip()

        for Conv in self.CommandMap:
            for word in Conv.get('text'):
                if word in Text:
                    Text = Text.replace(word, Conv.get('cmd'))
                    break

        return Text

    def FormatText(self, Text):
        Text = Text.strip()

        for Conv in self.FormatMap:
            for word in Conv.get('text'):
                if word in Text:
                    Text = Text.replace(word, Conv.get('to'))
                    break

        return Text


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
