# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

# 数据库的连接信息
connStr = 'sett/sett@10.18.129.67:1521/sett'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

exeSql = '''
create table recon_ib_cdr_74_final as
select t.* from recon_ib_cdr_74 t
union all
select tt.* from recon_ib_cdr_74_mig tt;
'''
print exeSql

curs.execute(exeSql)

print "==========================create recon_ib_cdr_74_final finished =========================="
curs.close()
conn.close()
