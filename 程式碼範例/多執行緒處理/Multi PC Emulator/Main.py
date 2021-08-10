import os
import sys
from multiprocessing import Process
from pprint import pprint as echo
from PC1 import PCaction_p1
from PC2 import PCaction_p2

def RunPCByIndex(key):
    # 根據模擬 PC 編號執行模擬 PC 動作
    SimuPC = 'PCaction_p{}'.format(key)

    echo('正在執行 PC{}'.format(key))
    getattr(getattr(sys.modules[__name__], SimuPC), "RunAction")()

def MultiThreadRun():
    # 多執行緒執行
    for i in range(8):
        P = Process(target=RunPCByIndex, args=(i+1,))
        P.start()


if __name__ == '__main__':
    MultiThreadRun()
