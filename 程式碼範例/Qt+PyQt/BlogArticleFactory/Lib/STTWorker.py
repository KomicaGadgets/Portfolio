import os
import sys
import time
from pprint import pprint as echo

import speech_recognition as sr
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread
from SharedMgr import F
from StatusBarMgr import StatusBarMgr

from .SpeechConverter import SpeechConverter


class STTWorker(QThread):
    def __init__(self, MainWindow: QtWidgets, StatusBarMgr: StatusBarMgr, STT, ThreadCounter):
        super(STTWorker, self).__init__()
        self.MW = MainWindow
        self.StatusBarMgr = StatusBarMgr
        self.SpeechConverter = SpeechConverter()
        self.STT = STT
        self.ThreadCounter = ThreadCounter

        self.Recognizer = None

        self.quit_flag = False

    def ReconizeSpeech(self, audio):
        if audio:
            self.StatusBarMgr.set('正在辨識語音內容...')

            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                RecText = self.Recognizer.recognize_google(
                    audio, language='zh-TW')
                ProcessedRecText = self.SpeechConverter.FormatText(RecText)
                ProcessedRecText = self.SpeechConverter.TextToCmd(
                    ProcessedRecText)
                self.MW.STTTextArea.textCursor().insertText(ProcessedRecText)
                self.StatusBarMgr.set('語音辨識中，請開始說話...')
            except sr.UnknownValueError:
                StausText = 'Google 語音辨識無法了解你的語音內容。'
                print(StausText)
                self.StatusBarMgr.setFlash(text=StausText, second=1)
            except sr.RequestError as e:
                print(
                    "Could not request results from Google Speech Recognition service; {0}".format(e))

            self.AutoBackup()

    def AutoBackup(self):
        F.STTBackupFile.Write(self.MW.STTTextArea.toPlainText())

    def run(self):
        self.Recognizer = sr.Recognizer()
        # self.Recognizer.energy_threshold = 3000

        while True:
            if not self.quit_flag:
                with sr.Microphone() as source:
                    self.Recognizer.adjust_for_ambient_noise(
                        source,
                        duration=2
                    )

                    try:
                        audio = self.Recognizer.listen(
                            source, timeout=None, phrase_time_limit=5)
                    except:
                        pass

                if self.ThreadCounter >= self.STT.STTThreadCounter:
                    self.ReconizeSpeech(audio)
            else:
                break

        self.quit()
        self.wait()


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
