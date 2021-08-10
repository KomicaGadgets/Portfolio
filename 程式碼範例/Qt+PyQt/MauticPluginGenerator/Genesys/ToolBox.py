import os
import shlex
import subprocess
import sys
from os import system as _s
from pathlib import Path
from pprint import pprint as echo

import pkg_resources


def YesNoPrompt(question)->bool:
	ErrorAnsFlag = False

	while "the answer is invalid":
		if ErrorAnsFlag:
			echo('輸入的回答格式錯誤，請重新輸入。')

		reply = str(input(question+' [y/n]：')).lower().strip()
		if reply[:1] == 'y':
			return True
		if reply[:1] == 'n':
			return False

		ErrorAnsFlag = True


def _e(Cmd):
	echo(Cmd)
	_s(Cmd)


def _v(Cmd):
	FormattedCmd = shlex.split(Cmd)
	echo(FormattedCmd)
	return subprocess.run(FormattedCmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True).stdout


def _vs(Cmd):
	return _v(Cmd).rstrip('\n')


def GetRuntimeUsr():
	return _vs('whoami')


def CheckSudo()->bool:
	return False if GetRuntimeUsr() != 'root' else True


def BlockIfNotSudo():
	if not CheckSudo():
		sys.exit('Need root privilege or using sudo!!!')

def ListInstalledModule():
	return [pkg.key for pkg in pkg_resources.working_set]


if __name__ == '__main__':
	BlockIfNotSudo()

	echo('AAA')
