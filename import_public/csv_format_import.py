# !/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ = 'Wuyongfei'
# __assessor__ = ''
# __createDate__ = '2016/12/5'
import cx_Oracle
import sys
import os

# 获取文件中的行
def getFileDataList(filename):
    fileHandle = open(filename, 'r')
    recordList = fileHandle.readlines()
    return recordList

#  插表
def insertRecords(connStr, tablename, param):
    conn = cx_Oracle.connect(connStr)
    curs = conn.cursor()
    # 自行修改列明
    insert_sql = '''
    insert into %s(
     PASSWORD,
     USERID,
     CARDTYPE,
     STATE,
     LOCKED,
     FEETOTAL,
     ADDDAYS,
     EXPIREDATE,
     CARDNUM,
     CALLING,
     OPERMODE,
     USERSCPID,
     TRANSACTION_ID,
     VENDORID,
     CELLID )
    values
    (:1, :2, :3,:4,:5,:6,:7,:8,:9,:10,:11,:12,:13,:14,:15)
    ''' % (tablename)
    curs.prepare(insert_sql)
    curs.executemany(None, param)
    conn.commit()
    curs.close()
    conn.close()


def processRecords(records):
    param = []
    for row in records:
        tmp_list = str(row).split(',')
        tuple_value = (tmp_list[0].replace('\"', ''), tmp_list[1].replace('\"', ''),
                       tmp_list[2].replace('\"', ''), tmp_list[3].replace('\"', ''),
                       tmp_list[4].replace('\"', ''), tmp_list[5].replace('\"', ''),
                       tmp_list[6].replace('\"', ''), tmp_list[7].replace('\"', ''),
                       tmp_list[8].replace('\"', ''), tmp_list[9].replace('\"', ''),
                       tmp_list[10].replace('\"', ''), tmp_list[11].replace('\"', ''),
                       tmp_list[12].replace('\"', ''), tmp_list[13].replace('\"', ''),
                       tmp_list[14].replace('\"', '').replace('\r', '').replace('\n', '')
                       )
        param.append(tuple_value)

    return param


def main():
    records = getFileDataList('VCrecorde2.csv')
    param = processRecords(records)
    insertRecords('mcc/hdymcc_smart@10.18.128.31:1521/mcc', 'tmp_vc_recharge_data', param)


if __name__ == "__main__":
    main()
