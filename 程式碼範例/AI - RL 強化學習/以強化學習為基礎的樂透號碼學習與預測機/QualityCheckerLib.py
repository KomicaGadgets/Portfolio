import argparse
import json
import random
import re
import select
import sys
import time
from pprint import pprint as echo

from DBMgr import DBMgr
from Genesys.InteractiveConsole import InteractiveConsole
from LotteryMatcher import LotteryMatcher


class QualityChecker():
    def __init__(self, RecallDistance=1, LottoType='BigLotto'):
        self.LottoType = LottoType
        self.DBMgr = DBMgr(LottoType=self.LottoType)

        RecallSQLObj = self.DBMgr.RecallHistoryNumber(
            Nth=RecallDistance + 1, IsPureNum=0)
        self.InputDate = RecallSQLObj['pk']

        self.PreviousPrizeNum = self.DBMgr.ExtractNumFromSQLObj(RecallSQLObj)
        self.PreviousPrizeNum.append(RecallSQLObj['previous_sales_amount'])
        self.PreviousPrizeNum.append(RecallSQLObj['previous_commision'])

        NextPrizeSQLObj = self.DBMgr.InitSQL().where(
            'pk', self.InputDate, '>').orderBy('pk', 'ASC').limit(1).fetch()
        self.PrizeDate = NextPrizeSQLObj['pk']
        self.NextPrizeNum = self.DBMgr.ExtractNumFromSQLObj(NextPrizeSQLObj)

        self.PredictedOutput = [[]]

        self.QCStatistic = {
            'HitCount': 0,
            'Hit1stCount': 0,
            'Hit2ndCount': 0,
            'Hit3rdCount': 0,
            'Hit4thCount': 0,
            'CommonHit2Count': 0,
            'CommonHit1Count': 0,
            'SpecialHitCount': 0
        }

        self.QCPercent = {
            'Total': 0
        }

        self.QualityList = []

    def CountPredict(self, PredictedOutput=[[]], IsVerbose=1):
        self.PredictedOutput = PredictedOutput
        IsVerbose = bool(IsVerbose)
        for NumRow in self.PredictedOutput:
            LMOutput = LotteryMatcher(
                LottoType=self.LottoType, Input=NumRow, HitNumber=self.NextPrizeNum).Hit()

            if IsVerbose:
                echo(LMOutput)

            if LMOutput['Prize'] != '沒有中獎':
                self.QCStatistic['HitCount'] += 1

                if LMOutput['Prize'] == '頭獎':
                    self.QCStatistic['Hit1stCount'] += 1
                if LMOutput['Prize'] == '貳獎':
                    self.QCStatistic['Hit2ndCount'] += 1
                if LMOutput['Prize'] == '參獎':
                    self.QCStatistic['Hit3rdCount'] += 1
                if LMOutput['Prize'] == '肆獎':
                    self.QCStatistic['Hit4thCount'] += 1

            if LMOutput['CommonTotal'] == 1 or LMOutput['CommonTotal'] == 2:
                self.QCStatistic['CommonHit{}Count'.format(
                    LMOutput['CommonTotal'])] += 1

            if LMOutput['SpecialTotal'] > 0:
                self.QCStatistic['SpecialHitCount'] += 1

        if IsVerbose:
            echo(self.QCStatistic)

    def AnalyzePossibility(self):
        PredictLen = len(self.PredictedOutput)

        self.QCPercent['Total'] = (self.QCStatistic['HitCount'] / PredictLen) * 100

    def VisualizeQuality(self):
        def PrintRatio(key, val, PredictLen):
            TextTag = ''

            if key == 'HitCount':
                TextTag = '總中獎率'
            if key == 'Hit1stCount':
                TextTag = '頭獎中獎率'
            if key == 'Hit2ndCount':
                TextTag = '二獎中獎率'
            if key == 'Hit3rdCount':
                TextTag = '三獎中獎率'
            if key == 'Hit4thCount':
                TextTag = '四獎中獎率'
            if key == 'CommonHit2Count':
                TextTag = '2 個號碼命中率'
            if key == 'CommonHit1Count':
                TextTag = '1 個號碼命中率'
            if key == 'SpecialHitCount':
                TextTag = '特別號命中率'

            echo('{}：{} / {} = {}%'.format(TextTag,
                                           val, PredictLen, (val / PredictLen) * 100))

        echo('兌獎期號的上一期期號：{}'.format(self.InputDate))

        PredictLen = len(self.PredictedOutput)
        for key, val in self.QCStatistic.items():
            PrintRatio(key, val, PredictLen)


def Go():
    Pasr = argparse.ArgumentParser()
    Pasr.add_argument(
        "-c", "--CLI", nargs='?', const=True, help="使用指令模式。")
    Pasr.add_argument(
        "-l", "--LottoType", nargs='?', type=int, choices=[0, 1], help="樂透彩類型（1=大樂透，0=威力彩）")
    Pasr.add_argument(
        "-r", "--Recall", nargs='?', type=int, help="要回溯的中獎期數，輸入 1 代表以最近的上一期日期當作中獎日期，2 代表上二期，依此類推")
    UsrArg = Pasr.parse_args()

    if not UsrArg.CLI:
        IC = InteractiveConsole()
        UsrLottoType = IC.AskStr('請輸入樂透彩類型？（1=大樂透，0=威力彩）：',
                                 'BigLotto', 'SuperLotto')
        RecallDistance = IC.AskInt(
            '請輸入要回溯的中獎期數，輸入 1 代表以最近的上一期日期當作中獎日期，2 代表上二期，依此類推\n不輸入 = 1：', 1)
        PredictBatch = IC.AskInt('請輸入要一次檢測幾組號碼？（0 或不輸入 = 500 組）：', 500)
    else:
        UsrLottoType = UsrArg.LottoType
        RecallDistance = UsrArg.Recall
        PredictBatch = 500

    from Env.BigLottoRL import ModelHelper, VisualizeHelper

    MH = ModelHelper()
    VH = VisualizeHelper()
    Env = {}
    Model = {}

    MH.PredictedOutput = []

    QC = QualityChecker(RecallDistance)

    from QC_Runner import QC_Runner
    QCR = QC_Runner(UsrArg.CLI, UsrLottoType, QC.PrizeDate,
                    QC.PreviousPrizeNum, QC.NextPrizeNum, PredictBatch)

    MH, VH = QCR.Run(Env, Model, MH, VH)

    QC.CountPredict(MH.PredictedOutput, IsVerbose=0)
    QC.VisualizeQuality()


if __name__ == '__main__':
    Go()
