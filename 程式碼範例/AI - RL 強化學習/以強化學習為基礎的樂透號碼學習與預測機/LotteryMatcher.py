import argparse
import json
import os
import re
import time
from pprint import pprint as echo

LottoType = 'SuperLotto'
Input = '28 17 27 23 1 32 2'
Date = '2019/12/19'
HitNumber = '28 17 27 23 1 33 6'


class LotteryMatcher:
    def __init__(self, LottoType='SuperLotto', Input=[], Date=None, HitNumber=[], ShowPrize=True):
        self.LottoType = LottoType
        self.ShowPrize = ShowPrize
        self.InputList = list(map(int, re.findall(r"\d+", Input))
                              ) if isinstance(Input, str) else Input
        self.HitNumberList = list(map(int, re.findall(r"\d+", HitNumber))) if isinstance(
            HitNumber, str) else HitNumber
        self.DateList = Date.split('/') if Date != None else None
        self.HitNumber = {
            'Common': self.HitNumberList[:6],
            'Special': self.HitNumberList[6:7]
        }

        self.HitResult = {
            'Common': [],
            'Special': [],
            'CommonTotal': 0,
            'SpecialTotal': 0
        }

        self.DefineLotteryText()
        self.DefinePrizeRule()
        self.ProcessInput()

    def DefineLotteryText(self):
        self.LottoTypeMap = {
            'SuperLotto': '威力彩',
            'BigLotto': '大樂透'
        }

    def DefinePrizeRule(self):
        self.PrizeRule = {
            'SuperLotto': {
                '6-1': '頭獎',
                '6-0': '貳獎',
                '5-1': '參獎（15萬）',
                '5-0': '肆獎（2萬）',
                '4-1': '伍獎（4000）',
                '4-0': '陸獎（800）',
                '3-1': '柒獎（400）',
                '2-1': '捌獎（200）',
                '3-0': '玖獎（100）',
                '1-1': '普獎（100）',
            },
            'BigLotto': {
                '6-0': '頭獎',
                '5-1': '貳獎',
                '5-0': '參獎',
                '4-1': '肆獎',
                '4-0': '伍獎（2000）',
                '3-1': '陸獎（1000）',
                '2-1': '柒獎（400）',
                '3-0': '普獎（400）'
            }
        }

    def ProcessInput(self):
        self.Input = {
            'Common': self.InputList[:6],
            'Special': self.InputList[-1:]
        }

        # if self.LottoType == 'BigLotto':
        #     self.Input = {
        #         'Common': self.InputList[:6]
        #     }

        if self.LottoType == 'BigLotto':
            self.Input = {
                'Common': self.InputList,
                'Special': [0]
            }

    def LottoTypeText(self):
        return self.LottoTypeMap[self.LottoType]

    def GetPrize(self):
        PrizeDesc = '沒有中獎'
        PrizeIndex = '{}-{}'.format(self.HitResult['CommonTotal'],
                                    self.HitResult['SpecialTotal'])

        if PrizeIndex in self.PrizeRule[self.LottoType]:
            PrizeDesc = self.PrizeRule[self.LottoType][PrizeIndex]

        return PrizeDesc

    def HitSuperLotto(self):
        CommonIntersect = list(
            set(self.Input['Common']) & set(self.HitNumber['Common']))
        SpecialIntersect = list(
            set(self.Input['Special']) & set(self.HitNumber['Special']))

        self.HitResult['Common'] = CommonIntersect
        self.HitResult['Special'] = SpecialIntersect
        self.HitResult['CommonTotal'] = len(CommonIntersect)
        self.HitResult['SpecialTotal'] = len(SpecialIntersect)

        return self.HitResult

    def HitBigLotto(self):
        CommonIntersect = list(
            set(self.Input['Common']) & set(self.HitNumber['Common']))
        SpecialIntersect = list(
            set(self.Input['Common']) & set(self.HitNumber['Special']))

        self.HitResult['Common'] = CommonIntersect
        self.HitResult['Special'] = SpecialIntersect
        self.HitResult['CommonTotal'] = len(CommonIntersect)
        self.HitResult['SpecialTotal'] = len(SpecialIntersect)

        return self.HitResult

    def Hit(self):
        self.HitResult = getattr(self, 'Hit{}'.format(self.LottoType))()

        if self.ShowPrize:
            self.HitResult['Prize'] = self.GetPrize()

        self.HitResult['Type'] = self.LottoTypeText()

        return self.HitResult
