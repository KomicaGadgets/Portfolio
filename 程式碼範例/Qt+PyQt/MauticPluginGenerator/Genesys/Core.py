import os
import sys
from pathlib import Path
from pprint import pprint as echo

from .FileMgr import Genesys_FileMgr
from .InteractiveConsole import Genesys_InteractiveConsole

MakeKeyMap = {
    'FileMgr': 'Genesys_FileMgr',
    'InteractiveConsole': 'Genesys_InteractiveConsole',
}


def Make(ClassKey: str = 'FileMgr', Config: dict = {}):
    ClassName = MakeKeyMap.get(ClassKey)

    Class = getattr(sys.modules[__name__], ClassName)(**Config)

    return Class


if __name__ == '__main__':
    R = Make('InteractiveConsole')
    N = R.AskInt('輸入數字：', 20)
    echo(N)
