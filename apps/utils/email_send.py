__author__ = '田明博'
__date__ = '2019/8/6 15:43'
from django.shortcuts import render
from django.core.mail import send_mail  # 发邮件
from users.models import *
from icourse.settings import EMAIL_FROM
import uuid


# 获取随机字符串
def get_random(length=8):
    random = str(uuid.uuid1())
    code = random[0:length]
    return code


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = get_random(4)
        code = code.replace('-', '')  # 去除横杠
    else:
        code = get_random(16)
        code = code.replace('-', '')
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""
    if send_type == 'register':
        email_title = "icourse注册激活"
        email_body = "请点击下面的链接激活你的账号"
        email_url = "http://127.0.0.1:8000/active/{0}".format(code)  # 忘写端口了，我套
        # send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])  # 邮件发送不成功，自己写个页面，进行验证
        # if send_status:
        #     pass
        return email_body, email_title, email_url

    elif send_type == 'forget':
        email_title = "icourse重置密码"
        email_body = "请点击下面的链接重置密码"
        email_url = "http://127.0.0.1:8000/reset/{0}".format(code)
        return email_body, email_title, email_url
