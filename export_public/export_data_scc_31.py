# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

# 数据库的连接信息
connStr = 'mrb/hdymrb_smart@10.18.128.32:1521/mrb'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

allItemSQL = '''
    select t.acct_item_type_id from acct_item_type@link_master_cc t where t.acct_res_id=1
    '''
resultlist = curs.execute(allItemSQL).fetchall()
tempList = []
for row in resultlist:
    print type(row[0])
    tempList.append(row[0])
print ("=======================================================================================")

# 查询所有rg100记录语句
recordSQL = '''
select /*+PARALLEL(a,8)*/
 a.billing_nbr,
 a.acct_item_type_id1,
 a.acct_item_type_id2,
 a.acct_item_type_id3,
 a.acct_item_type_id4,
 a.acct_item_type_id5,
 a.acct_item_type_id6,
 a.acct_item_type_id7,
 a.acct_item_type_id8,
 a.acct_item_type_id9,
 a.charge1,
 a.charge2,
 a.charge3,
 a.charge4,
 a.charge5,
 a.charge6,
 a.charge7,
 a.charge8,
 a.charge9,
 a.start_time,
 a.event_inst_id
  FROM EVENT_USAGE_C_275@link_slave_rb a
 where a.re_id = 1174
 and a.part_id >15
 and a.part_id <=31
and to_char(a.start_time,'yyyymm')= '201610'
'''
# print recordSQL
recordList = curs.execute(recordSQL).fetchall()

# 将所有charge的值加起来
finalList = []
for row in recordList:
    charge = 0
    for i in range(1, 10):
        if int(row[i]) in tempList:
            charge += (int(row[9+i]) == -1 and 0 or int(row[9+i]))
    oneRow = (row[0], str(charge), str(row[19]), row[20])
    # print oneRow
    finalList.append(oneRow)
print len(finalList)
# 插入临时表
curs.prepare('insert into tmp_rg100_data values(:1, :2, :3, :4)')
curs.executemany(None, finalList)
conn.commit()
print "==========================finished=========================="
curs.close()
conn.close()
