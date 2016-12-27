# !/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ = 'Wuyongfei'
# __assessor__ = ''
# __createDate__ = '2016/12/16'
import cx_Oracle


def getConnect(connStr):
    """获取连接"""
    return cx_Oracle.connect(connStr)


def closeConnect(conn):
    "关闭连接"
    conn.close()


def getCursor(conn):
    """获取cursor"""
    return conn.cursor()


def closeCursor(curs):
    """关闭cursor"""
    curs.close()


def executeSql(sqlStr, curs):
    """执行insert, create语句"""
    curs.execute(sqlStr)



def executeSelect(sqlStr, curs):
    """执行select 语句"""
    return curs.execute(sqlStr).fetchall()


def commit(conn):
    conn.commit()
