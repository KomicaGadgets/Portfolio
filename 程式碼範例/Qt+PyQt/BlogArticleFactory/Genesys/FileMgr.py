import os
import random
import re
import sys
import time
from pathlib import Path
from pprint import pprint as echo


class FileMap(object):
	def __init__(self, InputPath):
		self.RawPath = InputPath
		self.Path = self.MakeResolvedPath(InputPath)
		self._AbsPath = self.MakeAbsPath()

	def MakeResolvedPath(self, Input=''):
		return Path(Path(Input).resolve().absolute().as_posix())

	def MakeAbsPath(self):
		return self.Path.absolute().as_posix()

	def SetResolvedPath(self, Input):
		self.Path = self.MakeResolvedPath(Input)

	def SetAbsPath(self):
		self._AbsPath = self.MakeAbsPath()

	def AbsPath(self, ReCalc=0):
		if bool(ReCalc):
			self.SetAbsPath()

		return self._AbsPath

	def Extend(self, ExtPath=''):
		self.Path = self.Path / ExtPath
		self.SetResolvedPath(self.Path)
		self.AbsPath(1)
		return self

	def Safe(self):
		if not self.Path.exists():
			self.Path.touch()

		return self.Path

	def Read(self, mode='text'):
		return getattr(self.Path, 'read_'+mode)('utf8')

	def SafeRead(self, mode='text'):
		self.Safe()
		return self.Read(mode)

	def Write(self, body='', mode='text'):
		return getattr(self.Path, 'write_'+mode)(body)

	def SafeWrite(self, body='', mode='text'):
		self.Safe()
		return self.Write(body=body, mode=mode)

	def Open(self, mode: str = 'rb', encoding: str = 'utf8'):
		return getattr(self.Path, 'open')(mode=mode) if ('b' in mode) else getattr(self.Path, 'open')(mode=mode, encoding=encoding)

	def SafeOpen(self, mode: str = 'rb', encoding: str = 'utf8'):
		self.Safe()
		return self.Open(mode, encoding)

	def Del(self):
		if self.Path.exists():
			self.Path.unlink()

		return self.Path

	def MakeEmpty(self):
		if self.Path.exists():
			self.Path.unlink()

		self.Path.touch()

		return self.Path

	def Destroy(self):
		def GenerateSubstitutionList():
			List = list(range(0, 256))
			Seed = int(time.time())
			random.seed(Seed)
			random.shuffle(List)

			return List

		if self.Path.exists():
			SubsitutionList = GenerateSubstitutionList()

			with self.Open('rb+') as f:
				while True:
					Byte = f.read(1)
					if not Byte:
						break
					ByteInt = int.from_bytes(Byte, 'big')
					SubstituteInt = SubsitutionList[ByteInt]
					SubByte = SubstituteInt.to_bytes(1, 'big')
					# RandomInt = random.randint(0, 255)
					# SubByte = RandomInt.to_bytes(1, 'big')
					f.seek(-1, 1)
					f.write(SubByte)

			self.Path.unlink()


class Genesys_FileMgr(object):
	def __init__(self):
		self.RegisteredKeys = []

	def Set(self, key: str, path, pivot_path=None):
		if pivot_path:
			path = Path(pivot_path).parent/path

		setattr(self, key, FileMap(path))
		self.RegisteredKeys.append(key)

	def MultiSet(self, input: list = [], pivot_path=None):
		for item in input:
			self.Set(item[0], item[1], pivot_path)

	def ListKey(self):
		echo(self.RegisteredKeys)

	def MassDel(self, KeyList: list = []):
		for key in KeyList:
			getattr(getattr(self, key), 'Del')()


if __name__ == '__main__':
	C = Genesys_FileMgr()
	C.MultiSet([
		['A', './TPM.txt'],
		['B', '../TPM.txt'],
		['C', '../Sync']
	])

	A = C.C.AbsPath()
	R = C.C.Extend('../.././index.php').AbsPath()
	echo(A)
	echo(R)
