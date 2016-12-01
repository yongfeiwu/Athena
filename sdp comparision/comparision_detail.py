# !/usr/bin/python
# -*- coding: utf-8 -*-

import cx_Oracle

import my_date

connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

sdp_sql = '''
select * from tmp_sdp_recharge_data
'''
sdp_list = curs.execute(sdp_sql).fetchall()

time_sql = '''
select distinct(substr(t.starttime,0,8)) from tmp_sdp_recharge_data t
'''
time_list = curs.execute(time_sql).fetchall()

times = []
for time in time_list:
    times.append(time[0])

min_time = min(times)
max_time = max(times)

total_ocs_sdp = []
for time in times:
    sdp_charge_sql = '''
    select sum(t.charge) from tmp_sdp_recharge_data t where substr(t.starttime,0,8)=%s
    ''' % (time)
    total_charge_sdp = curs.execute(sdp_charge_sql).fetchall()[0][0]

    sdp_count_sql = '''
     select count(1) from tmp_sdp_recharge_data t where substr(t.starttime,0,8)=%s
    ''' % (time)
    total_count_sdp = curs.execute(sdp_count_sql).fetchall()[0][0]

    ocs_charge_sql = '''
    select abs(sum(t.charge)) from (
    select * from acct_book@link_scc01
    union all
    select * from acct_book
    ) t where to_char(t.created_date,'yyyymmdd')=%s
    and t.part_id=%s
    and t.acct_res_id=1
    and t.acct_book_type='P'
    and t.contact_channel_id=19
    ''' % (time, my_date.getTodayMonth())
    total_charge_ocs = curs.execute(ocs_charge_sql).fetchall()[0][0]

    ocs_count_sql = '''
    select count(1) from (
    select * from acct_book@link_scc01
    union all
    select * from acct_book
    ) t where to_char(t.created_date,'yyyymmdd')=%s
    and t.part_id=%s
    and t.acct_res_id=1
    and t.acct_book_type='P'
    and t.contact_channel_id=19
    ''' % (time, my_date.getTodayMonth())
    total_count_ocs = curs.execute(ocs_count_sql).fetchall()[0][0]

    minus_count = total_count_sdp - total_count_ocs
    minus_charge = total_charge_sdp - total_charge_ocs

    tuple_v = (time, total_count_sdp, total_count_ocs, total_charge_sdp, total_charge_ocs, minus_charge, minus_count)
    print tuple_v
    total_ocs_sdp.append(tuple_v)

print total_ocs_sdp
curs.prepare(
    'insert into tmp_sdp_ocs_comparison(STARTTIME ,SDP_COUNTS,OCS_COUNTS,SDP_AMOUNT,OCS_AMOUNT,AMOUNT_MINUS,AMOUNT_COUNTS) values(:1, :2, :3, :4, :5, :6,:7)')
curs.executemany(None, total_ocs_sdp)

conn.commit()
print "=====================SDP对账总量对比操作完成====================="
# 关闭数据库连接
curs.close()
conn.close()