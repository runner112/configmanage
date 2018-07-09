"""ansible URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hostgroup/(?P<group>\w*)/', views.Hostgroup),
    url(r'^upstream/(?P<Serviceline>\w*)/(?P<Idc>\w*)', views.Editupstream),
    url(r'^layer7/(?P<Serviceline>\w*)/(?P<Idc>\w*)', views.Checkconfig),
    url(r'^playbook/(?P<Serviceline>\w*)/(?P<Idc>\w*)', views.Playexecute),
    url(r'^layer7/', views.layer7),
    url(r'^asset/', views.Asset),
    url(r'^asset2/', views.Asset2),
    url(r'^seeasset/del/', views.DelIp),
    url(r'^seeasset/', views.SeeAsset),
    url(r'^$',views.Index),
]
