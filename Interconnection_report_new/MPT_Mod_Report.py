# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

# 数据库的连接信息
connStr = 'rb/smart123@10.18.137.32:1521/rb'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

exeSql = '''
create table tmp_mpt_mod_report as
SELECT PK.PK_STIME,
       NVL(PK.PK_DUR, 0) "Peak Actual Duration",
       NVL(OP.OP_DUR, 0) "Off-Peak Actual Duration"
from
(select TRUNC(t.START_TIME) PK_STIME,
               SUM(t.DURATION) PK_DUR
from event_usage_193 t
where t.re_id=1128
and SUBSTR(TO_CHAR(t.start_time, 'yyyymmddhh24miss'), 9, 2) BETWEEN '08' AND '17'
and substr(t.called_nbr,0,4)='9593'
and substr(t.called_nbr,0,5)='95939'
GROUP BY TRUNC(t.START_TIME)) pk

LEFT JOIN (SELECT TRUNC(tt.START_TIME) OP_SDATE,
                    SUM(tt.DURATION) OP_DUR
             /*+parallel(m, 8) */
               FROM event_usage_193 tt
              WHERE SUBSTR(TO_CHAR(tt.START_TIME, 'yyyymmddhh24miss'), 9, 2) NOT BETWEEN '08' AND '17'
                and substr(tt.called_nbr, 0, 5) = '95939'
                and substr(tt.called_nbr, 0, 4) = '9593'
                AND tt.re_id =1128
              GROUP BY TRUNC(tt.START_TIME)) OP
    ON PK.PK_STIME = OP.OP_SDATE

'''
print exeSql

curs.execute(exeSql)

print "==========================tmp_mpt_mod_report finished =========================="
curs.close()
conn.close()
