from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
import requests

from MyApp.models import *


# Create your views here.


def welcome(request):
    print('进入首页')
    # return HttpResponse('欢迎来到我的测试平台')
    return render(request, 'welcome.html')


# 控制不同页面返回不同数据:数据分发器
def child_json(eid, oid='', ooid=''):
    """
    child_json()  它专门用来接收页面名字，然后去不同的数据库中查找数据，
    进行整理后 返回给child()函数，再由child函数返回给前端浏览器
    :param eid:
    :return:
    """
    res = {}
    if eid == 'home.html':  # 首页的超链接
        data = DB_home_href.objects.all()
        home_log = DB_apis_log.objects.filter(user_id=oid)[::-1]
        if ooid == '':
            res = {"hrefs": data, 'home_log': home_log}
        else:
            log = DB_apis_log.objects.filter(id=ooid)[0]
            res = {"hrefs": data, 'home_log': home_log, 'log': log}
    
    if eid == 'project_list.html':  # 首页的项目列表
        data = DB_project.objects.all()
        res = {'projects': data}
    
    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)  # 获取项目下对应的apis
        res = {'project': project, 'apis': apis}
    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project': project}
    if eid == 'P_project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project': project}
    
    return res


# 返回子页面
def child(request, eid, oid, ooid):
    """
    eid，就是获取url中的 (?P<eid>.+) 的值，
    也就是我们welcome.html中的{{ whichHTML }} ，
    也就是我们后台函数返回的子页面html的真实名字
    :param request:
    :param eid: 进入的html文件名
    :param oid:
    :return:
    """
    res = child_json(eid, oid, ooid)
    
    return render(request, eid, res)


def home(request, log_id=''):
    # return render(request,'home.html',{'username':'赵丹丹'})
    # return render(request, 'welcome.html', {'whichHTML': 'home.html', 'oid': request.user.id})
    return render(request, 'welcome.html', {'whichHTML': 'home.html', 'oid': request.user.id, 'ooid': log_id})


def login(request):
    return render(request, 'login.html')


# 开始登陆
def login_action(request):
    """
    然后让我们思考这个函数应该做些什么事？
    1、获取前端给的 俩个字符串：用户名和密码
    2、调用django自带的用户数据库，来验证这个用户是否存在并且密码正确
    3、如果不正确，就随便给前端返回点什么，前端都会弹窗说报错文案
    4、如果正确，就给用户进行重定向，定到首页：home.html
    :param request:
    :return:
    """
    u_name = request.GET['username']
    p_word = request.GET['password']
    print(u_name, p_word)
    
    # 开始联通 Django 用户库，查看用户名和密码是否正确
    from django.contrib import auth
    # user = auth.authenticate(username=u_name,passowrd=p_word)
    # print(user)
    user = User.objects.filter(username=u_name).exists()
    # if user is not None:
    if user:
        # auth.login(request,user)
        # request.session['user']=u_name
        return HttpResponse('成功')
    else:
        return HttpResponse('失败')  # 用户名+密码错误


def register_action(request):
    """

    :param request:
    :return:
    """
    u_name = request.GET['username']
    p_word = request.GET['password']
    
    print('注册用户名密码：', u_name + '\n' + p_word)
    
    # from django.contrib.auth.hashers import make_password
    try:
        user = User.objects.create(username=u_name, password=p_word)
        user.save()
        return HttpResponse('注册成功！')
    except:
        return HttpResponse('注册失败，用户名{username}好像已存在'.format(username=u_name))


def logout(request):
    """
    1、调用django的内部函数auth.logout函数 来实现退出功能。
    2、给用户跳转到登陆页面。
    :param request:
    :return:
    """
    from django.contrib import auth
    auth.logout(request)
    return HttpResponseRedirect('/login/')


def pei(request):
    """
    吐槽函数
    这里给大家提供几个建议：
    1、通过钉钉的机器人发消息 ，此方法比较实时。很快速。而且不用存放在我们平台的数据库，省空间。但是操作起来需要钉钉里面群里添加机器人-发送接口 ，初次使用会很蒙蔽。
    2、发短信/邮件，此方法也可以，但是就是有点小题大做。而且调取短信接口花钱，发送邮件代码不是很好写。有兴趣的可以自己这么做
    3、存放在django平台的数据库中，给创建个吐槽表，然后管理员可以去后台随时查看，以后我们还可以利用这些吐槽做个弹幕.....  而且这里我正好可以给大家讲一下，如何新建一个表 和 如何操作这个表 的技术。
    :param request:
    :return:
    """
    tucao_text = request.GET['tocao_text']
    DB_tucao.objects.create(user=request.user.username, text=tucao_text)
    return HttpResponse('')


def api_help(request):
    """
    进入帮助文档函数
    :param request:
    :return:
    """
    return render(request, 'welcome.html', {'whichHTML': 'help.html', 'oid': ''})


def project_list(request):
    """
    进入项目列表
    :param request:
    :return:
    """
    return render(request, 'welcome.html', {'whichHTML': 'project_list.html', 'oid': ''})


def delete_project(request):
    """
    删除项目
    1、获取传过来的参数项目id
    2、去数据库的项目表 中删除掉这个id的项目
    3、随便返回个空字符串给前端
    :param request:
    :return:
    """
    id = request.GET['id']
    
    DB_project.objects.filter(id=id).delete()
    DB_apis.objects.filter(project_id=id).delete()
    
    return HttpResponse('')


def add_project(request):
    """
    新增项目
    1、接收project_name
    2、去项目表新建项目
    3、返回给前端一个空证明已经成功完成
    :param request:
    :return:
    """
    project_name = request.GET['project_name']
    DB_project.objects.create(name=project_name, remark='', user=request.user, other_user='')
    return HttpResponse('')


def open_apis(request, id):
    """

    :param request:
    :return:
    """
    project_id = id
    return render(request, 'welcome.html', {'whichHTML': 'P_apis.html', 'oid': project_id})


def open_cases(request, id):
    """

    :param request:
    :return:
    """
    project_id = id
    return render(request, 'welcome.html', {'whichHTML': 'P_cases.html', 'oid': project_id})


def open_project_set(request, id):
    """

    :param request:
    :return:
    """
    project_id = id
    return render(request, 'welcome.html', {'whichHTML': 'P_project_set.html', 'oid': project_id})


def save_project_set(request, id):
    """

    :param request:
    :return:
    """
    project_id = id
    name = request.GET['name']
    remark = request.GET['remark']
    other_user = request.GET['other_user']
    
    DB_project.objects.filter(id=project_id).update(name=name, remark=remark, other_user=other_user)
    
    return HttpResponse('')


def project_api_add(request, Pid):
    """
    保存新增接口
    :param request:
    :return:
    """
    project_id = Pid
    DB_apis.objects.create(project_id=project_id, api_method='none')
    return HttpResponseRedirect('/apis/%s/' % project_id)


def project_api_del(request, id):
    """
    删除api
    :param request:
    :param id:
    :return:
    """
    project_id = DB_apis.objects.filter(id=id)[0].project_id
    DB_apis.objects.filter(id=id).delete()
    
    return HttpResponseRedirect('/apis/%s/' % project_id)


def save_bz(request):
    """
    保存备注
    :param request:
    :return:
    """
    api_id = request.GET['api_id']
    bz_value = request.GET['bz_value']
    DB_apis.objects.filter(id=api_id).update(desc=bz_value)
    return HttpResponse('')


def get_bz(request):
    """
    获取备注
    :param request:
    :return:
    """
    api_id = request.GET['api_id']
    bz_value = DB_apis.objects.filter(id=api_id)[0].desc
    return HttpResponse(bz_value)


def Api_save(request):
    """
    保存接口
    1、获取到前端过来的所有数据
    2、保存
    3、返回保存成功文案
    :param request:
    :return:
    """
    api_id = request.GET['api_id']
    api_name = request.GET['api_name']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    # ts_api_body = request.GET['ts_api_body']
    
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
    else:
        ts_api_body = request.GET['ts_api_body']
    
    # 保存数据
    DB_apis.objects.filter(id=api_id).update(
        name=api_name,
        api_method=ts_method,
        api_url=ts_url,
        api_host=ts_host,
        api_header=ts_header,
        body_method=ts_body_method,
        api_body=ts_api_body,
    
    )
    
    return HttpResponse('success')


def get_api_data(request):
    """
    获取接口数据
    第一句是获取到前端过来的接口id
    第二句是拿到这个接口的字典格式数据
    第三句是返回给前端，但是数据要变成json串。
    :param request:
    :return:
    """
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type='application/json')


def Api_send(request):
    """
    调试弹窗发送请求
    1、获取到前端过来的所有数据
    2、发送请求返回值
    3、将返回值返回给前端
    :param request:
    :return:
    """
    # 获取到前端过来的所有数据
    api_id = request.GET['api_id']
    api_name = request.GET['api_name']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    # print(ts_body_method)
    # ts_api_body = request.GET['ts_api_body']
    
    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
        
        if ts_body_method in ['', None]:
            return HttpResponse('请先选择好请求编码格式和请求体，再点击Send按钮发送请求！')
    else:
        ts_api_body = request.GET['ts_api_body']
        api = DB_apis.objects.filter(id=api_id)
        api.update(last_body_method=ts_body_method, last_api_body=ts_api_body)
    # 发送请求返回值
    try:
        header = json.loads(ts_header)  # 将字符串转化为json
    except:
        return HttpResponse('请求头不符合json格式！')
    # 拼接URL
    if ts_host[-1] == '/' and ts_url[0] == '/':
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':
        url = ts_host + '/' + ts_url
    else:
        url = ts_host + ts_url
    
    try:
        if ts_body_method == 'none':
            response = requests.request(ts_body_method.upper(), url, headers=header, data={})
        elif ts_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_body_method.upper(), url, headers=header, data=payload, files=files)
        elif ts_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_body_method.upper(), url, headers=header, data=payload)
        else:
            if ts_body_method == 'Text':
                header['Content-Type'] = 'text/plain'
            if ts_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'
            if ts_body_method == 'Json':
                header['Content-Type'] = 'text/plain'
            if ts_body_method == 'Html':
                header['Content-Type'] = 'text/plain'
            if ts_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(ts_body_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))
        # 把返回值传递到前端页面
        response.encoding = 'utf-8'
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))


def copy_api(request):
    """
    复制接口
    :param request:
    :return:
    """
    api_id = request.GET['api_id']
    
    # 开始复制
    old_api = DB_apis.objects.filter(id=api_id)[0]
    
    DB_apis.objects.create(project_id=old_api.project_id,
                           name=old_api.name + '_副本',
                           api_method=old_api.api_method,
                           api_url=old_api.api_url,
                           api_header=old_api.api_header,
                           api_login=old_api.api_login,
                           api_host=old_api.api_host,
                           desc=old_api.desc,
                           body_method=old_api.body_method,
                           api_body=old_api.api_body,
                           result=old_api.result,
                           sign=old_api.sign,
                           file_key=old_api.file_key,
                           file_name=old_api.file_name,
                           public_header=old_api.public_header,
                           last_body_method=old_api.last_body_method,
                           last_api_body=old_api.last_api_body,
                           )
    
    # 返回
    return HttpResponse('')


def error_request(request):
    """
    异常值测试
    :param request:
    :return:
    """
    api_id = request.GET['api_id']
    new_body = request.GET['new_body']
    span_text = request.GET['span_text']
    #
    # print(new_body)
    api = DB_apis.objects.filter(id=api_id)[0]
    method = api.api_method
    url = api.api_url
    host = api.api_host
    header = api.api_header
    body_method = api.body_method
    try:
        header = json.loads(header)  # 将字符串转化为json
    except:
        return HttpResponse('请求头不符合json格式！')
    if host[-1] == '/' and url[0] == '/':
        url = host[:-1] + url
    elif host[-1] != '/' and url[0] != '/':
        url = host + '/' + url
    else:
        url = host + url
    
    try:
        if body_method == 'form-data':
            files = []
            payload = {}
            print(eval(new_body))
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload, files=files)
        elif body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload)
        elif body_method == 'Json':
            header['Content-Type'] = 'text/plain'
            response = requests.request(method.upper(), url, headers=header, data=new_body.encode('utf-8'))
        else:
            return HttpResponse('非法的请求体类型')
        # 把返回值传递到前端页面
        response.encoding = 'utf-8'
        res_json = {"response": response.text, "span_text": span_text}
        return HttpResponse(json.dumps(res_json), content_type='application/json')
    except:
        res_json = {"response": '对不起，接口未通！', "span_text": span_text}
        return HttpResponse(json.dumps(res_json), content_type='application/json')


# 首页发送请求
def Api_send_home(request):
    # 提取所有数据
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']
    ts_api_body = request.GET['ts_api_body']
    # 发送请求获取返回值
    try:
        header = json.loads(ts_header)  # 处理header
    except:
        return HttpResponse('请求头不符合json格式！')
    # 写入到数据库请求记录表中
    DB_apis_log.objects.create(user_id=request.user.id,
                               api_method=ts_method,
                               api_url=ts_url,
                               api_header=ts_header,
                               api_host=ts_host,
                               body_method=ts_body_method,
                               api_body=ts_api_body, )
    
    # 拼接完整url
    if ts_host[-1] == '/' and ts_url[0] == '/':  # 都有/
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':  # 都没有/
        url = ts_host + '/' + ts_url
    else:  # 肯定有一个有/
        url = ts_host + ts_url
    try:
        if ts_body_method == 'none':
            response = requests.request(ts_method.upper(), url, headers=header, data={})
        
        elif ts_body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)
        
        elif ts_body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(ts_api_body):
                payload[i[0]] = i[1]
            response = requests.request(ts_method.upper(), url, headers=header, data=payload)
        
        else:  # 这时肯定是raw的五个子选项：
            if ts_body_method == 'Text':
                header['Content-Type'] = 'text/plain'
            
            if ts_body_method == 'JavaScript':
                header['Content-Type'] = 'text/plain'
            
            if ts_body_method == 'Json':
                header['Content-Type'] = 'text/plain'
            
            if ts_body_method == 'Html':
                header['Content-Type'] = 'text/plain'
            
            if ts_body_method == 'Xml':
                header['Content-Type'] = 'text/plain'
            response = requests.request(ts_method.upper(), url, headers=header, data=ts_api_body.encode('utf-8'))
        
        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        return HttpResponse(response.text)
    except Exception as e:
        return HttpResponse(str(e))


def get_home_log(request):
    """
    获取最新请求记录
    :param request:
    :return:
    """
    user_id = request.user.id
    all_logs = DB_apis_log.objects.filter(user_id=user_id)
    ret = {'all_logs': list(all_logs.values('id', 'api_method', 'api_host', 'api_url'))[::-1]}
    return HttpResponse(json.dumps(ret), content_type='application/json')


def get_api_log_home(request):
    """
    获取完整的单一的请求记录数据
    :param request:
    :return:
    """
    log_id = request.GET['log_id']
    log = DB_apis_log.objects.filter(id=log_id)
    ret = {"log": list(log.values())[0]}
    # print(ret)
    return HttpResponse(json.dumps(ret), content_type='application/json')

