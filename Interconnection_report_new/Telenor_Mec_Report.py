# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

# 数据库的连接信息
connStr = 'rb/smart123@10.18.137.32:1521/rb'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

exeSql = '''
create table tmp_telenor_mec_report as
SELECT PK.PK_STIME,
NVL(PK.PK_DUR, 0) "Peak Actual Duration",
NVL(OP.OP_DUR, 0) "Off-Peak Actual Duration",
NVL(SMS.SMS_CNT, 0) "No of SMS"
FROM (SELECT TRUNC(M.START_TIME) PK_STIME,
SUM(M.DURATION) PK_DUR,
ceil(sum(M.DURATION) / 6) PK_UNIT
/*+parallel(m, 8) */
FROM RECON_IB_CDR_67 M
WHERE SUBSTR(TO_CHAR(M.START_TIME, 'yyyymmddhh24miss'), 9, 2) BETWEEN '08' AND '17'
AND SUBSTR(M.ORG_NUM, 0, 5) in
('95979', '95978', '95977' ,'95976')  and (substr(m.term_num,0,5) in ('95930','95931','95932','95933','95934','95936') or substr(m.term_num,0,6) in ('959340','959346','959349'))
and substr(m.term_num,0,6)<>'959593'
AND M.REID BETWEEN 1249 AND 1252
GROUP BY TRUNC(M.START_TIME)) PK
LEFT JOIN (SELECT TRUNC(M.START_TIME) OP_SDATE,
SUM(M.DURATION) OP_DUR,
ceil(sum(M.DURATION) / 6) OP_UNIT
/*+parallel(m, 8) */
FROM RECON_IB_CDR_67 M
WHERE SUBSTR(TO_CHAR(M.START_TIME, 'yyyymmddhh24miss'), 9, 2) NOT BETWEEN '08' AND '17'
AND SUBSTR(M.ORG_NUM, 0, 5) in
('95979', '95978', '95977' ,'95976')  and (substr(m.term_num,0,5) in ('95930','95931','95932','95933','95934','95936') or substr(m.term_num,0,6) in ('959340','959346','959349'))
and substr(m.term_num,0,6)<>'959593'
AND M.REID BETWEEN 1249 AND 1252
GROUP BY TRUNC(M.START_TIME)) OP
ON PK.PK_STIME = OP.OP_SDATE
LEFT JOIN (SELECT TRUNC(M.START_TIME) SMS_SDATE, COUNT(*) SMS_CNT
/*+parallel(m, 8) */
FROM RECON_IB_CDR_67 M
WHERE SUBSTR(M.ORG_NUM, 0, 5) in
('95979', '95978', '95977' , '95976')  and (substr(m.term_num,0,5) in ('95930','95931','95932','95933','95934','95936') or substr(m.term_num,0,6) in ('959340','959346','959349'))
and substr(m.term_num,0,6)<>'959593'
AND M.REID >= 1253
GROUP BY TRUNC(M.START_TIME)) SMS
ON SMS.SMS_SDATE = OP.OP_SDATE
ORDER BY PK.PK_STIME
'''
print exeSql

curs.execute(exeSql)

print "==========================tmp_telenor_mec_report finished =========================="
curs.close()
conn.close()
