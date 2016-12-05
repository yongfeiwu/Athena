# !/usr/bin/python
# coding: utf-8

import cx_Oracle

TABLE_NAME = 'tmp_wave'
# 查询客户给的列表中的总数
query_all_data = '''
select * from %s
''' % (TABLE_NAME)

# 查询acc_nbr信息
query_acc_nbr = '''
select count(*) from acc_nbr t where t.acc_nbr in (select acc_nbr from %s)
''' % (TABLE_NAME)

# 查询imsi信息
query_imsi = '''
select count(a.imsi) from sim_card a,%s b where a.imsi=b.imsi
''' % (TABLE_NAME)

# 查询iccid信息
query_iccid = '''
select count(a.iccid) from sim_card a,%s b where a.iccid=b.iccid
''' % (TABLE_NAME)

# 创建对比表
comparison_sql = '''
insert into  tmp_check_nbr_sim
select c.iccid,c.imsi,a.acc_nbr
  from acc_nbr a, sim_nbr b, sim_card c,WAVE_67 d
 where a.acc_nbr_id = b.acc_nbr_id
   and b.sim_card_id = c.sim_card_id
   and b.state = 'A' and a.acc_nbr=d.acc_nbr
'''

minus_sql = '''
    select count(1) from (
    select * from WAVE_67
    minus
    select * from check_nbr_sim_67)
    '''

minus_detail_sql = '''
select
a.acc_nbr wave_nbr,
b.acc_nbr db_nbr,
a.iccid wave_iccid,
b.iccid db_nbr,
a.imsi wave_imsi,
b.imsi db_imsi
from wave_67 a,check_nbr_sim_67 b
where a.acc_nbr=b.acc_nbr
and a.imsi<>b.imsi
union
select
a.acc_nbr wave_nbr,
b.acc_nbr db_nbr,
a.iccid wave_iccid,
b.iccid db_nbr,
a.imsi wave_imsi,
b.imsi db_imsi
from wave_67 a,check_nbr_sim_67 b
where a.acc_nbr=b.acc_nbr
and a.iccid<>b.iccid
'''
check_wholesale_discount_sql = '''select count(distinct a.acc_nbr_id)
  from wholesale_inst a, acc_nbr b, WAVE_67 c
 where a.acc_nbr_id = b.acc_nbr_id
   and b.acc_nbr = c.acc_nbr'''

check_wholesale_sql = '''
select count(a.acc_nbr_id)
  from wholesale_inst a, acc_nbr b, WAVE_67 c
 where a.acc_nbr_id = b.acc_nbr_id
   and b.acc_nbr = c.acc_nbr
'''


def check_main():
    check_flag = 0
    flag = 0
    try:
        conn = cx_Oracle.connect('crm/hdycrm_smart@10.18.128.37:1522/crm ')
        curs = conn.cursor()
        total_counts = len(curs.execute(query_all_data).fetchall())
        total_acc_counts = curs.execute(query_acc_nbr).fetchall()[0][0]
        total_imsi_counts = curs.execute(query_imsi).fetchall()[0][0]
        total_iccid_counts = curs.execute(query_iccid).fetchall()[0][0]
        if (total_counts <> total_acc_counts) or (total_counts <> total_imsi_counts) or (
                    total_counts <> total_iccid_counts):
            check_flag = 2
        print "*****************放号总数  :%s*****************" % (str(total_counts))
        print "*****************MSISDN统计:%s*****************" % (str(total_acc_counts))
        print "*****************IMSI  统计:%s*****************" % (str(total_imsi_counts))
        print "*****************ICCID 统计:%s*****************" % (str(total_iccid_counts))

        curs.execute('delete from tmp_check_nbr_sim')
        conn.commit
        curs.execute(comparison_sql)
        conn.commit()

        total_wholesale_discount_counts = curs.execute(check_wholesale_discount_sql).fetchall()[0][0]
        total_wholesale_count = curs.execute(check_wholesale_sql).fetchall()[0][0]

        if total_wholesale_discount_counts == total_wholesale_count:
            print "*****************wholesale无重复提交数据共:%s*****************" % (total_wholesale_count)
        else:
            check_flag = 1
            print "*****************wholesale存在重复提交数据共:%s*****************" % (
                total_wholesale_count - total_wholesale_discount_counts)

        minus_counts = curs.execute(minus_sql).fetchall()[0][0]
        print "*****************不平数 统计:%s*****************" % (minus_counts)
        print "*****************详细信息如下:*****************"

        if minus_counts > 0:
            result = curs.execute(minus_detail_sql).fetchall()
            for row in result:
                print row

    except Exception, e:
        flag = 1
        print "*****************异常:%s*****************" % (str(e))
    finally:
        curs.close()
        conn.close()
        if flag == 0:
            if check_flag == 0:
                print '*****************不需要校验数据OK*****************'
            elif check_flag == 1:
                print '*****************数据有问题:请验证wholesale表*****************'
            elif check_flag == 2:
                print '*****************数据有问题:请验证卡号表,具体脚本如下:*****************'
                print query_acc_nbr
                print query_imsi
                print query_iccid


def main():
    check_main()


if __name__ == "__main__":
    main()
