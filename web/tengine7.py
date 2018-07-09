#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
import time
import commands
import difflib

firstdir = "/Users/wangwang1/data/ansible/7_layer/"
seconddir = "/nginx_config/update/templates/upstream/"
thiredir = "/nginx_config/rollback/templates/upstream/"

#显示每组upstream业务信息
def NgninxUpstream(group):
    Info = {"Service":"","Upstream":""}
    nginx_dir = firstdir + group + seconddir
    cmd = "find %s -name '*.conf' -o -name '*.upstream'| awk -F '\/' '{print $NF}'" %(nginx_dir)
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        res = output.split("\n")
    Info["Service"]=group
    Info["Upstream"]=res
    return Info

#显示upstream内容
def Showupstream(upstream,serviceline,idc):
    dir = firstdir+ serviceline + "/" + idc + seconddir + upstream
    file_object = open(dir, 'r')
    content = file_object.read()
    file_object.close()
    return content

#更改upstream内容

def UpdateUpstream(upstream,serviceline,idc,updatefile):
    dir = firstdir+ serviceline + "/" + idc + seconddir + upstream
    upstreamfile = open(dir,'r')
    backupstreamfile = firstdir+ serviceline + "/" + idc + thiredir + upstream + time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    rollbackupstreamfile = firstdir+ serviceline + "/" + idc + thiredir + upstream + "rollback"
    backupstream = open(backupstreamfile,'w')
    rollbackupstrem = open(rollbackupstreamfile,'w')
    content = upstreamfile.readline()
    while len(content) > 0:
        backupstream.write(content)
        rollbackupstrem.write(content)
        content = upstreamfile.readline()
    backupstream.close()
    rollbackupstrem.close()
    upstreamfile.close()
    try:
        changupstream  = open(dir,'w')
        changupstream.write(updatefile)

        return ('配置文件变更成功')
    except Exception, e:
        return ("配置文件变更失败")
    changupstream.close()

#对比更改upstream内容

def Contrastupstream(upstream,serviceline,idc,updatefile):
    dir = firstdir+ serviceline + "/" + idc + seconddir + upstream
    a=[]
    b=[]
    res =''
    tempfile = open('/tmp/tempupstream','w')
    tempfile.write(updatefile)
    tempfile.close()
    after = open('/tmp/tempupstream','r')
    for i in after.readlines():
        a.append(i)
    after.close()
    before = open(dir,'r')
    for i in before.readlines():
        b.append(i)
    before.close()
    dif = difflib.unified_diff(b, a, fromfile='before', tofile='after')
    for i in dif:
        res = res + i
    return (res)

#下发配置文件

def Sendconfiguration(ipgroup,serviceline):
    return