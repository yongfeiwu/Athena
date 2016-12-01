# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import datetime

now = str(datetime.date.today()).replace('-', '')

connStr = 'crm/hdycrm_smart@10.18.128.37:1522/crm'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

create_9001_sql = '''
    create table tmp_user_not_exist_%s as
    select c.acc_nbr,t.wo_id
      from sa_wo t,sa_order b, order_item c
     where t.order_id=b.order_id
     and b.order_item_id = c.order_item_id
     and t.ne_id = 3001
       and t.state = 'D'
       and t.check_in_comments = '9001|The user does not exist'
''' % now

curs.execute(create_9001_sql)

update_sql = '''
    update sa_wo t
   set t.ne_id       = 1006,
       t.ws_id       = 1006,
       t.input_param = replace(t.input_param, '="2"', '="1"'),
       t.state       = 'A'
 where t.wo_id in (select a.wo_id from tmp_user_not_exist_%s a)
''' % now

curs.execute(update_sql)
conn.commit()

curs.close()
conn.close()

