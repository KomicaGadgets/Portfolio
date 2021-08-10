# -*- coding: utf-8 -*-
import json
import os
import sys
import psutil
from multiprocessing import Process
from pprint import pprint as echo
from nsenter import Namespace

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import WifiMgr
import Reset

PCIndex = 2
DirPrefix = os.path.dirname(os.path.abspath(__file__))

IsWifi = 0
IsYoutube = 0
IsParallelAction = 1

def SetMyEnv():
    with open('PC{}/config.json'.format(PCIndex)) as json_file:
        pc_settings = json.load(json_file)

    my_env = {**os.environ.copy(), **pc_settings}
    return my_env

def WatchYoutube(YouTubeURL='LxPELW6CUFw'):
    # 模擬觀看 Youtube 影片(CLI)
    echo('正在播放 YouTube 影片...')
    os.system(
        'mpsyt set show_video true, set show_status true, set player vlc, set encoder 1, playurl https://www.youtube.com/watch?v={}, exit'.format(YouTubeURL))


def RunActionByFile(file, pgid):
    Cfg = WifiMgr.LoadWifiConfig(DirPrefix+'/config.json')
    with Namespace('/var/run/netns/%s'%Cfg['pc_nic'], 'net'):
        my_env = SetMyEnv()
        ext = os.path.splitext(file)[1]
        if(ext == '.sh'):
            P = psutil.Popen(file, shell=True, executable='/bin/bash', env=my_env)
        if(ext == '.py'):
            P = psutil.Popen(['python', file], shell=False, env=my_env)

def ParallelRunAction():
    os.setpgrp()
    pgid = os.getpgrp()
    Reset.SavePGID(PCIndex, pgid)

    with open(DirPrefix + '/ParallelActions.txt') as f:
        ActionList = f.read().splitlines()

    for file in ActionList:
        if file and file[:1] != '#':
            echo('正在執行 {}...'.format(file))
            P = Process(target=RunActionByFile, args=(file, pgid))
            P.start()

def RunAction():
    Cfg = WifiMgr.LoadWifiConfig(DirPrefix+'/config.json')

    # 觀看 YouTube 影片
    if bool(IsYoutube):
        WatchYoutube('LxPELW6CUFw')

    # 同步執行所有動作
    if bool(IsParallelAction):
        ParallelRunAction()


if __name__ == '__main__':
    RunAction()
