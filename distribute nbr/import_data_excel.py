# !/usr/bin/python
# coding: utf-8

import sys

import cx_Oracle
import xlrd


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception, e:
        print str(e)


def excle_table_byindex(file):
    try:
        data = open_excel(file)
        table = data.sheets()[0]
        nrows = table.nrows
        param = []
        for rownum in range(0, nrows):
            rowval = table.row_values(rownum)
            # if rowval:
            tupleValue = (str(int(table.cell_value(rownum, 1))), str(int(table.cell_value(rownum, 2))),
                          '9' + str(int(table.cell_value(rownum, 3))))
            param.append(tupleValue)
        # print param
        inoracle(param)
    except Exception, e:
        print str(e)


def inoracle(param):
    flag = 0
    try:
        conn = cx_Oracle.connect('crm/hdycrm_smart@10.18.128.37:1522/crm ')
        curs = conn.cursor()
        curs.execute('delete FROM  tmp_wave')
        conn.commit()
        curs.prepare('insert into tmp_wave(iccid, imsi, acc_nbr) values(:1, :2, :3)')
        curs.executemany(None, param)
        conn.commit()
    except Exception, e:
        flag = 1
        print "*****************异常:%s*****************" % (str(e))
    finally:
        curs.close()
        conn.close()
        if flag == 0:
            print '*****************finsh*****************'


def main():
    reload(sys)
    # sys.setdefaultencoding('UTF-8')
    excle_table_byindex('nbrlist.xlsx')


if __name__ == "__main__":
    main()
