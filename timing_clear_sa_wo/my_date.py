# !/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
import cx_Oracle

now = datetime.date.today()


def getlastBillingCycle():
    if str(datetime.date.today()).split('-')[1] == str(datetime.date.today() + datetime.timedelta(-1)).split('-')[1]:
        return getBillingCycle()
    else:
        return str(int(getBillingCycle()) - 1)


def getlastBillingCyclePOS():
    if str(datetime.date.today()).split('-')[1] == str(datetime.date.today() + datetime.timedelta(-1)).split('-')[1]:
        return getBillingCyclePOS()
    else:
        return str(int(getBillingCyclePOS()) - 1)


def getBillingCycle():
    connStr = connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
    conn = cx_Oracle.connect(connStr)
    curs = conn.cursor()
    billingSql = '''select t.billing_cycle_id from billing_cycle t where to_char(t.cycle_begin_date,'yyyymm')=to_char(sysdate,'yyyymm')
    and t.billing_cycle_type_id=1'''
    result = curs.execute(billingSql).fetchall()[0][0]
    curs.close()
    conn.close()
    return result


def getBillingCyclePOS():
    connStr = connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
    conn = cx_Oracle.connect(connStr)
    curs = conn.cursor()
    billingSql = '''select t.billing_cycle_id from billing_cycle t where to_char(t.cycle_begin_date,'yyyymm')=to_char(sysdate,'yyyymm')
    and t.billing_cycle_type_id=2'''
    result = curs.execute(billingSql).fetchall()[0][0]
    curs.close()
    conn.close()
    return result


def getlastMonth():
    lastMonth = ''
    if str(datetime.date.today()).split('-')[1] == str(datetime.date.today() + datetime.timedelta(-1)).split('-')[1]:
        lastMonth = str(datetime.date.today()).split('-')[1]
    else:
        lastMonth = str(datetime.date.today() + datetime.timedelta(-1)).split('-')[1]
    return lastMonth


def getYesterday():
    """
     返回昨天 格式yyyymmdd 20160913
    :return String :
    """
    return str(now + datetime.timedelta(-1)).replace('-', '')


def getToday():
    """
    返回今天 格式yyyymmdd 20160913
    :return string:
    """
    return str(now).replace('-', '')


def getTodayDays():
    """返回今天是昨天是第几天"""
    return str(int(str(now).split('-')[2]))


def getTodayMonth():
    """返回今天是昨天是第几个月"""
    return str(int(str(now).split('-')[1]))


def getLastMonth():
    return str(int(str(now).split('-')[1]) - 1)


def getYestdayDays():
    "返回昨天是第几天,如果遇到每个月的第一天返回上月最后一天"
    return str(now + datetime.timedelta(-1)).split('-')[2]


def getLastWeekStartDay():
    "用鱼innwa bank report 的起始时间"
    dayscount = datetime.timedelta(7)
    dayto = now - dayscount
    return str(dayto).replace('-','')


