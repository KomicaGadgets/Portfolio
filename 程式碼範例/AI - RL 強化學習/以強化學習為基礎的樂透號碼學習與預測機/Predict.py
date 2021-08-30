import asyncio
import collections
import json
import msvcrt
import random
import re
import select
import sys
import time
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
from stable_baselines.deepq.policies import CnnPolicy, LnMlpPolicy
from stable_baselines.deepq.policies import MlpPolicy as DQMlpPolicy

from DBMgr import DBMgr
from Genesys.InteractiveConsole import InteractiveConsole
from LotteryMatcher import LotteryMatcher


def IsTensoflowUsingGPU():
    import tensorflow as tf
    if tf.test.gpu_device_name():
        print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
    else:
        print("Please install GPU version of TF")
    exit()


if __name__ == '__main__':
    IC = InteractiveConsole()
    UsrLottoType = IC.AskStr('請輸入樂透彩類型？（1=大樂透，0=威力彩）',
                             'BigLotto', 'SuperLotto')
    IsUseCustomNum = False

    CustomNum = []

    if IsUseCustomNum:
        CustomNumNotReady = True

        while CustomNumNotReady:
            CustomNum = IC.Ask('請輸入中獎號碼：')
            CustomNum = re.findall(r"\d+", CustomNum)

            if len(CustomNum) != 7:
                echo('輸入的號碼分割後數量要是 7 個')
                echo('目前分割後的結果：{}'.format(','.join(CustomNum)))
            else:
                CustomNum = list(map(int, CustomNum))
                CustomNumNotReady = False

    PredictBatch = IC.AskInt('請輸入要一次預測幾組號碼？（0 或不輸入 = 10 組）', 10)

    from Env.BigLottoRL import (
            ModelHelper, BigLottoRL, BigLottoRL_Real, VisualizeHelper)

    MH = ModelHelper()
    VH = VisualizeHelper()
    Env = {}
    Model = {}

    MH.PredictedOutput = []

    for E in MH.RunEnv:
        E = E.replace('_LimitBudget', '')
        RealEnv = globals()['{}_Real'.format(E)]
        Env[E] = DummyVecEnv([lambda: RealEnv(CustomNum)])

        Algo = globals()[MH.ModelCfg[E]['algo']]
        Model[E] = Algo.load('Data/{}Model_{}'.format(UsrLottoType, E))
        Model[E].set_env(Env[E])
        VH.ViewResult(Model[E], Env[E], E, MH, CustomNum,
                      PredictBatch, IsReduceFromManyMode=False,
                      IsVerbose=(PredictBatch <= 10000))

        Env[E].close()
