# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import datetime

now = str(datetime.date.today()).replace('-', '')
print now
connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

# 创建临时表
tmp_sql = '''
create table tmp_special_group_%s as
select b.*
  from prod a, SUBS_SPECIAL_GROUP b
 where a.prod_state = 'E'
   and a.block_reason = '00000020000000'
   and a.prod_id = b.subs_id and to_char(b.created_date,'yyyymmdd')<= %s
   union all
   select  b.*
  from prod@link_scc01 a, SUBS_SPECIAL_GROUP b
 where a.prod_state = 'E'
   and a.block_reason = '00000020000000'
   and a.prod_id = b.subs_id and to_char(b.created_date,'yyyymmdd')<= %s
''' % (now, now, now)

curs.execute(tmp_sql)

# 删除黑名单表数据
del_black_sql = '''
delete from subs_special_group t where t.subs_special_group_id in(select aa.subs_special_group_id from tmp_special_group_%s aa)
''' % (now)
curs.execute(del_black_sql)

# 修改产品状态master
update_masterp_sql = '''
update prod t
   set t.block_reason = '00000000000000', t.prod_state = 'A'
 where t.indep_prod_id is null
   and t.prod_state='E'
   and t.prod_id in (select tt.subs_id from tmp_special_group_%s tt)
''' % (now)
curs.execute(update_masterp_sql)

# 修改产品状态slaver
update_slaverp_sql = '''
update prod@link_scc01 t
   set t.block_reason = '00000000000000', t.prod_state = 'A'
 where t.indep_prod_id is null
   and t.prod_state='E'
   and t.prod_id in (select tt.subs_id from tmp_special_group_%s tt)
''' % (now)
curs.execute(update_slaverp_sql)

# 删除累积量master
del_mastera_sql = '''
delete from subs_special_group t
 where t.subs_special_group_id in
       (select aa.subs_special_group_id from tmp_special_group_%s aa)
''' % (now)
curs.execute(del_mastera_sql)

# 删除累积量slaver
del_slavera_sql = '''
delete from special_cust_accumulate@link_scc01 t
 where t.subs_id in (select tt.subs_id from tmp_special_group_%s tt)
''' % (now)
curs.execute(del_slavera_sql)

conn.commit()

# 资源关闭
curs.close()
conn.close()
