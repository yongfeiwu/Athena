# !/usr/bin/python
# -*- coding: utf-8 -*-
import csv

import cx_Oracle

# 数据库的连接信息
connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

printHeader = True
csv_file = "bal_trans.csv"
outputFile = open(csv_file, 'w')
output = csv.writer(outputFile, dialect='excel')
select_sql = '''
 select out_acc_nbr,
        in_acc_nbr,
        created_date,
        decode(contact_channel_id, '', 'USSD', 1, 'CRM', 20, 'WSC')
   from tmp_bal_trans_1018_1117 A
  where to_char(created_date, 'yyyymmdd') <= '20161117'
  order by A.CREATED_DATE

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
