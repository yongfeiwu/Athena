#! /usr/bin/python
# -*- coding: utf-8 -*-
# -*- 上线结算方脚本 -*-

import cx_Oracle

connStr = 'tb_v7_sett/smart@10.18.137.14:1521/MCC'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

partner_id_sql = 'select max(partner_id)+1 from ib_partner '

result = curs.excute(partner_id_sql)

curs.close()
conn.close()

