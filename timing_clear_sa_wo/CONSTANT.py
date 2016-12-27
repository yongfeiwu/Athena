# !/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ = 'Wuyongfei'
# __assessor__ = ''
# __createDate__ = '2016/12/16'
# 常量定义文件
import my_date

# 数据库连接串
CONN_STR = 'tb_mcc/smart@10.18.137.14:1521/mcc'
# 清理类型目前只有4种
# 清理类型
# 1,3:根据签入返回码和事件类型处理
# 2:根据网元id处理
# 4:根据签入返回码直接处理
CLEAR_TYPE = ['1','2','3','4']
