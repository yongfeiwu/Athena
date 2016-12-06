# !/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ = '吴永飞'
# __assessor__ = '余安进'
# __createDate__ = '2016/12/2'
# 此脚本处理crbt和ota的工单，如果crbt单子大于3000，启动清理，ota单子大于1000，启动清理
import cx_Oracle

# 数据库的连接信息
connStr = 'crm/hdycrm_smart@10.18.128.37:1522/crm'
# connStr = 'tb_crm/smart@10.18.137.14:1521/MCC'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

# 定义清空临时表语句
clear_tmp_table_sql = '''
delete from tmp_sa_wo_crbt_ota
'''

# 确保每次临时表中都没有数据
curs.execute(clear_tmp_table_sql)
conn.commit()

# 定义查询ota数目的sql
query_sql_ota = '''
select count(1) from sa_wo t where t.ne_id=1002 and t.state='D'
'''
amount_ota = curs.execute(query_sql_ota).fetchall()[0][0]
print amount_ota

# 定义查询crbt数目的sql
query_sql_crbt = '''
  select count(1)
    from sa_wo a
   where a.check_in_comments like '9047|failed to chg'
     and a.event_type = 355001
     and a.state='D'
'''
amount_crbt = curs.execute(query_sql_crbt).fetchall()[0][0]
print amount_crbt

# 定义插入临时表crbt的数据，防止在处理这部分数据的时候出现变动
i_crbt_sql = '''
    insert into tmp_sa_wo_crbt_ota
  select *
    from sa_wo a
   where a.check_in_comments like '9047|failed to chg'
     and a.event_type = 355001
     and a.state='D'
'''
# 定义插入临时表ota的数据，防止在处理这部分数据的时候出现变动
i_ota_sql ='''
insert into tmp_sa_wo_crbt_ota
select * from sa_wo t where t.ne_id=1002 and t.state='D'
'''

# 定义修改订单语句
u_order_item_sql = '''
update order_item t set t.order_state ='E' where t.order_item_id in(
    select distinct(b.order_item_id) from tmp_sa_wo_crbt_ota a,sa_order b
    where a.order_id=b.order_id
    )
'''

if amount_crbt >= 3000:
    # 插入临时表
    curs.execute(i_crbt_sql)
    conn.commit()
    curs.execute('insert into sa_wo_bak select * from tmp_sa_wo_crbt_ota')
    conn.commit()
    curs.execute('delete from sa_wo where wo_id in (select aa.wo_id from tmp_sa_wo_crbt_ota aa)')
    conn.commit()
    curs.execute(u_order_item_sql)
    conn.commit()
    curs.execute(clear_tmp_table_sql)
    conn.commit()
if amount_ota >= 1000:
    curs.execute(i_ota_sql)
    conn.commit()
    curs.execute('insert into sa_wo_bak select * from tmp_sa_wo_crbt_ota')
    conn.commit()
    curs.execute('delete from sa_wo where wo_id in (select aa.wo_id from tmp_sa_wo_crbt_ota aa)')
    conn.commit()
    curs.execute(clear_tmp_table_sql)
    conn.commit()

print "==========================script finished =========================="
curs.close()
conn.close()
