# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import csv

connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()


tmp_cc_sql = '''
create table tmp_ota_data as(
select c.acc_nbr,e.imsi,e.iccid from
 subs a, prod b,acc_nbr c,sim_nbr d,sim_card e
 where a.subs_id = b.prod_id
 and b.prod_state in('A','D','E')
 and a.acc_nbr=c.acc_nbr
 and c.acc_nbr_id=d.acc_nbr_id
 and d.state='A'
 and d.sim_card_id=e.sim_card_id
 union
select c.acc_nbr,e.imsi,e.iccid from
 subs@link_scc01 a, prod@link_scc01 b,acc_nbr c,sim_nbr d,sim_card e
 where a.subs_id = b.prod_id
 and b.prod_state in('A','D','E')
 and a.acc_nbr=c.acc_nbr
 and c.acc_nbr_id=d.acc_nbr_id
 and d.state='A'
 and d.sim_card_id=e.sim_card_id)
'''
curs.execute(tmp_cc_sql)


printHeader = True
csv_file = "ota_data.csv"
outputFile = open(csv_file, 'w')
output = csv.writer(outputFile, dialect='excel')
select_sql = '''
 select t.* from tmp_ota_data t
'''
curs = conn.cursor()
curs.execute(select_sql)
if printHeader:
    cols = []
    for col in curs.description:
        cols.append(col[0])
    output.writerow(cols)

for row_data in curs:
    output.writerow(row_data)



outputFile.close()
curs.close()
conn.close()
