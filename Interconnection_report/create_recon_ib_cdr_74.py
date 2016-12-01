# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

# 数据库的连接信息
connStr = 'sett/sett@10.18.129.67:1521/sett'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

exeSql = '''
CREATE  table RECON_IB_CDR_74_MIG as
SELECT A.START_TIME START_TIME,
A.DURATION DURATION,
DECODE(SUBSTR(A.CALLING_NBR, 1, 1),
'0',
'95' || SUBSTR(A.CALLING_NBR, 2, 99),
'9',
DECODE(SUBSTR(A.CALLING_NBR, 1, 3),
'959',
A.CALLING_NBR,
'95' || A.CALLING_NBR),
'95' || A.CALLING_NBR) ORG_NUM,
DECODE(SUBSTR(A.CALLED_NBR, 1, 1),
'0',
'95' || SUBSTR(A.CALLED_NBR, 2, 99),
'9',
DECODE(SUBSTR(A.CALLED_NBR, 1, 3),
'959',
A.CALLED_NBR,
'95' || A.CALLED_NBR),
'95' || A.CALLED_NBR) TERM_NUM,
A.RE_ID REID
FROM IB_CDR_74_MIG A
'''
print exeSql

curs.execute(exeSql)

print "==========================create recon_ib_cdr_74_mig finished=========================="
curs.close()
conn.close()
