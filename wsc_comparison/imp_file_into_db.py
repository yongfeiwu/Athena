# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re

import cx_Oracle

# 路径常量
LOCALPATH = "/Users/nicholas/PycharmProjects/project/Athena/wsc_comparison"
# # 转换目录
# os.chdir(LOCALPATH)


# 返回LOCALPATH下的所有文件和目录名
# for dir in os.path.
file_record = []
obj_file = []
all_records = []

param_list = []
for p, d, f in os.walk(LOCALPATH):
    for filename in f:
        # .DS_Store mac下特有记录文件排列等信息
        if re.search('^in01_G_85', filename):
            obj_file.append(os.path.join(p, filename))
        else:
            pass
print "=====================总共有  %s 个文件=====================" % (len(obj_file))

# print obj_file

# 将所有行数放到list中
for filename in obj_file:
    file_record = []
    for line in open(filename).readlines():
        file_record.append(line)
    for record in file_record:
        if re.search('\*223\*', record):
            all_records.append(record)
print "=====================总共有%s条充值记录=====================" % (len(all_records))
# 处理数据
for record in all_records:
    # 切割每一条数据
    element_list = record.split("|")
    calling_nbr = element_list[2]
    start_time = element_list[4]
    end_time = element_list[5]
    temp = element_list[3]
    charge = temp.split('*')[2]
    called_nbr = ''
    if len(temp.split('*')) == 4:
        called_nbr = temp.split('*')[3]
        tuple_v = (calling_nbr, called_nbr, charge, start_time, end_time, temp)
        param_list.append(tuple_v)
        # 组成元祖类型以便后续批量插入
    # break
print len(param_list)

# 数据库的连接信息
connStr = 'tb_mcc/smart@10.18.137.14:1521/mcc'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()


curs.prepare(
    'insert into tmp_vas_transfer_data(calling_nbr ,called_nbr,charge,start_time,end_time,command_line) values(:1, :2, :3,:4,:5,:6)')
curs.executemany(None, param_list)
conn.commit()
print "=====================操作完成====================="
# 关闭数据库连接
curs.close()
conn.close()
