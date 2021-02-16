from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


def welcome(request):
    print('进入首页')
    # return HttpResponse('欢迎来到我的测试平台')
    return render(request,'welcome.html')

 # 返回子页面
def child(request,eid,oid):
    """
    eid，就是获取url中的 (?P<eid>.+) 的值，
    也就是我们welcome.html中的{{ whichHTML }} ，
    也就是我们后台函数返回的子页面html的真实名字
    :param request:
    :param eid:
    :param oid:
    :return:
    """
    return render(request,eid)


def home(request):
    # return render(request,'home.html',{'username':'赵丹丹'})
    return render(request,'welcome.html',{'whichHTML':'Home.html','oid':''})

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