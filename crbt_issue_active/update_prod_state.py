# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import datetime

now = str(datetime.date.today()).replace('-', '')

connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()
tmp_update1_sql = '''
    update prod t
    set t.prod_state = 'A'
    where t.prod_id in (select b.prod_id
                       FROM subs a, prod b, tmp_crbt_active_issue_%s c
                      where a.subs_id = b.indep_prod_id
                        and a.acc_nbr = c.acc_nbr
                        and b.offer_id in (35, 375)
                        and b.prod_state = 'E')''' % now

tmp_update2_sql = '''
     update prod@link_scc01 t
     set t.prod_state = 'A'
     where t.prod_id in (select b.prod_id
                        FROM subs@link_scc01                a,
                             prod@link_scc01                b,
                             tmp_crbt_active_issue_%s c
                       where a.subs_id = b.indep_prod_id
                         and a.acc_nbr = c.acc_nbr
                         and b.offer_id in (35, 375)
                         and b.prod_state = 'E')''' % now
curs.execute(tmp_update1_sql)
curs.execute(tmp_update2_sql)
conn.commit()
curs.close()
conn.close()
