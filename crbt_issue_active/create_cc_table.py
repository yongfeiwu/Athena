# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import datetime
now = str(datetime.date.today()).replace('-', '')


connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()
# tmp_drop_cc = '''
# drop table tmp_crbt_active_issue_%s
# ''' % now
# curs.execute(tmp_drop_cc)

tmp_cc_sql = '''
create table tmp_crbt_active_issue_%s as(
select b.acc_nbr,e.imsi,a.offer_id from
 tmp_subscribers_%s@link_mrb a,subs b,acc_nbr c,sim_nbr d,sim_card e
 where a.subs_id=b.subs_id
 and b.acc_nbr= c.acc_nbr
 and c.acc_nbr_id=d.acc_nbr_id
 and d.sim_card_id=e.sim_card_id
 and d.state='A'
 union
 select b.acc_nbr,e.imsi,a.offer_id from
 tmp_subscribers_%s@link_mrb a,subs@link_scc01 b,acc_nbr c,sim_nbr d,sim_card e
 where a.subs_id=b.subs_id
 and b.acc_nbr= c.acc_nbr
 and c.acc_nbr_id=d.acc_nbr_id
 and d.sim_card_id=e.sim_card_id
 and d.state='A')
''' % (now, now, now)
curs.execute(tmp_cc_sql)



curs.close()
conn.close()


