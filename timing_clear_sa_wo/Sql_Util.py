# !/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ = 'Wuyongfei'
# __assessor__ = ''
# __createDate__ = '2016/12/26'
import CONSTANT


# 获取查询工单的sql语句
def getQueryWoSql(clear_type, row):
    query_wo_sql = ''
    # 错误类型2，只需要使用ne_id即可
    if clear_type == CONSTANT.CLEAR_TYPE[0]:
        query_wo_sql = '''select * from sa_wo where event_type = %s and check_in_comments = '%s' ''' % (row[0], row[1])

    elif clear_type == CONSTANT.CLEAR_TYPE[1]:
        query_wo_sql = '''select * from sa_wo where ne_id = %s''' % (row[0])

    elif clear_type == CONSTANT.CLEAR_TYPE[2]:
        query_wo_sql = '''select * from sa_wo where event_type = %s and check_in_comments = '%s' ''' % (row[0], row[1])
    elif clear_type == CONSTANT.CLEAR_TYPE[3]:
        query_wo_sql = '''select * from sa_wo where check_in_comments = '%s' ''' % (row[0])
    return query_wo_sql


# 获取自动化处理配置表中的各种类型的sql语句
def getErrTypeSql(clear_type):
    error_type_sql = ''
    if clear_type == CONSTANT.CLEAR_TYPE[0]:
        # 获取错误类型1的信息列表
        error_type_sql = '''
        select t.event_type, t.check_in_comments
          from sa_wo_tmp_err t
         where t.state = 'A'
           and t.clear_type = '1'
        '''
    elif clear_type == CONSTANT.CLEAR_TYPE[1]:
        error_type_sql = '''
        select t.ne_id
          from sa_wo_tmp_err t
         where t.state = 'A'
           and t.clear_type = '2'
        '''
    elif clear_type == CONSTANT.CLEAR_TYPE[2]:
        error_type_sql = '''
        select t.event_type, t.check_in_comments
          from sa_wo_tmp_err t
         where t.state = 'A'
           and t.clear_type = '3'
        '''
    elif clear_type == CONSTANT.CLEAR_TYPE[3]:
        error_type_sql = '''
        select t.check_in_comments
          from sa_wo_tmp_err t
         where t.state = 'A'
           and t.clear_type = '4'
        '''
    return error_type_sql


def updateWo(clear_type, wo):
    update_sql = ''
    if clear_type == '3':
        update_sql = '''update sa_wo a set a.state='A' where a.wo_id= %s''' % (wo[0])
    elif clear_type == '4':
        update_sql = '''update sa_wo a set a.state='C' where a.wo_id= %s''' % (wo[0])
    return update_sql


def getInsertSql():
    return '''insert into sa_wo_script_bak(
        WO_ID,
        ORDER_ID,
        SEQ,
        NODE_INST_ID,
        WS_ID,
        NE_ID,
        EVENT_TYPE,
        STATE,
        STATE_DATE,
        CHECK_OUT_DATE,
        CHECK_IN_DATE,
        CHECK_OUT_COMMENTS,
        CHECK_IN_COMMENTS,
        CREATED_DATE,
        BACKFILL_PARAM,
        INPUT_PARAM,
        IS_BLOCK,
        PRIORITY,
        COMPLETED_DATE,
        REQ_DATE,
        SP_ID,
        IS_ROLLBACK,
        IN_STAFF_JOB_ID,
        OUT_STAFF_JOB_ID
        ) values(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24)'''


def getDeleteSql():
    return '''delete from sa_wo where wo_id in (select aa.wo_id from sa_wo_script_bak aa)'''


def getModifyOrderItermStateSql():
    return '''update order_item t set t.order_state ='E' where t.order_item_id in(
    select distinct(b.order_item_id) from sa_wo_script_bak a,sa_order b
    where a.order_id=b.order_id
    )'''


def getMoveFinalTableSql():
    return '''insert into sa_wo_wyf_final select * from sa_wo_script_bak'''


def getModifyWoStateSql(clear_type, woId):
    updateWoSateSql = ''
    if clear_type == '4':
        updateWoSateSql = '''
         update sa_wo a
           set a.state = 'A'
         where a.wo_id = %s''' % (woId)
    elif clear_type == '3':
        updateWoSateSql = '''
        update sa_wo a
           set a.state = 'C'
         where a.wo_id = %s
        ''' % (woId)
    return updateWoSateSql


def getDeleteScriptTableSql():
    return '''delete from sa_wo_script_bak'''
