# !/usr/bin/python
# -*- coding: utf-8 -*-
import os

import cx_Oracle

# 路径常量
LOCALPATH = "/Users/nicholas/Downloads/sdp_comparison_report/20161110"
# 转换目录
os.chdir(LOCALPATH)
# 打印目录
# print os.getcwd()

# 返回LOCALPATH下的所有文件和目录名
# for dir in os.path.
obj_record = []
obj_file = []
all_records = []
for p, d, f in os.walk(LOCALPATH):
    for filename in f:
        # .DS_Store mac下特有记录文件排列等信息
        if filename == '.DS_Store':
            pass
        else:
            obj_file.append(os.path.join(p, filename))
print "=====================总共有  %s 个文件=====================" % (len(obj_file))

# 将所有行数放到list中
for filename in obj_file:
    for line in open(filename).readlines():
        obj_record.append(line)
print "=====================总共有%s条充值记录=====================" % (len(obj_record))

# 处理数据
for record in obj_record:
    # 切割每一条数据
    element_list = record.split("|")

    # 组成元祖类型以便后续批量插入
    tuple_v = (str(element_list[0]), int(element_list[1][6:]), int(element_list[2].split(".")[0]))
    all_records.append(tuple_v)
# 数据库的连接信息
connStr = 'mcc/hdymcc_smart@10.18.128.31:1521/mcc'
# 连接数据库
conn = cx_Oracle.connect(connStr)
curs = conn.cursor()

curs.prepare(
    'insert into tmp_sdp_recharge_data(starttime ,telnum,charge) values(:1, :2, :3)')
curs.executemany(None, all_records)
conn.commit()
print "=====================操作完成====================="
# 关闭数据库连接
curs.close()
conn.close()
