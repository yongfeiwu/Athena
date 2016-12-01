# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import csv

connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

query_sql = '''
select '95'||a.acc_nbr from subs a,prod b
where a.subs_id=b.prod_id
and b.prod_state='A'
and b.offer_id in(261)
union all
select '95'||a.acc_nbr from subs@link_slave_cc a,prod@link_slave_cc b
where a.subs_id=b.prod_id
and b.prod_state='A'
and b.offer_id in(261)
'''

printHeader = False
csv_file = "swe_post_subs.csv"
outputFile = open(csv_file, 'w')
output = csv.writer(outputFile, dialect='excel')

curs.execute(query_sql)
print "=============================starting============================="

for row_data in curs:
    output.writerow(row_data)

print "=============================finished============================="
outputFile.close()
curs.close()
conn.close()
