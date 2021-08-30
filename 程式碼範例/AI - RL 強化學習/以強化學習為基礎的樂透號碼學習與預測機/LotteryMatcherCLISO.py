# cython: language_level=3

import argparse
import json
from pprint import pprint as echo

from LotteryMatcher import LotteryMatcher

LottoType = 'SuperLotto'
Input = '28 17 27 23 1 32 2'
Date = '2019/12/19'
HitNumber = '28 17 27 23 1 33 6'


def Go():
    Pasr = argparse.ArgumentParser()
    Pasr.add_argument(
        "-t", "--LottoType", help="Lottery Type. Supported tags: SuperLotto, BigLotto.", default='SuperLotto')
    Pasr.add_argument(
        "-d", "--Date", help="Winning numbers at specific date. For Example: 2019/12/19")
    Pasr.add_argument(
        "-i", "--Input", help="Input data. For Example: 28 17 27 23 1 32 2")
    Pasr.add_argument("-n", "--HitNumber",
                      help="Number to be matched. For Example: 12 5 13 38 1 33 6")
    UsrArg = Pasr.parse_args()

    Output = None

    if UsrArg.Input != None:
        IsInputJSON = False

        try:
            InputList = json.loads(UsrArg.Input)
            IsInputJSON = True
        except ValueError as e:
            pass

        if not IsInputJSON:
            InputList = [UsrArg.Input]

        for NumRow in InputList:
            LM = LotteryMatcher(LottoType=UsrArg.LottoType,
                                Input=NumRow, HitNumber=UsrArg.HitNumber)
            Output = LM.Hit()
            echo(NumRow)
            echo(Output)
            echo('-------------------------------------')
