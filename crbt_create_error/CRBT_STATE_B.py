# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()
# 删除临时表


# 调用存储过程
curs.callproc('CRBT_STATE_B')

# 资源关闭
curs.close()
conn.close()
