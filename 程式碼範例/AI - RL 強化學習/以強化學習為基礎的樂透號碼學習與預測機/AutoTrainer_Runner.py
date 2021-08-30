import json
import random
import re
import sys
import time
from pathlib import Path
from pprint import pprint as echo

import gym
import numpy as np
import tensorflow as tf
from gym import spaces
from gym.utils import seeding
from stable_baselines import A2C, DQN, PPO2, TRPO
from stable_baselines.common import make_vec_env
from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines.common.policies import MlpLstmPolicy, MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv

from DBMgr import DBMgr
from Env.BigLottoRL import (BigLottoRL, BigLottoRL_Real, ModelHelper,
                            VisualizeHelper)
from Genesys.InteractiveConsole import InteractiveConsole
from Genesys.ToolBox import _vs, stop
from LotteryMatcher import LotteryMatcher
from SharedMgr import F


class AutoTrainer_Runner():
    def __init__(self, UsrLottoType, IsUseTrainedModel, RestartIndex):
        self.UsrLottoType = UsrLottoType
        self.IsUseTrainedModel = IsUseTrainedModel
        self.RestartIndex = RestartIndex

        self.QualityList = []

        self.FlagFiles = {
            'Stop': Path('.{}Stop'.format(self.UsrLottoType)),
            'Pause': Path('.{}Pause'.format(self.UsrLottoType))
        }

        self.QCThreshold = 200
        self.QCIncrement = 200
        self.QualityListFinalLen = 5
        self.QCSinglePredictGoal = 90
        self.QCMiniumSinglePredictGoal = 0
        self.QCTotalPredictGoal = 90

        self.IsModelRefined = 0

        self.ComputeMiniumHitPercent()

    def CheckPause(self):
        return self.FlagFiles.get('Pause').is_file()

    def CheckStop(self):
        IsStop = self.FlagFiles.get('Stop').is_file()

        if IsStop:
            self.FlagFiles.get('Stop').unlink()

        return IsStop

    def ComputeMiniumHitPercent(self):
        self.QCMiniumSinglePredictGoal = (
            (self.QCTotalPredictGoal - 100) * self.QualityListFinalLen) + 100

    def CheckQuality(self, Env, Model, MH, VH):
        QualityListLen = len(self.QualityList)

        for SessionOffset in range(1, self.QualityListFinalLen + 1):
            IsPause = 0

            MH.PredictedOutput = []

            QCOutput = _vs(
                'python3 "{}" -c -l 1 -r {}'.format(
                    F.QualityChecker.AbsPath(),
                    SessionOffset
                )
            )
            TotalHitPercent = float(
                re.findall(r'總中獎率.*=\s([\d.]+)%', QCOutput)[0]
            )
            echo(QCOutput)

            if TotalHitPercent >= self.QCMiniumSinglePredictGoal:
                self.QualityList.append(TotalHitPercent)

                QualityListLen = len(self.QualityList)

                if QualityListLen < self.QualityListFinalLen:
                    continue
            else:
                echo('單次預測準確率 {}%，小於最小基準值 {}%，預估平均準確率不可能達標，繼續訓練模型。'.format(
                    TotalHitPercent,
                    self.QCMiniumSinglePredictGoal
                ))
                self.QualityList = []
                break

            if QualityListLen >= self.QualityListFinalLen:
                AvgQuality = sum(self.QualityList) / QualityListLen

                if AvgQuality >= self.QCTotalPredictGoal:
                    echo('前 {} 期預測平均準確率為 {}%，大於 {}%，模型已準備好用於實戰。'.format(
                        QualityListLen,
                        AvgQuality,
                        self.QCTotalPredictGoal
                    ))
                    self.QualityListFinalLen += 5
                    self.ComputeMiniumHitPercent()
                    IsPause = 1
                else:
                    echo('前 {} 期預測平均準確率為 {}%，沒有大於 {}%，繼續訓練模型。'.format(
                        QualityListLen,
                        AvgQuality,
                        self.QCTotalPredictGoal
                    ))

            self.QualityList = []

            if bool(IsPause):
                self.FlagFiles.get('Pause').touch()
                echo('已寫入暫停命令')
                self.IsModelRefined = 1
                break

    def SaveRound(self, Round):
        RawSaveData = F.LastTrainSave.SafeRead()
        SaveData = json.loads(RawSaveData) if RawSaveData else {}
        SaveData['Round'] = Round
        F.LastTrainSave.Write(json.dumps(
            SaveData, indent=4, sort_keys=True))

    def InitQCThreshold(self, Round):
        IsComputeThreshold = 0

        if Round > self.QCThreshold:
            self.QCThreshold = Round

        if self.QCThreshold < 2000:
            IsComputeThreshold = 1

        if 1500 <= self.QCThreshold < 2000:
            self.QCIncrement = 50
            IsComputeThreshold = 1

        if bool(IsComputeThreshold):
            QCTMod = self.QCThreshold % self.QCIncrement
            if QCTMod > 0:
                self.QCThreshold += self.QCIncrement - \
                    (self.QCThreshold % self.QCIncrement)

        if self.QCThreshold >= 2000:
            self.QCIncrement = 1
            self.QCThreshold += 1

    def Run(self, Env, Model, MH, VH, Round=1):
        IsLoadDBProgress = 0

        if self.IsUseTrainedModel and F.LastTrainSave.Path.exists():
            SaveData = json.loads(F.LastTrainSave.Read())
            Round = SaveData.get('Round')
            self.InitQCThreshold(Round)
            IsLoadDBProgress = 1
        else:
            F.LastTrainSave.Del()

        for E in MH.RunEnv:
            CurrentEnv = globals()[E]
            Env[E] = SubprocVecEnv(
                [lambda: CurrentEnv(RestartIndex=self.RestartIndex, IsLoadDBProgress=IsLoadDBProgress)])
            Model[E] = None

        while Round > 0:
            if self.CheckPause():
                time.sleep(10)
                continue

            for E in MH.RunEnv:
                if not Model[E]:
                    Algo = globals()[MH.ModelCfg[E]['algo']]

                    if self.IsUseTrainedModel:
                        Model[E] = Algo.load(
                            'Data/{}Model_{}'.format(self.UsrLottoType, E))
                        Model[E].set_env(Env[E])
                    else:
                        Algo = globals()[MH.ModelCfg[E]['algo']]
                        Policy = globals()[MH.ModelCfg[E]['policy']]
                        Model[E] = Algo(Policy, Env[E])

                Model[E].learn(total_timesteps=MH.ModelCfg[E]
                               ['total_timesteps'])
                Model[E].save(
                    'Data/{}Model_{}'.format(self.UsrLottoType, E))

                VH.ViewResult(Model[E], Env[E], E, MH, IsSaveProgress=1)

            echo('已完成第 {} 回合之模型訓練...'.format(Round))
            Round += 1

            self.SaveRound(Round)

            if Round == self.QCThreshold:
                echo('即將進行品質檢查...')
                self.CheckQuality(Env, Model, MH, VH)

                self.QCThreshold += self.QCIncrement

            MH.PredictedOutput = []

            if self.CheckStop():
                for E in MH.RunEnv:
                    Model[E].save(
                        'Data/{}Model_{}'.format(self.UsrLottoType, E))
                    Env[E].close()
                echo('已停止運作')
                break


if __name__ == '__main__':
    pass
