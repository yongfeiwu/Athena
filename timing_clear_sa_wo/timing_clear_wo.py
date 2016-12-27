# !/usr/bin/python
# -*- coding:utf-8 -*-
# __author__ = 'Wuyongfei'
# __assessor__ = ''
# __createDate__ = '2016/12/23'

import CONSTANT
import Util


# 错误类型1处理入口
def hanleType1(wo_list):
    Util.move2bak(wo_list)
    Util.updateOrderItermState()


# 错误类型2处理入口
def handleType2(wo_list):
    Util.move2bak(wo_list)


# 错误类型3，4处理入口
def handleType43(wo_list, type):
    Util.updateWoState(wo_list, type)


def handleRecords():
    for type in CONSTANT.CLEAR_TYPE:
        # 获取配置表信息
        err_list = Util.errTypeList(type)
        for err in err_list:
            # 获取工单列表
            wo_list = Util.woList(type, err)

            if (type == '4') or (type == '3'):
                handleType43(wo_list, type)

            elif type == '2':
                handleType2(wo_list)

            elif type == '1':
                hanleType1(wo_list)


def main():
    handleRecords()


if __name__ == "__main__":
    main()
