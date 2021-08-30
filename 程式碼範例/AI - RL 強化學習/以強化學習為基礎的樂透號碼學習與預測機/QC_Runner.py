import asyncio
import json
import random
import re
import select
import sys
import time
from pprint import pprint as echo

import arrow
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

from Env.SuperLottoRL import (
    ModelHelper, SuperLottoRL, SuperLottoRL_LimitBudget, SuperLottoRL_Real, VisualizeHelper)
from Env.BigLottoRL import (
    ModelHelper, BigLottoRL, BigLottoRL_Real, VisualizeHelper)


class QC_Runner():
    def __init__(self, IsCLI, UsrLottoType, DatePK, InputNum, PrizeNum, PredictBatch):
        self.IsCLI = IsCLI
        self.UsrLottoType = UsrLottoType
        self.DatePK = DatePK
        self.InputNum = InputNum
        self.PrizeNum = PrizeNum
        self.PredictBatch = PredictBatch

    def Run(self, Env, Model, MH, VH):
        for E in MH.RunEnv:
            # E = E.replace('_LimitBudget', '')
            RealEnv = globals()['{}_Real'.format(E)]
            Env[E] = DummyVecEnv(
                [lambda: RealEnv(self.InputNum, self.PrizeNum)])

            Algo = globals()[MH.ModelCfg[E]['algo']]
            Model[E] = Algo.load('Data/{}Model_{}'.format(MH.LottoType, E))
            Model[E].set_env(Env[E])
            VH.ViewResult(Model[E], Env[E], E, MH,
                          self.DatePK, self.PredictBatch, IsVerbose=0 if self.IsCLI else 1, IsSaveProgress=0)

            Env[E].close()

        return MH, VH


if __name__ == '__main__':
    pass
