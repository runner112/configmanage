#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.shortcuts import render
# Create your views here.
#!/usr/bin/python
import datetime
from django.http.response import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import template
from haproxy import HaproxyIp
from tengine7 import NgninxUpstream,Showupstream,UpdateUpstream,Contrastupstream
from backconfig import update,contrast,rallbackup
from models import HostGroup,Host

##后台ansible主机信息录入
def Asset(request):
    obj_dic = {'status':'','GroupType':''}
    obj_dic['GroupType'] = HostGroup.objects.all()

    if request.method == 'POST':
        hostgroup = request.POST.get("hostgroup",None).strip()
        is_empty = all([hostgroup])
        if is_empty:
            count = group_number = HostGroup.objects.filter(name=hostgroup).count()
            if count >= 1:
                obj_dic['status'] = '主机名以录入，请修改主机名'
            else:
                HostGroup.objects.create(name=hostgroup)
                obj_dic['status'] = '主机组录入成功'
        else:
            obj_dic['status'] = '主机组不能为空'

    return render(request,'asset.html',{'list':obj_dic})


def Asset2(request):
    obj_dic = {'status':'','GroupType':''}
    obj_dic['GroupType'] = HostGroup.objects.all()

    if request.method == 'POST':
        ip = request.POST.get("ip",None).strip()
        id = request.POST.get('hostgroup',None)
        is_empty = all([ip,id])
        if is_empty:
            count = Host.objects.filter(ip=ip).count()
            if count >= 1:
                obj_dic['status'] = 'ip已重复录入'
            else:

                group = HostGroup.objects.get(id=id)
                Host.objects.create(ip=ip,group=group)
                obj_dic['status'] = '主机组录入成功'
        else:
            obj_dic['status'] = 'ip或主机组不能为空'

    return render(request,'asset.html',{'list':obj_dic})


def SeeAsset(request):
    obj_dic = {'hostlist':''}
    obj_dic['hostlist'] = Host.objects.order_by("group")
    return render(request,'seeasset.html',{'list':obj_dic})

def DelIp(request):
    ip = request.POST.get("ip",None)
    Host.objects.get(ip=ip).delete()
    return HttpResponse("ok")

##主页查询vip或member是否在公版ha上
def Index(request):
    ret = {'status':""}
    haproxy = ['ha_wbg1_bx',
               'ha_wbg1_ft',
               'ha_wbg1_kxc',
               'ha_wbg1_nfjd',
               'ha_wbg1_shx',
               'ha_wbg1_yf']
    if request.method == "POST":
        ipaddress  = request.POST.get('ipaddress', None)
        is_empty = all([ipaddress])
        if is_empty:
            ret['status'] = "查找结果:"
            ha_list = HaproxyIp(haproxy,ipaddress)

            return render(request,"index.html",{"list":ret,"ha":ha_list})
        else:
            ret['status'] = "ip 不能为空!"
            return render(request, "index.html", {"list": ret})

    else:
        return render(request,"index.html")


#haproxy配置文件管理

def Hostgroup(request,group):
        mesg = {'content':'','group':'','diff':''}
        dir = "/Users/wangwang1/data/ansible/ha/"+ group +"/ha_config/roles/update/templates/haproxy.cfg"
        file_object = open(dir,'r')
        content = file_object.read()
        file_object.close()
        mesg['content'] = content
        mesg['group'] = group
        if request.method == 'POST':
            comment = request.POST.get('comment', None)
            idnumber = request.POST.get('idnumber', None)
            is_empty = all([comment])
            if is_empty:
                if idnumber == "button01":
                    mesg['diff'] = contrast(group, comment)
                    return HttpResponse(mesg['diff'])
                elif idnumber == "button02":
                    res = update(group,comment)
                    return HttpResponse(res)
                elif idnumber == "button03":
                    res = rallbackup(group)
                    return HttpResponse(res)

        return render(request,'editconfiguration.html',{"mesg":mesg})

#7层nginx配置文件管理

def layer7(request):
    idc = request.GET['idc']
    upstream_infor = NgninxUpstream(idc)
    return render(request,'layer7.html',{'upstream_infor':upstream_infor})

def Checkconfig(request,Serviceline,Idc):
    res = {'upstream':'','content':''}
    Upstream = request.GET['upstream']
    content = Showupstream(Upstream,Serviceline,Idc)
    res['upstream']=Upstream
    res['content']=content
    return render(request,"browseupstream.html",{"res":res})

def Editupstream(request,Serviceline,Idc):
    mesg = {'upstream':'','content':''}
    Upstream = request.GET['upstream']
    content = Showupstream(Upstream, Serviceline, Idc)
    mesg['upstream']=Upstream
    mesg['content']=content
    if request.method == 'POST':
        comment = request.POST.get('comment', None)
        idnumber = request.POST.get('idnumber', None)
        if idnumber == "button02":
            res = UpdateUpstream(Upstream,Serviceline,Idc,comment)
            return HttpResponse(res)
        if idnumber == "button01":
            res = Contrastupstream(Upstream,Serviceline,Idc,comment)
            return HttpResponse(res)

    return render(request,'editconfigupstream.html',{"mesg":mesg})

###下发7层配置

def Playexecute(request,Serviceline,Idc):
    objc = Host.objects.filter(group__name=Idc)
    if request.method == 'POST':
        ip_sun = request.POST.get("ip_sum")
        dizhi = request.POST.get("dizhi")
    return render(request,'Playexecute.html',{"objc":objc})