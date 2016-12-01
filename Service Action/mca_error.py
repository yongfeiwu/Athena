# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

connStr = 'crm/hdycrm_smart@10.18.128.37:1522/crm'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

# for '4|Unknown error' this error
U1sql = '''
    update sa_wo t set t.state='C' where t.wo_id in(
select a.wo_id
    from sa_wo a
   where a.check_in_comments like '4|Unknown error'
     and a.event_type = 254002
     and a.state='D'
)
'''

curs.execute(U1sql)
conn.commit()
u2sql = '''
update sa_wo t
   set t.state = 'C'
 where t.wo_id in
       (select a.wo_id
          from sa_wo a
         where a.check_in_comments = '3|wrong format of user number'
           and a.event_type = 254001)
'''
curs.execute(u2sql)
conn.commit()

curs.close()
conn.close()
