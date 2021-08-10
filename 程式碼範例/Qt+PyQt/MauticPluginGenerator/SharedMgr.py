import os
import re
import sys
from pathlib import Path, PurePath
from pprint import pprint as echo

from Genesys.Core import Make

F = Make('FileMgr')

F.MultiSet([
    ['DataDir', './Data/'],
    ['OutputDir', './Output/']
])

F.MultiSet([
    ['TplBundleDir', f'{F.DataDir.AbsPath()}/TemplateBundle'],
])

F.MultiSet([
    ['TplBundleIntegrationDir', f'{F.TplBundleDir.AbsPath()}/Integration'],
])

F.MultiSet([
    ['TplBundlePluginBase', f'{F.TplBundleDir.AbsPath()}/TemplateBundle.php'],
    ['TplBundleIntegration',
        f'{F.TplBundleIntegrationDir.AbsPath()}/TemplateIntegration.php'],
])

if __name__ == '__main__':
    pass
