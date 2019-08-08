__author__ = '田明博'
__date__ = '2019/8/8 9:54'
import re
from django import forms
from operation.models import UserAsk


# 使用ModelForm组件
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):  # 钩子函数，clean(),不加字段，可以全局校验,验证手机号是否合法
        mobile = self.cleaned_data['mobile']
        rule = '^1([38]\d|5[0 - 35 - 9]|7[3678])\d{8}$'
        p = re.compile(rule)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号非法', code='mobile_invalid')
