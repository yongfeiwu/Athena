# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import datetime

connStr = 'mrb/hdymrb_smart@10.18.128.32:1521/mrb'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()
now = str(datetime.date.today()).replace('-', '')

# tmp_drop_rb = '''
# drop table tmp_subscribers_%s
# ''' % now
# curs.execute(tmp_drop_rb)

tmp_rb_sql = '''
    create table tmp_subscribers_%s as(
SELECT distinct(t.subs_id),t2.offer_id
  FROM owe_event_charge t, prod@LINK_MASTERCC_NEW t2
 WHERE regexp_substr(t.attr_list, '975=[^\|]+', 1, 1, 'i') =
       '975=' || t2.prod_id   and t.state = 1

   and t2.prod_state = 'E'
   and t2.offer_id in (375,35)
union
SELECT distinct(t.subs_id),t2.offer_id
  FROM owe_event_charge t, prod@LINK_SLAVECC_NEW t2
 WHERE regexp_substr(t.attr_list, '975=[^\|]+', 1, 1, 'i') =
       '975=' || t2.prod_id
   and t.state = 1
   and t2.prod_state = 'E'
   and t2.offer_id in (375,35)
minus
SELECT distinct(t.subs_id),t2.offer_id
  FROM owe_event_charge t, prod@LINK_SLAVECC_NEW t2
 WHERE regexp_substr(t.attr_list, '975=[^\|]+', 1, 1, 'i') =
       '975=' || t2.prod_id
   and t.state = 0
   and t2.prod_state = 'E'
   and t2.offer_id in (375,35)
minus
SELECT distinct(t.subs_id),t2.offer_id
  FROM owe_event_charge t, prod@LINK_MASTERCC_NEW t2
 WHERE regexp_substr(t.attr_list, '975=[^\|]+', 1, 1, 'i') =
       '975=' || t2.prod_id
   and t.state = 0
   and t2.prod_state = 'E'
   and t2.offer_id in (375,35))
''' % now
curs.execute(tmp_rb_sql)
curs.close()
conn.close()
