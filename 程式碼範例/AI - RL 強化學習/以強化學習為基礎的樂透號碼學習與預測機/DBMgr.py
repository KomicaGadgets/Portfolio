import json
import os
import re
import sqlite3
from pprint import pprint as echo
from shutil import copyfile

import arrow

from Genesys.Core import Make
from SharedMgr import F

# conn = sqlite3.connect(F.LottoDB.AbsPath())
# conn.row_factory = sqlite3.Row


class DBMgr():
    def __init__(self, LottoType='SuperLotto', RestartIndex=0, IsLoadDBProgress=0):
        self.conn = sqlite3.connect(F.LottoDB.AbsPath())
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.SQLClause = None
        self.SessionNo = None

        self.LottoType = LottoType

        self.RestartIndex = RestartIndex
        self.RowIndex = self.RestartIndex
        self.DBTblLen = 0
        self.TblKey = {}
        self.SelectField = ['num_{}'.format(i) for i in range(1, 8)]

        self.SQLClauseCfg = {
            'select': '*',
            'from': self.LottoType,
            'where': None,
            'orderBy': {
                'column': None,
                'order': None
            },
            'limit': None,
            'offset': None
        }

        self.DefineTblKey()

        if bool(IsLoadDBProgress):
            self.LoadDBProgress()

    def LoadDBProgress(self):
        if F.LastTrainSave.Path.exists():
            SaveData = json.loads(F.LastTrainSave.Read())
            self.SessionNo = SaveData.get('DatePK')
            self.RowIndex = SaveData.get('RowIndex')

    def InitSQL(self):
        self.SQLClauseCfg = {
            'select': '*',
            'from': self.LottoType,
            'where': None,
            'orderBy': {
                'column': None,
                'order': None
            },
            'limit': None,
            'offset': None
        }

        return self

    def GetSQL(self):
        self.SQLClause = 'SELECT {} FROM {}'.format(
            self.SQLClauseCfg.get('select', '*'),
            self.SQLClauseCfg.get('from')
        )

        Where = self.SQLClauseCfg.get('where')
        if Where:
            self.SQLClause += ' WHERE {}'.format(Where)

        OrderByCfg = self.SQLClauseCfg.get('orderBy')
        Column = OrderByCfg.get('column')
        Order = OrderByCfg.get('order')
        if Column and Order:
            self.SQLClause += ' ORDER BY {} {}'.format(Column, Order)

        Limit = self.SQLClauseCfg.get('limit')
        if Limit:
            self.SQLClause += ' LIMIT {}'.format(Limit)

        Offset = self.SQLClauseCfg.get('offset')
        if Offset:
            self.SQLClause += ' OFFSET {}'.format(Offset)

        return self.SQLClause

    def fetch(self, out_type='one'):
        SQLExecution = self.c.execute(self.GetSQL())
        return getattr(SQLExecution, 'fetch{}'.format(out_type))()

    def where(self, Column=None, Value=None, Operator='='):
        if Column and Value and Operator:
            self.SQLClauseCfg['where'] = '{} {} {}'.format(
                Column, Operator, Value)

        return self

    def orderBy(self, Column=None, Order=None):
        if Column and Order:
            self.SQLClauseCfg['orderBy'] = {
                'column': Column,
                'order': Order
            }

        return self

    def limit(self, Limit=None):
        if Limit:
            self.SQLClauseCfg['limit'] = Limit

        return self

    def offset(self, Offset=None):
        if Offset:
            self.SQLClauseCfg['offset'] = Offset

        return self

    def DefineTblKey(self):
        self.TblKey = {
            'SuperLotto': [
                'session_no',
                'date_y',
                'date_m',
                'date_d',
                'previous_sales_amount',
                'previous_commision',
                'num_1',
                'num_2',
                'num_3',
                'num_4',
                'num_5',
                'num_6',
                'num_7',
                'index_1',
                'index_2',
                'index_3',
                'index_4',
                'index_5',
                'index_6'
            ],
            'BigLotto': [
                'session_no',
                'date_y',
                'date_m',
                'date_d',
                'previous_sales_amount',
                'previous_commision',
                'num_1',
                'num_2',
                'num_3',
                'num_4',
                'num_5',
                'num_6',
                'num_7',
                'index_1',
                'index_2',
                'index_3',
                'index_4',
                'index_5',
                'index_6',
                'index_7'
            ],
            'Redeem': [
                'type',
                'description',
                'session_no',
                'date_y',
                'date_m',
                'date_d',
                'num_1',
                'num_2',
                'num_3',
                'num_4',
                'num_5',
                'num_6',
                'num_7'
            ]
        }

    def CheckDBTblLen(self):
        if self.DBTblLen == 0:
            self.DBTblLen = self.c.execute(
                'SELECT COUNT(*) as total FROM {}'.format(self.LottoType)).fetchone()[0]

    def CreateLottoTable(self, ForceCreate=0):
        FieldConfig = []

        for k in self.TblKey[self.LottoType]:
            if k == 'type':
                FieldConfig.append('%s TEXT DEFAULT "SuperLotto"' % k)
            else:
                FieldConfig.append('%s INTEGER DEFAULT 0' % k)

        if bool(ForceCreate):
            self.c.execute('DROP TABLE IF EXISTS %s' % self.LottoType)

        self.c.execute('CREATE TABLE IF NOT EXISTS {} (pk INTEGER NOT NULL PRIMARY KEY,{})'.format(
            self.LottoType, ','.join(FieldConfig)))
        self.conn.commit()

    def ImportSingleHistory(self, SingleCrawlerData):
        ImpData = []

        for key, val in SingleCrawlerData.items():
            ImpData.append(str(val))

        ImportVal = '({})'.format(','.join(ImpData))

        self.c.execute("INSERT OR IGNORE INTO {} VALUES {}".format(
            self.LottoType, ImportVal))
        self.conn.commit()

    def ExtractNumFromSQLObj(self, SQLObject):
        Output = []

        for k in self.SelectField:
            Output.append(SQLObject[k])

        return Output

    def SequentialHistoryNumber(self, IsAppendSalesInfo=0):
        self.CheckDBTblLen()
        self.InitSQL()

        if self.RowIndex > self.DBTblLen - 1 - 1:
            self.RowIndex = self.RestartIndex

        SQLObject = self.orderBy('pk', 'ASC').limit(
            1).offset(self.RowIndex).fetch()
        self.SessionNo = SQLObject['pk']
        Output = self.ExtractNumFromSQLObj(SQLObject)

        if bool(IsAppendSalesInfo):
            Output.append(SQLObject['previous_sales_amount'])
            Output.append(SQLObject['previous_commision'])

        self.RowIndex += 1

        return Output

    def NextHistoryNumber(self, IsAppendSalesInfo=0):
        self.CheckDBTblLen()
        self.InitSQL()

        NextRowIndex = self.RowIndex

        if NextRowIndex > self.DBTblLen - 1:
            NextRowIndex = self.RestartIndex

        SQLObject = self.orderBy('pk', 'ASC').limit(
            1).offset(NextRowIndex).fetch()
        self.SessionNo = SQLObject['pk']
        Output = self.ExtractNumFromSQLObj(SQLObject)

        if bool(IsAppendSalesInfo):
            Output.append(SQLObject['previous_sales_amount'])
            Output.append(SQLObject['previous_commision'])

        return Output

    def LatestHistoryNumber(self, IsAppendSalesInfo=0):
        self.InitSQL()

        SQLObject = self.orderBy('pk', 'DESC').limit(1).fetch()
        self.SessionNo = SQLObject['pk']
        Output = self.ExtractNumFromSQLObj(SQLObject)

        if bool(IsAppendSalesInfo):
            Output.append(SQLObject['previous_sales_amount'])
            Output.append(SQLObject['previous_commision'])

        return Output

    def RecallHistoryNumber(self, Nth=1, IsPureNum=1):
        self.InitSQL()

        SQLObject = self.orderBy('pk', 'DESC').limit(1).offset(Nth - 1).fetch()
        self.SessionNo = SQLObject['pk']
        Output = self.ExtractNumFromSQLObj(
            SQLObject) if bool(IsPureNum) else SQLObject

        return Output

    def SessionHistoryNumber(self, Session='1090731'):
        self.InitSQL()

        SQLObject = self.where('pk', Session).fetch()
        self.SessionNo = SQLObject['pk']
        Output = self.ExtractNumFromSQLObj(SQLObject)

        return Output


if __name__ == '__main__':
    C = DBMgr(LottoType='BigLotto')
    R = C.SessionHistoryNumber('1090501')
    echo(R)
