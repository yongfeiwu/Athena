# !/usr/bin/python
# -*- coding: utf-8 -*-
import cx_Oracle
import datetime

now = str(datetime.date.today()).replace('-', '')

connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()
tmp_select_cc = '''
select *
  from tmp_crbt_active_issue_%s
''' % now

result = curs.execute(tmp_select_cc).fetchall()
curs.close()
conn.close()

connStr = 'crm/hdycrm_smart@10.18.128.37:1522/crm'
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()
insert_cbrt_sql = ''
insert_hlr_sql = ''
for param in result:
    if param[2] == 35:
        if (len(param[0]) == 8) or (len(param[0]) == 9):
            # insert_cbrt_sql = '''
            #     insert into sa_wo
            #     values
            #       (SA_WO_ID_SEQ.NEXTVAL,
            #        122122,
            #        1,
            #        122122,
            #        1006,
            #        1006,
            #        355004,
            #        'A',
            #        sysdate,
            #        sysdate,
            #        sysdate,
            #        '',
            #        '',
            #        sysdate,
            #        '',
            #        'KI=""|ServiceOfferId="%s"|RBT_NE_ID="1"|MDN="95%s"|IMSI="%s"',
            #        'N',
            #        100,
            #        sysdate,
            #        '',
            #        '',
            #        '',
            #        '',
            #        '')
            #     ''' % (param[2], param[0], param[1])
            insert_hlr_sql = '''
                insert into sa_wo
                    values
                      (SA_WO_ID_SEQ.NEXTVAL,
                       12241224,
                       1,
                       12241224,
                       2004,
                       2004,
                       500461,
                       'A',
                       sysdate,
                       sysdate,
                       sysdate,
                       '',
                       '',
                       sysdate,
                       '',
                       'ServiceOfferId="%s"|RBT_NE_ID="1"|MDN="95%s"|IMSI="%s"',
                       'N',
                       100,
                       sysdate,
                       '',
                       '',
                       '',
                       '',
                       '')
                    ''' % (param[2], param[0], param[1])

        else:
            # insert_cbrt_sql = '''
            #     insert into sa_wo
            #     values
            #       (SA_WO_ID_SEQ.NEXTVAL,
            #        122122,
            #        1,
            #        122122,
            #        3001,
            #        3001,
            #        355004,
            #        'A',
            #        sysdate,
            #        sysdate,
            #        sysdate,
            #        '',
            #        '',
            #        sysdate,
            #        '',
            #        'KI=""|ServiceOfferId="%s"|RBT_NE_ID="2"|MDN="95%s"|IMSI="%s"',
            #        'N',
            #        100,
            #        sysdate,
            #        '',
            #        '',
            #        '',
            #        '',
            #        '')
            #     ''' % (param[2], param[0], param[1])
            insert_hlr_sql = '''
                insert into sa_wo
                    values
                      (SA_WO_ID_SEQ.NEXTVAL,
                       12241224,
                       1,
                       12241224,
                       2004,
                       2004,
                       500461,
                       'A',
                       sysdate,
                       sysdate,
                       sysdate,
                       '',
                       '',
                       sysdate,
                       '',
                       'ServiceOfferId="%s"|RBT_NE_ID="2"|MDN="95%s"|IMSI="%s"',
                       'N',
                       100,
                       sysdate,
                       '',
                       '',
                       '',
                       '',
                       '')
                    ''' % (param[2], param[0], param[1])
    else:
        # insert_cbrt_sql = '''
        # insert into sa_wo
        #         values
        #           (SA_WO_ID_SEQ.NEXTVAL,
        #            122122,
        #            1,
        #            122122,
        #            1001,
        #            1001,
        #            355004,
        #            'A',
        #            sysdate,
        #            sysdate,
        #            sysdate,
        #            '',
        #            '',
        #            sysdate,
        #            '',
        #            'KI=""|ServiceOfferId="%s"|RBT_NE_ID="3"|MDN="95%s"|IMSI="%s"',
        #            'N',
        #            100,
        #            sysdate,
        #            '',
        #            '',
        #            '',
        #            '',
        #            '')
        # ''' % (param[2], param[0], param[1])
        insert_hlr_sql = '''
            insert into sa_wo
                values
                  (SA_WO_ID_SEQ.NEXTVAL,
                   12241224,
                   1,
                   12241224,
                   2004,
                   2004,
                   500461,
                   'A',
                   sysdate,
                   sysdate,
                   sysdate,
                   '',
                   '',
                   sysdate,
                   '',
                   'ServiceOfferId="%s"|RBT_NE_ID="3"|MDN="95%s"|IMSI="%s"',
                   'N',
                   100,
                   sysdate,
                   '',
                   '',
                   '',
                   '',
                   '')
                ''' % (param[2], param[0], param[1])
    curs.execute(insert_hlr_sql)
    # curs.execute(insert_cbrt_sql)
    conn.commit()
curs.close()
conn.close()