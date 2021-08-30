import argparse
import json
import os
import re
import shutil
import sys
import time
from argparse import RawTextHelpFormatter
from pathlib import Path, PurePath
from pprint import pprint as echo


class InteractiveConsole:
    def __init__(self):
        pass

    def IsValidInput(self, Input):
        Output = 1 if bool(Input) and Input != '0' else 0
        return bool(Output)

    def Ask(self, Msg):
        return input(Msg)

    def AskStr(self, Msg, Success='OK', Error='Error'):
        Output = Success if self.IsValidInput(self.Ask(Msg)) else Error
        return Output

    def AskBool(self, Msg):
        return self.IsValidInput(self.Ask(Msg))

    def AskInt(self, Msg, Default=0):
        Response = self.Ask(Msg)
        Output = int(Response) if self.IsValidInput(Response) else Default
        return Output

    def AskInList(self, Msg, List=[]):
        Response = self.Ask(Msg)
        return Response if Response in List else False


if __name__ == '__main__':
    pass
