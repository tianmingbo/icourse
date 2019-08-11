__author__ = '田明博'
__date__ = '2019/8/6 8:09'
from django import forms
from django.core.exceptions import ValidationError
from users.models import UserProfile
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


# 忘记密码
class ForgetForm(forms.Form):
    email = forms.CharField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(min_length=6)
    password2 = forms.CharField(min_length=6)


class UploadImageForm(forms.ModelForm):
    '''用户更改图像'''

    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    '''个人中心信息修改'''

    class Meta:
        model = UserProfile
        fields = ['nick_name', 'gender', 'birthday', 'address', 'mobile']

