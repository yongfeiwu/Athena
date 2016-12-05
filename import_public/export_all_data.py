# !/usr/bin/python
# -*- coding: utf-8 -*-

import cx_Oracle
import csv

# 数据库的连接信息
connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

printHeader = False
csv_file = "all_data.csv"
outputFile = open(csv_file, 'w')
output = csv.writer(outputFile, dialect='excel')
select_sql = '''
select t.acc_nbr||'|'||-t.double_fee||'|0|1|'||'|' from tmp_wsc_refund_last t
'''
curs.execute(select_sql)
print "=============================starting============================="
if printHeader:
    cols = []
    for col in curs.description:
        cols.append(col[0])
    output.writerow(cols)

for row_data in curs:
    output.writerow(row_data)

print "=============================finished============================="
outputFile.close()
curs.close()
conn.close()
