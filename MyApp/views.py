from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from MyApp.models import *

# Create your views here.


def welcome(request):
    print('进入首页')
    # return HttpResponse('欢迎来到我的测试平台')
    return render(request,'welcome.html')

#控制不同页面返回不同数据:数据分发器
def child_json(eid,oid=''):
    """
    child_json()  它专门用来接收页面名字，然后去不同的数据库中查找数据，
    进行整理后 返回给child()函数，再由child函数返回给前端浏览器
    :param eid:
    :return:
    """
    res = {}
    if eid == 'home.html': #首页的超链接
        data = DB_home_href.objects.all()
        res = {"hrefs": data}

    if eid == 'project_list.html': # 首页的项目列表
        data = DB_project.objects.all()
        res = {'projects':data}

    if eid=='P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project':project}
    if eid=='P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project':project}
    if eid=='P_project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project':project}

    return res

 # 返回子页面
def child(request,eid,oid):
    """
    eid，就是获取url中的 (?P<eid>.+) 的值，
    也就是我们welcome.html中的{{ whichHTML }} ，
    也就是我们后台函数返回的子页面html的真实名字
    :param request:
    :param eid: 进入的html文件名
    :param oid:
    :return:
    """
    res = child_json(eid,oid)

    return render(request,eid,res)


def home(request):
    # return render(request,'home.html',{'username':'赵丹丹'})
    return render(request,'welcome.html',{'whichHTML':'home.html','oid':''})

def login(request):
    return render(request,'login.html')

#开始登陆
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
        return HttpResponse('失败') # 用户名+密码错误

def register_action(request):
    """

    :param request:
    :return:
    """
    u_name = request.GET['username']
    p_word = request.GET['password']

    print('注册用户名密码：',u_name+'\n'+p_word)


    # from django.contrib.auth.hashers import make_password
    try:
        user = User.objects.create(username=u_name,password=p_word)
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
    DB_tucao.objects.create(user=request.user.username,text=tucao_text)
    return HttpResponse('')

def api_help(request):
    """
    进入帮助文档函数
    :param request:
    :return:
    """
    return render(request,'welcome.html',{'whichHTML':'help.html','oid':''})

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
    project_name=request.GET['project_name']
    DB_project.objects.create(name=project_name,remark='',user=request.user,other_user='')
    return HttpResponse('')

def open_apis(request,id):
    """

    :param request:
    :return:
    """
    project_id = id
    return render(request,'welcome.html',{'whichHTML':'P_apis.html','oid':project_id})

def open_cases(request,id):
    """

    :param request:
    :return:
    """
    project_id = id
    return render(request, 'welcome.html', {'whichHTML': 'P_cases.html', 'oid': project_id})

def open_project_set(request,id):
    """

    :param request:
    :return:
    """
    project_id = id
    return render(request, 'welcome.html', {'whichHTML': 'P_project_set.html', 'oid': project_id})

def save_project_set(request,id):
    """

    :param request:
    :return:
    """
    project_id = id
    name = request.GET['name']
    remark = request.GET['remark']
    other_user = request.GET['other_user']

    DB_project.objects.filter(id=project_id).update(name=name,remark=remark,other_user=other_user)

    return HttpResponse('')

