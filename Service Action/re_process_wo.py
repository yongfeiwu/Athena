# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle

connStr = connStr = 'crm/hdycrm_smart@10.18.128.37:1522/crm'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

