from django.shortcuts import render, redirect, HttpResponse
from django.contrib import auth
from django.urls import reverse
from users.forms import *
from django.contrib.auth.backends import ModelBackend
from users.models import *
from django.db.models import Q, F
from django.views.generic.base import View


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
