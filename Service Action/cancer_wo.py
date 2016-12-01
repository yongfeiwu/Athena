# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

"""此脚本仅仅用作撤销对应错误码的工单"""
connStr = 'crm/hdycrm_smart@10.18.128.37:1522/crm'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

"""错误码:'1033|Number threshold exceeded'"""
# 定义查询语句(需要明确是什么网元,什么时间类型,什么报错)
querySql = '''
select * from sa_wo_his t where t.check_in_comments = '1033|Number threshold exceeded' and t.state='D'
and t.ne_id = 2004 and t.event_type=500007
'''


result = curs.execute(querySql).fetchall()

for row in result:
    insertSql = '''
    insert into sa_wo_his
    select * from sa_wo t where t.check_in_comments = '1033|Number threshold exceeded' and t.state='D'
    and t.wo_id = %s
    '''%(row[0])
    print insertSql
    curs.execute(insertSql)
    conn.commit()

    updateSql = '''
    update order_item t set t.order_state='E' where t.order_item_id in(
    select so.order_item_id from sa_order so where so.order_id=%s
    )
    '''%(row[1])
    print updateSql
    curs.execute(updateSql)
    conn.commit()

    deleteSql = '''delete from sa_wo where wo_id = %s'''%(row[0])
    print deleteSql
    curs.execute(deleteSql)
    conn.commit()
curs.close()
conn.close()