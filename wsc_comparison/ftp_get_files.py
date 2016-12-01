#!/usr/bin/python
# -*- coding: utf-8 -*-

import ftplib
import re
import socket
import sys

CONST_BUFFER_SIZE = 8192
host = '10.18.34.133'
username = 'zxin10'
password = 'os10+ZTE'
remote_path = '/ipaycdr/cdrbak/'


def connect(host_p, user_p, pwd_p):
    try:
        ftp = ftplib.FTP(host_p)
        ftp.login(user_p, pwd_p)
        return ftp
    except socket.error, socket.gaierror:
        print("连接失败, 请检查IP地址和用户名密码!")
        sys.exit(0)


def disconnect(ftp):
    ftp.quit()


def listFiles(ftp):
    return ftp.nlst()


def download(ftp, filename):
    f = open(filename, "wb").write
    try:
        ftp.retrbinary("RETR %s" % filename, f, CONST_BUFFER_SIZE)
    except ftplib.error_perm:
        print 'error'
    return True


def main():
    ftp = connect(host, username, password)
    try:
        ftp.cwd(remote_path)
        filesList = listFiles(ftp)
    except ftplib.error_perm:
        print host + " %s desn't exist" % (remote_path)

    count = 0
    # in01_G_85_xxxxx_2016MMDD.r
    for fileName in filesList:
        if re.search('^in01_G_85', fileName):
            timeSpan = fileName.split('_')[4].split('.')[0]
            if timeSpan >= '20161018':
                count = count + 1
                download(ftp, fileName)
            else:
                pass
        else:
            pass
    print '=====================总共下载%s个文件=====================' % (str(count))
    disconnect(ftp)
    print '=====================END====================='


if __name__ == "__main__":
    main()
