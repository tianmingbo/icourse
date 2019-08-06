__author__ = '田明博'
__date__ = '2019/8/6 8:09'
from django import forms
from django.core.exceptions import ValidationError
from users.models import *


# 使用form组件
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


# 自定义注册
class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label='用户名',
        error_messages={
            "max_length": "用户名最长为16",
            "required": "用户名不能为空"
        },
        widget=forms.widgets.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    password = forms.CharField(
        min_length=6,
        label='密码',
        error_messages={
            "min_length": "密码最短为6",
            "required": "密码不能为空"
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control'},
            render_value=True
        )
    )

    re_password = forms.CharField(
        min_length=6,
        label='确认密码',
        error_messages={
            "min_length": "确认密码最短为6",
            "required": "确认密码不能为空"
        },
        widget=forms.widgets.PasswordInput(
            attrs={'class': 'form-control'},
            render_value=True
        )
    )

    email = forms.CharField(
        label='邮箱',
        error_messages={
            "invalid": "邮箱格式不正确",
            "required": "邮箱不能为空"
        },
        widget=forms.widgets.EmailInput(
            attrs={'class': 'form-control'},
        )
    )

    # 自定义校验规则，在相应的字段前加 clean_ 方法
    # 校验姓名
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = UserProfile.objects.filter(username=username)
        if is_exist:
            # 表示用户已经注册
            self.add_error("username", ValidationError("用户名已存在"))
        else:
            return username

    # 校验email
    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exist = UserProfile.objects.filter(email=email)
        if is_exist:
            # 表示邮箱已经注册
            self.add_error("email", ValidationError("邮箱已存在"))
        else:
            return email

    # 重写全局的钩子函数，对确认密码做校验
    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")

        if re_password and re_password != password:
            self.add_error("re_password", ValidationError("两次密码不一致"))
        else:
            return self.cleaned_data
