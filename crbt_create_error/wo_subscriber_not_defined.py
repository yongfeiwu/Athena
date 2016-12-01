# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import datetime

now = str(datetime.date.today()).replace('-', '')

connStr = 'crm/hdycrm_smart@10.18.128.37:1522/crm'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

# 更新3001的订单状态
update_3001_sql = '''
update order_item t set t.order_state='E' where t.order_item_id in(
select b.order_item_id
      from sa_wo t,sa_order b, order_item c
     where t.order_id=b.order_id
     and b.order_item_id = c.order_item_id
       and t.state = 'D'
       and t.check_in_comments = '3001|Subscriber not defined')
'''

curs.execute(update_3001_sql)

# 将数据移到wo备份表
insert_sa_wo_bak = '''
insert into sa_wo_bak
select * from sa_wo  t
where t.state = 'D'
and t.check_in_comments = '3001|Subscriber not defined'
'''
curs.execute(insert_sa_wo_bak)

# 将sa表中数据清掉
delete_sa_wo_sql = '''
delete from sa_wo t where t.state = 'D'
and t.check_in_comments = '3001|Subscriber not defined'
'''

curs.execute(delete_sa_wo_sql)
conn.commit()
curs.close()
conn.close()
