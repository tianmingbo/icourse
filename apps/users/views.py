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
from django.utils.safestring import mark_safe


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
        return render(request,'index.html')


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
                if user.is_active:
                    auth.login(request, user)  # 注册用户后才能使用
                    return redirect(reverse('index'))
                else:
                    return render(request, "login.html", {"msg": "用户未激活！"})
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
            # print(email, pwd)
            UserProfile.objects.create(username=email, email=email, is_active=False, password=pwd)
            # 发送注册邮件
            email_body, email_title, email_url = send_register_email(email, 'register')
            # return redirect(reverse('login'))
            a = mark_safe("{0}<a href='{1}'>{2}</a>".format(email_body, email_url, email_url))
            return render(request, 'active.html', locals())
        return render(request, "register.html", {"register_form": register_form})


# 用户状态激活
class ActiveUserView(View):
    def get(self, request, active_code):
        obj = EmailVerifyRecord.objects.filter(code=active_code).first()
        if obj:
            # 获取要激活的用户名
            email = obj.email
            # 用户激活
            use_obj = UserProfile.objects.filter(email=email).first()
            use_obj.is_active = True
            use_obj.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


# 找回密码
class ForgetView(View):
    def get(self, request):
        forget_form = ForgetForm()
        print('in get')
        return render(request, 'forgetpwd.html', locals())


    def post(self, request):
        forget_form = ForgetForm(request.POST)
        print('in post')
        if forget_form.is_valid():
            print('dfadf')
            email = request.POST.get('email')
            email_body, email_title, email_url = send_register_email(email, 'forget')
            # 生成链接
            a = mark_safe("{0}<a href='{1}'>{2}</a>".format(email_body, email_url, email_url))
            return render(request, 'reset_link.html', locals())

        return render(request, 'forgetpwd.html', locals())  # 提交数据的格式不正确，重新提交


class ResetView(View):
    # 点击重置密码链接，进入此逻辑，返回重置密码页面
    def get(self, request, active_code):
        obj = EmailVerifyRecord.objects.filter(code=active_code).first()  # 找到有没有重置密码的对象
        if obj:
            email=obj.email
            return render(request, 'password_reset.html', locals())  # 返回重置密码页面
        else:
            return render(request, 'register.html')


# 修改密码
class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            email = request.POST.get('email')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user_obj = UserProfile.objects.filter(email=email).first()
            user_obj.password = make_password(pwd1)
            user_obj.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email')
            return render(request,'password_reset.html',locals())