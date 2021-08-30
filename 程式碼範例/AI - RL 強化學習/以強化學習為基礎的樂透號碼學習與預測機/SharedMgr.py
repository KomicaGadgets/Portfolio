import os
import re
import sys
from pathlib import Path, PurePath
from pprint import pprint as echo

from Genesys.Core import Make


F = Make('FileMgr')

F.MultiSet([
    ['LottoDB', './Data/LottoHistory.db'],
    ['LastTrainSave', './Data/LastTrainSave.txt']
])

F.Set('QualityChecker', './QualityChecker.py', __file__)


if __name__ == '__main__':
    pass
