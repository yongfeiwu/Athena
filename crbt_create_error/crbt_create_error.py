# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

connStr = 'crm/hdycrm_smart@10.18.128.37:1522/crm'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()
# 删除临时表
dSql = '''
delete from tmp_wo_crbt
'''
curs.execute(dSql)
conn.commit()

# 把需要修改的数据插入到临时表,防止在处理这部分数据的时候出现变动
iSql = '''
    insert into tmp_wo_crbt
  select *
    from sa_wo a
   where a.check_in_comments like '9047|failed to chg'
     and a.event_type = 355001
     and a.state='D'
'''

curs.execute(iSql)
conn.commit()

# 将数据存到wo的备份表
i2Sql = '''
insert into sa_wo_bak
select * from tmp_wo_crbt
'''
curs.execute(i2Sql)
conn.commit()

# 删除wo当前表中的数据
d2Sql = '''
delete from sa_wo where wo_id in (select aa.wo_id from tmp_wo_crbt aa)
'''

curs.execute(d2Sql)
conn.commit()

# 修改订单表,以便继续订购
uSql = '''
update order_item t set t.order_state ='E' where t.order_item_id in(
select d.order_item_id from tmp_wo_crbt a,sa_node_inst b,sa_order c,order_item d
where a.node_inst_id=b.node_inst_id
and b.order_id=c.order_id
and c.order_item_id=d.order_item_id
and a.state='D'
and a.event_type=355001
and a.check_in_comments ='9047|failed to chg')
'''

curs.execute(uSql)
conn.commit()

curs.close()
conn.close()
