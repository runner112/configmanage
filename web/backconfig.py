#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
import commands
import re
import time
import difflib


firstdir = "/Users/wangwang1/data/ansible/ha/"
seconddir = "/ha_config/roles/update/templates/haproxy.cfg"
thiredir = "/ha_config/roles/rollback/templates/haproxy.cfg"

def update(pagefile,updatefile):
    old_file_name = firstdir + pagefile + seconddir
    old_file = open(old_file_name, 'r')
    new_file_name = firstdir + pagefile + thiredir + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    rollback_file_name = firstdir + pagefile + thiredir + "rollback"
    new_file = open(new_file_name, 'w')
    rollback_flie = open(rollback_file_name,'w')
    content = old_file.readline()
    while len(content) > 0:
        new_file.write(content)
        rollback_flie.write(content)
        content = old_file.readline()
    try:
        changfile = open(old_file_name,'w')
        changfile.write(updatefile)
        changfile.close()
        return ('配置文件变更成功')
    except Exception,e:
        return ("配置文件变更失败")
    old_file.close()
    new_file.close()
    rollback_flie.close()

def contrast(pagefile,updatefile):
    old_file_name = firstdir + pagefile + seconddir
    a=[]
    b=[]
    res =''
    tempfile = open('/tmp/temppage','w')
    tempfile.write(updatefile)
    tempfile.close()
    after = open('/tmp/temppage','r')
    for i in after.readlines():
        a.append(i)
    after.close()
    before = open(old_file_name,'r')
    for i in before.readlines():
        b.append(i)
    before.close()
    dif = difflib.unified_diff(b, a, fromfile='before', tofile='after')
    for i in dif:
        res = res + i
    return (res)




def rallbackup(pagefile):
    new_file_name = firstdir + pagefile + seconddir
    old_file_name = firstdir + pagefile + thiredir + "rollback"
    old_file = open(old_file_name, 'r')
    new_file = open(new_file_name, 'w')
    content = old_file.readline()
    try:
        while len(content)>0:
            new_file.write(content)
            content = old_file.readline()
        return ("配置文件回滚成功")
    except Exception,e:
        return ("配置文件回滚失败")
    old_file.close()
    new_file.close()
