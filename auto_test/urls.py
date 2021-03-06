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
from django.contrib.auth.views import auth_login, auth_logout

from MyApp.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^welcome/$', welcome),  # 获取菜单
    url(r'^home/$', home),  # 进入首页
    url(r'^child/(?P<eid>.+)/(?P<oid>.*)/(?P<ooid>.*)/$', child),  # 返回子页面
    url(r'^login/$', login),  # 登陆
    url(r'^login_action/$', login_action),  # 登陆
    url(r'^register_action/$', register_action),  # 注册
    url(r'logout/$', logout),  # 推出
    url(r'pei/$', pei),  # 吐槽
    url(r'^help/$', api_help),  # 帮助文档
    url(r'^project_list/$', project_list),  # 进入项目列表
    url(r'^delete_project/$', delete_project),  # 删除项目
    url(r'^add_project/$', add_project),  # 新增项目
    url(r'^apis/(?P<id>.*)/$', open_apis),  # 进入接口库
    url(r'^cases/(?P<id>.*)/$', open_cases),  # 进入用例设置
    url(r'^project_set/(?P<id>.*)/$', open_project_set),  # 进入项目设置
    url(r'^save_project_set/(?P<id>.*)/$', save_project_set),  # 保存项目设置
    url(r'^project_api_add/(?P<Pid>.*)/$', project_api_add),  # 新增接口
    url(r'^project_api_del/(?P<id>.*)/$', project_api_del),  # 删除接口
    url(r'^save_bz/$', save_bz),  # 保存备注
    url(r'^get_bz/$', get_bz),  # 获取备注
    url(r'^Api_save/$', Api_save),  # 保存接口
    url(r'^get_api_data/$', get_api_data),  # 获取接口信息
    url(r'^Api_send/$', Api_send),  # 接口请求
    url(r'^copy_api/$', copy_api),  # 复制接口
    url(r'^error_request/$', error_request),  # 异常值测试
    url(r'^Api_send_home/$', Api_send_home),  # 首页发送请求
    url(r'^get_home_log/$', get_home_log),  # 获取最新请求记录
    url(r'^get_api_log_home/$', get_api_log_home),  # 获取完整的单一请求记录数据
    url(r'^home_log/(?P<log_id>.*)$', home),  # 再次进入首页，这次要带着请求记录
    url(r'^add_case/(?P<eid>.*)$', add_case),  # 新增测试用例
    url(r'^del_case/(?P<eid>.*)/(?P<oid>.*)/$', del_case),  # 新增测试用例
    url(r'^copy_case/(?P<eid>.*)/(?P<oid>.*)/$', copy_case),  # 新增测试用例

]
