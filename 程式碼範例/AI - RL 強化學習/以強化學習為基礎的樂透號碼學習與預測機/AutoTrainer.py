import argparse
import json
import random
import select
import sys
import time
from pathlib import Path
from pprint import pprint as echo

from Genesys.InteractiveConsole import InteractiveConsole

if __name__ == '__main__':
    Pasr = argparse.ArgumentParser()
    Pasr.add_argument(
        "-s", "--Stop", nargs='?', const=True, help="Flag to stop train.")
    Pasr.add_argument(
        "-p", "--Pause", nargs='?', const=True, help="Flag to pause train. Sleep 10 seconds in one round.")
    Pasr.add_argument(
        "-r", "--Resume", nargs='?', const=True, help="Flag to resume train from pause.")
    UsrArg = Pasr.parse_args()

    IC = InteractiveConsole()

    UsrLottoType = IC.Ask('請輸入樂透彩類型？（1=大樂透，0=威力彩）')
    UsrLottoType = 'BigLotto' if IC.IsValidInput(
        UsrLottoType) else 'SuperLotto'

    FlagFiles = {
        'Stop': Path('.{}Stop'.format(UsrLottoType)),
        'Pause': Path('.{}Pause'.format(UsrLottoType))
    }

    if UsrArg.Stop:
        FlagFiles.get('Stop').touch()
        echo('已寫入停止命令')
        sys.exit()
    elif UsrArg.Pause:
        FlagFiles.get('Pause').touch()
        echo('已寫入暫停命令')
        sys.exit()
    elif UsrArg.Resume:
        if FlagFiles.get('Pause').is_file():
            FlagFiles.get('Pause').unlink()
            echo('已刪除暫停命令')
        sys.exit()

    from Env.BigLottoRL import ModelHelper, VisualizeHelper

    MH = ModelHelper()
    VH = VisualizeHelper()
    Env = {}
    Model = {}

    IsUseTrainedModel = bool(
        IC.AskInt('是否使用現有模型並繼續訓練？（1 = yes，0 或不輸入 = no）', 0))

    Round = 1

    HumanRestartIndex = IC.AskInt('請輸入要從第幾筆資料開始觀察＆訓練（0 或不輸入 = 從第 0+1 筆開始）：', 0)
    RestartIndex = (HumanRestartIndex -
                    1) if HumanRestartIndex > 0 else 0

    from AutoTrainer_Runner import AutoTrainer_Runner
    ATR = AutoTrainer_Runner(UsrLottoType, IsUseTrainedModel, RestartIndex)
    ATR.Run(Env, Model, MH, VH, Round)
