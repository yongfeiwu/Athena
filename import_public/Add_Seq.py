# !/usr/bin/python
# -*- coding: utf-8 -*-

import cx_Oracle

# 数据库的连接信息
connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

querySql = '''
select a.acc_nbr,a.double_fee,a.subs_id,a.advice_type from tmp_pre_ad_data_NOT_B_NEW a
'''

result = curs.execute(querySql)
count = 0
param = []
for row in result:
    count = count + 1
    tuple = (int(count), row[0], row[1], row[2], row[3])
    param.append(tuple)
print param
curs.prepare(
    'insert into tmp_pre_ad_data_lastest(seq_id ,acc_nbr,double_fee,subs_id,advice_type) values(:1, :2, :3, :4, :5)')
curs.executemany(None, param)
conn.commit()
print "===================finished==================="
curs.close()
conn.close()
