"""auto_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib.auth.views import auth_login,auth_logout

from MyApp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^welcome/$', welcome),# 获取菜单
    url(r'^home/$', home),# 进入首页
    url(r'^child/(?P<eid>.+)/(?P<oid>.*)/$', child),# 返回子页面
    url(r'^login/$', login),# 登陆
    url(r'^login_action/$', login_action),# 登陆
    url(r'^register_action/$', register_action),# 注册
    url(r'logout/$', logout),# 推出
    url(r'pei/$', pei),# 推出


]
