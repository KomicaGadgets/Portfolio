import os
import re
import shutil
import sys
import time
from copy import deepcopy
from pathlib import Path
from pprint import pprint as echo

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from SharedMgr import F
from StatusBarMgr import StatusBarMgr


class PluginManipulator():
    def __init__(self, MainWindow: QtWidgets):
        self.MW = MainWindow
        self.StatusBarMgr = StatusBarMgr(self.MW)
        self.ErrorDialog = QMessageBox()

        self.FileName = {
            'Bundle': '',
            'Integration': '',
        }
        self.CodeReplace = {
            'PluginChName': '',
            'PluginDesc': '',
            'PluginShortName': '',
            'PluginShortNameUpper': '',
            'PluginShortNameLower': '',
            'PluginName_NoSpace': '',
            'PluginName_LowerNoSpace': '',
            'PluginName_Underline': '',
            'PluginName_UpperShortOrNoSpace': '',
            'PluginName_UpperShortOrUnderline': '',
            'PluginName_LowerShortOrUnderline': '',
            'PluginName_LowerShortOrLowerNoSpace': '',
        }

        self.ConfigPathForModify = ''

    def SetVar(self):
        PluginChName = self.MW.PluginChName.text().strip()
        PluginDesc = self.MW.PluginDesc.text().strip()
        PluginName = self.MW.PluginName.text().strip()
        PluginShortName = self.MW.PluginShortName.text().strip()
        PluginShortNameUpper = PluginShortName.upper()
        PluginShortNameLower = PluginShortName.lower()

        PluginName_NoSpace = self.MW.PluginName_NoSpace.text().strip()
        PluginName_LowerNoSpace = self.MW.PluginName_LowerNoSpace.text().strip()
        PluginName_Underline = self.MW.PluginName_Underline.text().strip()

        self.FileName = {
            'Bundle': f'{PluginName_NoSpace}Bundle',
            'Integration': f'{PluginShortNameUpper if PluginShortName else PluginName_NoSpace}Integration',
        }
        self.CodeReplace = {
            'PluginChName': PluginChName,
            'PluginDesc': PluginDesc,
            'PluginShortName': PluginShortName,
            'PluginShortNameUpper': PluginShortNameUpper,
            'PluginShortNameLower': PluginShortNameLower,
            'PluginName_NoSpace': PluginName_NoSpace,
            'PluginName_LowerNoSpace': PluginName_LowerNoSpace,
            'PluginName_Underline': PluginName_Underline,
            'PluginName_UpperShortOrNoSpace': PluginShortNameUpper if PluginShortName else PluginName_NoSpace,
            'PluginName_UpperShortOrUnderline': PluginShortNameUpper if PluginShortName else PluginName_Underline,
            'PluginName_LowerShortOrUnderline': PluginShortNameLower if PluginShortName else PluginName_Underline,
            'PluginName_LowerShortOrLowerNoSpace': PluginShortNameLower if PluginShortName else PluginName_LowerNoSpace,
        }

    def SetPath(self):
        F.MultiSet([
            ['OutputBundleDir',
                f'{F.OutputDir.AbsPath()}/{self.FileName.get("Bundle")}/'],
        ])

    def CheckEventListenerExist(self):
        EventListenerNameList = ['IsCampaignSub', 'IsEmailSub', 'IsLeadSub']
        Output = False

        for ChkBoxName in EventListenerNameList:
            Item = getattr(self.MW, ChkBoxName)

            if Item.isChecked():
                Output = True
                break

        return Output

    def ReplaceAndUpdateFile(self, File):
        File = File if isinstance(File, Path) else Path(File)

        Body = File.read_text('utf8')

        for key, value in self.CodeReplace.items():
            Body = Body.replace(f'{{*{key}*}}', value)

        File.write_text(Body, 'utf8')

    def ModifyConfigEventLink(self, SectionName: str, IsEnable: bool):
        ConfigPathObj = self.ConfigPathForModify if self.ConfigPathForModify else deepcopy(
            F.OutputBundleDir).Extend('Config/config.php').Path

        Body = ConfigPathObj.read_text(encoding='utf8')

        Regex = re.compile(
            f'<{SectionName}>(.*)<\/{SectionName}>', flags=re.MULTILINE | re.DOTALL)
        FullSection = Regex.search(Body)
        FullSection = FullSection.group(0)
        CodePart = Regex.findall(Body)[0]

        ReplacedContent = CodePart if IsEnable else ''

        Body = Body.replace(FullSection, ReplacedContent)

        ConfigPathObj.write_text(Body, 'utf8')

    def CopyBundleAndProcess(self):
        self.StatusBarMgr.set(text='正在檢查並清除外掛輸出資料夾...')
        if F.OutputBundleDir.Path.is_dir():
            shutil.rmtree(F.OutputBundleDir.AbsPath(), ignore_errors=True)
            time.sleep(1)

        self.StatusBarMgr.set(text='正在複製外掛樣版資料夾...')
        shutil.copytree(F.TplBundleDir.AbsPath(),
                        F.OutputBundleDir.AbsPath())

        self.StatusBarMgr.set(text='正在更新 TemplateBundle.php...')
        self.ReplaceAndUpdateFile(
            deepcopy(F.OutputBundleDir).Extend('TemplateBundle.php').Path
        )

        self.StatusBarMgr.set(text='正在重新命名 TemplateBundle.php...')
        os.chdir(F.OutputBundleDir.AbsPath())
        Path('TemplateBundle.php').rename(
            f'{self.FileName.get("Bundle")}.php'
        )

        self.StatusBarMgr.set(text='正在更新 TemplateIntegration.php...')
        self.ReplaceAndUpdateFile(
            deepcopy(F.OutputBundleDir).Extend(
                'Integration/TemplateIntegration.php').Path
        )

        self.StatusBarMgr.set(text='正在重新命名 TemplateIntegration.php...')
        os.chdir(f'{F.OutputBundleDir.AbsPath()}/Integration/')
        Path('TemplateIntegration.php').rename(
            f'{self.FileName.get("Integration")}.php'
        )

        self.StatusBarMgr.set(text='正在更新 messages.ini...')
        self.ReplaceAndUpdateFile(
            deepcopy(F.OutputBundleDir).Extend(
                'Translations/en_US/messages.ini').Path
        )

        self.StatusBarMgr.set(text='正在更新 config.php...')
        self.ReplaceAndUpdateFile(
            deepcopy(F.OutputBundleDir).Extend(
                'Config/config.php').Path
        )
        self.ModifyConfigEventLink(
            'FormService', self.MW.IsFormService.isChecked())
        self.ModifyConfigEventLink(
            'CampaignSub', self.MW.IsCampaignSub.isChecked())
        self.ModifyConfigEventLink(
            'EmailSub', self.MW.IsEmailSub.isChecked())
        self.ModifyConfigEventLink(
            'LeadSub', self.MW.IsLeadSub.isChecked())

        self.StatusBarMgr.set(text='正在更新 PublicController.php...')
        self.ReplaceAndUpdateFile(
            deepcopy(F.OutputBundleDir).Extend(
                'Controller/PublicController.php').Path
        )

        EventListenerDir = deepcopy(F.OutputBundleDir).Extend('EventListener')
        CampaignSubPath = deepcopy(EventListenerDir).Extend(
            'CampaignSubscriber.php').Path
        EmailSubPath = deepcopy(EventListenerDir).Extend(
            'EmailSubscriber.php').Path
        LeadSubPath = deepcopy(EventListenerDir).Extend(
            'LeadSubscriber.php').Path

        if self.MW.IsCampaignSub.isChecked():
            self.StatusBarMgr.set(text='正在更新 CampaignSubscriber.php...')
            self.ReplaceAndUpdateFile(CampaignSubPath)
        else:
            CampaignSubPath.unlink()

        if self.MW.IsEmailSub.isChecked():
            self.StatusBarMgr.set(text='正在更新 EmailSubscriber.php...')
            self.ReplaceAndUpdateFile(EmailSubPath)
        else:
            EmailSubPath.unlink()

        if self.MW.IsLeadSub.isChecked():
            self.StatusBarMgr.set(text='正在更新 LeadSubscriber.php...')
            self.ReplaceAndUpdateFile(LeadSubPath)
        else:
            LeadSubPath.unlink()

    def Generate(self):
        self.SetVar()
        self.SetPath()

        if self.CheckEventListenerExist():
            self.CopyBundleAndProcess()

            self.StatusBarMgr.setFlash(
                text='已更新並輸出新的外掛資料夾！關閉本視窗後方可移動外掛資料夾！', second=3)
        else:
            self.ErrorDialog.setIcon(QMessageBox.Critical)
            self.ErrorDialog.setText('請選取至少一個 EventListener！')
            self.ErrorDialog.setWindowTitle('錯誤')
            self.ErrorDialog.exec_()


if __name__ == '__main__':
    echo('請執行 Main.py，勿直接執行本檔。')
