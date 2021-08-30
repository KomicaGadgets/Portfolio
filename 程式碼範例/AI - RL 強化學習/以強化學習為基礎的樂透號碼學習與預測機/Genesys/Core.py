import os
import sys
from pathlib import Path
from pprint import pprint as echo

from .FileMgr import Genesys_FileMgr

MakeKeyMap = {
    'FileMgr': 'Genesys_FileMgr',
}


def Make(ClassKey: str = 'FileMgr', Config: dict = {}):
    ClassName = MakeKeyMap.get(ClassKey)

    Class = getattr(sys.modules[__name__], ClassName)(**Config)

    return Class


if __name__ == '__main__':
    R = Make('FileMgr')
    R.ListKey()
