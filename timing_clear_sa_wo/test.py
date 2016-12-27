# !/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ = 'Wuyongfei'
# __assessor__ = ''
# __createDate__ = '2016/12/5'
import cx_Oracle

conn = cx_Oracle.connect('crm/hdycrm_smart@10.18.128.37:1522/crm')
curs = conn.cursor()

dict1 = dict(curs.execute('select * from sa_wo_script_bak').fetchall())
print dict1