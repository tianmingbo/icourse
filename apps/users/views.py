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
import json
from utils.mixin_utils import LoginRequiredMixin


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
        return render(request, 'index.html')


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
            email = obj.email
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
            return render(request, 'password_reset.html', locals())


class InfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        user_info = UserInfoForm(request.POST, instance=request.user)
        if user_info.is_valid():
            user_info.save()
            return HttpResponse({"status": "success"}, content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info.errors), content_type='application/json')


class UploadImageView(View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return HttpResponse({"status": "success"}, content_type='application/json')
        else:
            return HttpResponse({"status": "fail"}, content_type='application/json')


class UpdatePwdView(View):
    def post(self, request):
        modify_forms = ModifyPwdForm(request.POST)
        if modify_forms.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse({"status": "fail", "msg": "密码不一致"}, content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse({"status": "success"}, content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_forms.errors), content_type='application/json')


class SendEmailView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        email_body, email_title, email_url = send_register_email(email, 'update_email')
        a = mark_safe("{0}<a href='{1}'>{2}</a>".format(email_body, email_url, email_url))
        return render(request, 'reset_link.html', locals())


class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        flag = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if flag:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


from operation.models import UserFavorite, UserCourse, UserMessage
from courses.models import Course, CourseOrg, Teacher
from pure_pagination import Paginator, PageNotAnInteger


class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        course_list = UserCourse.objects.filter(user=user)
        return render(request, 'usercenter-mycourse.html', {'course_list': course_list})


class MyFavCourseView(View):
    def get(self, request):
        course_list = []
        user = request.user
        like_courses = UserFavorite.objects.filter(user=user, fav_type=1)
        # 遍历所有
        for i in like_courses:
            # 找到每一个课程的id
            course_id = i.fav_id
            # 找到所有课程对象
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html',
                      {'course_list': course_list})


class MyFavOrgView(View):
    def get(self, request):
        org_list = []
        user = request.user
        like_orgs = UserFavorite.objects.filter(user=user, fav_type=2)
        # 遍历所有
        for i in like_orgs:
            # 找到每一个课程的id
            org_id = i.fav_id
            # 找到所有机构对象
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html', {'org_list': org_list})


class MyFavTeacherView(View):
    def get(self, request):
        teacher_list = []
        user = request.user
        like_teachers = UserFavorite.objects.filter(user=user, fav_type=3)
        # 遍历所有
        for i in like_teachers:
            teacher_id = i.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html', {'teacher_list': teacher_list})


class MyMessageView(View):
    def get(self, request):
        user = request.user
        all_message = UserMessage.objects.filter(user=user.id)
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 4, request=request)
        messages = p.page(page)
        return render(request, 'usercenter-message.html', {'message': messages})
