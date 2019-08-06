__author__ = '田明博'
__date__ = '2019/8/6 8:09'
from django import forms
from django.core.exceptions import ValidationError
from users.models import *
from captcha.fields import CaptchaField


# 使用form组件
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


# 自定义注册
class RegisterForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True, max_length=6)
    captcha = CaptchaField(error_messages={
        'invalid': '验证码错误'
    })
