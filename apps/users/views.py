from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.urls import reverse
from users.forms import *
from django.contrib.auth.backends import ModelBackend
from users.models import *
from django.db.models import Q, F
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from utils.email_send import *


# Create your views here.
# 设置邮箱和用户名都可以登录，重载authenticate方法
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))  # 或
            # 密码为密文
            # AbstractUser中有check_password方法
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class IndexView(View):
    def get(self, request):
        return HttpResponse('这是主页')


# 基于类CBV
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)  # 使用forms组件进行格式校验
        if login_form.is_valid():  # 如果合法
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = auth.authenticate(username=username, password=password)
            # 使用auth组件进行校验用户信息
            if user is not None:
                auth.login(request, user)  # 注册用户后才能使用
                return redirect(reverse('index'))
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect(reverse('index'))


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', locals())

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 校验通过
            email = request.POST.get('email')
            pwd = request.POST.get('password')
            # 检查这个用户名是否已经注册过
            flag = UserProfile.objects.filter(email=email)
            if flag:
                return render(request, 'register.html', {'register_form': register_form, 'msg': '用户已经注册'})
            # 密码加密
            pwd = make_password(pwd)
            # 创建新用户
            print(email, pwd)
            UserProfile.objects.create(username=email, email=email, is_active=False, password=pwd)
            # 发送注册邮件
            send_register_email(request, email, 'register')
            # return redirect(reverse('login'))
        return render(request, 'register.html', locals())


# 用户状态激活
class ActiveUserView(View):
    def get(self, request, active_code):
        obj = EmailVerifyRecord.objects.filter(code=active_code).first()
        if obj:
            # 获取要激活的用户名
            email = obj.email
            # 用户激活
            UserProfile.objects.get(email=email).update(is_active=True)
        else:
            return render(request, 'register.html')
        return render(request, 'login.html')
