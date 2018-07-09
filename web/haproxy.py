#!/usr/bin/env python
#_*_coding:utf-8_*_
import os
import commands
import re

def HaproxyIp(ha,ip):
    ha_info = []
    for ha_group in ha:
         ha_dir =  "/Users/wangwang1/data/ansible/ha/%s/ha_config/roles/update/templates/haproxy.cfg" %ha_group
         cmd = "cat %s | grep %s: | grep -Ev '^\s+\#'" %(ha_dir,ip)
         (status,output)=commands.getstatusoutput(cmd)
         if  status == 0:
             if re.findall("bind",output):
                 vip = "vip: " + ip
                 ha_dic = {"group":ha_group,"ip":vip}
                 ha_info.append(ha_dic)
             elif re.findall("server",output):
                 member = "member: " + ip
                 ha_dic = {"group":ha_group,"ip":member}
                 ha_info.append(ha_dic)
    return ha_info

