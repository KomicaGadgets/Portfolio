# cython: language_level=3

import asyncio
import hashlib
import json
import random
import sys
import time
from pprint import pprint as echo

import gym
import numpy as np
from DBMgr import DBMgr
from gym import spaces
from gym.utils import seeding
from LotteryMatcher import LotteryMatcher
from SharedMgr import F


class BigLottoRL(gym.Env):
    def __init__(self, CustomNum=[], CustomPrizeNum=[], RestartIndex=0, IsLoadDBProgress=0):
        self.DBMgr = DBMgr(
            LottoType='BigLotto', RestartIndex=RestartIndex, IsLoadDBProgress=IsLoadDBProgress)
        self.int_seed = 19921123
        self.action_space = spaces.MultiDiscrete([49, 49, 49, 49, 49, 49])
        self.observation_space = spaces.MultiDiscrete(
            [49, 49, 49, 49, 49, 49, 49, 1200, 1200])

        self.next_number = 0
        self.guess_count = 0
        self.guess_max = 1000 * 2
        self.observation = 0

        self.seed(self.int_seed)
        self.CustomNum = CustomNum if CustomNum else None
        self.CustomPrizeNum = CustomPrizeNum if CustomPrizeNum else None
        self.reset()

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        CorrectAction = action + 1
        PredictedNumber = CorrectAction.tolist()

        LMOutput = LotteryMatcher(
            LottoType='BigLotto',
            Input=PredictedNumber,
            HitNumber=self.CustomPrizeNum if self.CustomPrizeNum else self.next_number
        ).Hit()

        reward = 0
        done = False

        if LMOutput['CommonTotal'] + LMOutput['SpecialTotal'] >= 3:
            reward = 1

        self.guess_count += 1
        if self.guess_count >= self.guess_max:
            done = True

        return self.observation, reward, done, {
            'Prize': LMOutput['Prize'],
            'HitCommon': LMOutput['Common'],
            'HitSpecial': LMOutput['Special'],
            'predicted_number': sorted(PredictedNumber),
            'session_no': self.DBMgr.SessionNo,
            'next_number': sorted(self.next_number[:6]) + self.next_number[6:7],
            'RowIndex': self.DBMgr.RowIndex
        }

    def reset(self):
        SequentialHistory = self.DBMgr.SequentialHistoryNumber(
            IsAppendSalesInfo=1)
        NextSequentialHistory = self.DBMgr.NextHistoryNumber(
            IsAppendSalesInfo=1)
        self.next_number = NextSequentialHistory
        self.guess_count = 0
        self.observation = SequentialHistory
        return self.observation


class BigLottoRL_Real(BigLottoRL):
    def reset(self):
        LatestHistory = self.CustomNum if self.CustomNum else self.DBMgr.LatestHistoryNumber(
            IsAppendSalesInfo=1)
        NextHistory = self.CustomPrizeNum if self.CustomPrizeNum else self.DBMgr.NextHistoryNumber(
            IsAppendSalesInfo=1)
        self.next_number = NextHistory
        self.guess_count = 0
        self.observation = LatestHistory
        return self.observation


class VisualizeHelper():
    def __init__(self):
        self.DatePK = None

    def SaveProgress(self, RowIndex, DatePK):
        RawSaveData = F.LastTrainSave.SafeRead()
        SaveData = json.loads(RawSaveData) if RawSaveData else {}
        SaveData['RowIndex'] = RowIndex
        SaveData['DatePK'] = DatePK
        F.LastTrainSave.Write(json.dumps(
            SaveData, indent=4, sort_keys=True))

    def ViewResult(self, Model, env, E, MH, DatePK=None, PredictBatch=5, IsReduceFromManyMode=False, IsVerbose=1, IsSaveProgress=0):
        def FormatMsg(Observation, Info):
            Info = Info[0]
            MsgLine = [
                '觀察值：{}　中獎情形：{}'.format(
                    ', '.join([str(n) for n in Observation]), Info.get('Prize')),
                '預測號碼：{}　目標獎號：{}'.format(
                    Info.get('predicted_number'), Info.get('next_number')[:7]),
                '兌獎期號：{}'.format(
                    DatePK if DatePK else Info.get('session_no')),
                '命中普通號碼：{}　命中特別號：{}'.format(
                    Info.get('HitCommon'), Info.get('HitSpecial'))
            ]
            return '\n'.join(MsgLine)

        if IsReduceFromManyMode:
            RFMModeSpanSize = 89183 + random.randint(-29728, 29728)
            echo('本次以多取少前置樣本數：{}'.format(RFMModeSpanSize))
            echo('號碼預測即將在 3 秒後開始...')
            time.sleep(3)

        obs = env.reset()
        while True:
            action, _states = Model.predict(obs)    # action=[[...]]
            obs, rewards, dones, info = env.step(action)

            CorrectAction = action + 1
            Observation = obs.tolist()[0]
            Pred = CorrectAction.tolist()[0]

            if len(set(Pred)) < 6:
                continue

            SortedPredict = sorted(Pred)
            HashBox = hashlib.sha1()
            HashBox.update(str(SortedPredict).encode('utf8'))
            SPHash = HashBox.hexdigest()

            if SPHash not in MH.PredictedOutputHash:
                MH.PredictedOutput.append(SortedPredict)
                MH.PredictedOutputHash.append(SPHash)

            if bool(IsVerbose):
                print(FormatMsg(Observation, info))
                print('-------------------------------------------------')

            if IsReduceFromManyMode:
                if len(MH.PredictedOutput) >= RFMModeSpanSize + PredictBatch:
                    MH.PredictedOutput = MH.PredictedOutput[-1 * PredictBatch:]
                    break
            else:
                if len(MH.PredictedOutput) >= PredictBatch:
                    break

        if bool(IsSaveProgress):
            self.SaveProgress(info[0].get('RowIndex'),
                              info[0].get('session_no'))

        if bool(IsVerbose):
            echo(MH.PredictedOutput)


class ModelHelper():
    def __init__(self):
        self.LottoType = 'BigLotto'
        self.RunEnv = ['BigLottoRL']
        self.PredictedOutput = []
        self.PredictedOutputHash = []
        self.vh = None
        self.ModelCfg = {
            'BigLottoRL': {
                'algo': 'A2C',
                'policy': 'MlpPolicy',
                        'total_timesteps': 10000
            }
        }
