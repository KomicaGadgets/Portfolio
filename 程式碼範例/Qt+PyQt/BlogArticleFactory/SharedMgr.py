import os
import re
import sys
from pathlib import Path, PurePath
from pprint import pprint as echo

from Genesys.Core import Make
from Genesys.ToolBox import BlockIfNotSudo, _e, _v, _vs

F = Make('FileMgr')

F.Set('JSDir', './JS')
F.Set('DataDir', './Data')

F.MultiSet([
    ['InitSTT', '{}/InitSTT.js'.format(F.JSDir.AbsPath())],
    ['STTBackupFile', '{}/STTBackup.txt'.format(F.DataDir.AbsPath())],
    ['CNTWMapFile', '{}/CNTWMap.txt'.format(F.DataDir.AbsPath())]
])

if __name__ == '__main__':
    pass
