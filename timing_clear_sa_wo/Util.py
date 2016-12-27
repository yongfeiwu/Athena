# !/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ = 'Wuyongfei'
# __assessor__ = ''
# __createDate__ = '2016/12/26'

import Sql_Util
import DB_Util
import CONSTANT


def close(conn, curs):
    DB_Util.closeCursor(curs)
    DB_Util.closeConnect(conn)


def errTypeList(clear_type):
    sql = Sql_Util.getErrTypeSql(clear_type)
    conn = DB_Util.getConnect(CONSTANT.CONN_STR)
    curs = DB_Util.getCursor(conn)
    result = DB_Util.executeSelect(sql, curs)
    return result


def woList(clear_type, err):
    sql = Sql_Util.getQueryWoSql(clear_type, err)
    conn = DB_Util.getConnect(CONSTANT.CONN_STR)
    curs = DB_Util.getCursor(conn)
    result = DB_Util.executeSelect(sql, curs)
    return result


def commit(conn):
    DB_Util.commit(conn)


def updateWoComm(type, wo):
    sql = Sql_Util.updateWo(type, wo)
    conn = DB_Util.getConnect(CONSTANT.CONN_STR)
    curs = DB_Util.getCursor(conn)
    # DB_Util.executeSql(sql, curs)
    # DB_Util.commit(conn)
    close(conn, curs)

def move2bak(wo_list):
    conn = DB_Util.getConnect(CONSTANT.CONN_STR)
    curs = DB_Util.getCursor(conn)
    # 数据插入到临时表
    isSql = Sql_Util.getInsertSql()
    curs.prepare(isSql)
    curs.executemany(None, wo_list)
    conn.commit()
    # 删除sa_wo中的数据
    dSql = Sql_Util.getDeleteSql()
    curs.execute(dSql)
    conn.commit()

    # 将数据移动到脚本处理的最终备份表
    fSql = Sql_Util.getMoveFinalTableSql()
    curs.execute(fSql)
    conn.commit()
    # 将临时表中的数据清空
    dSciprtSql = Sql_Util.getDeleteScriptTableSql()
    curs.execute(dSciprtSql)
    conn.commit()
    close(conn, curs)


def updateOrderItermState():
    conn = DB_Util.getConnect(CONSTANT.CONN_STR)
    curs = DB_Util.getCursor(conn)
    uOrdersql = Sql_Util.getModifyOrderItermStateSql()
    curs.execute(uOrdersql)

    conn.commit()
    close(conn, curs)



def updateWoState(wo_list,type):
    conn = DB_Util.getConnect(CONSTANT.CONN_STR)
    curs = DB_Util.getCursor(conn)
    for wo in wo_list:
        uWoAsql = Sql_Util.getModifyWoStateSql(type,wo[0])
        curs.execute(uWoAsql)
        conn.commit()
    close(conn, curs)


