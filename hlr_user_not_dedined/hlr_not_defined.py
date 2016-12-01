# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import re
import datetime

connStr = 'crm/hdycrm_smart@10.18.128.37:1522/crm'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

query_sql = '''
select t.* from sa_wo t where t.state='D' and t.check_in_comments = '3001|Subscriber not defined'
'''

result = curs.execute(query_sql).fetchall()
infor = []

for row in result:
    subsInfo = {}
    # print row[15].split("|")
    for param in row[15].split("|"):
        if re.search('MDN', param):
            subsInfo['MDN'] = param.split("=")[1]
            # print param.split("=")[1]
        if re.search('IMSI', param):
            subsInfo['IMSI'] = param.split("=")[1]
            # print param.split("=")[1]

        infor.append(subsInfo)

print infor
