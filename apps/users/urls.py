__author__ = '田明博'
__date__ = '2019/8/10 9:02'

from django.conf.urls import url
from .views import *

urlpatterns = [
    # 用户信息
    url(r'^info/', InfoView.as_view(), name='user_info'),
    # 修改头像
    url(r'^image/upload/', UploadImageView.as_view(), name='image_upload'),
    # 修改密码
    url(r'^update/pwd/', UpdatePwdView.as_view(), name='update_pwd'),
    # 发送邮箱验证码
    url(r'^sendemail_code/', SendEmailView.as_view(), name='sendemail_code'),
    # 修改邮箱
    url(r'^update_email/', UpdateEmailView.as_view(), name='update_email'),
    # 我的课程
    url(r'^mycourse/', MyCourseView.as_view(), name='mycourse'),
    # 我的收藏下
    url(r'^my_fav/course/', MyFavCourseView.as_view(), name='myfav_course'),
    url(r'^my_fav/org/', MyFavOrgView.as_view(), name='myfav_org'),
    url(r'^my_fav/teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),

    # 我的消息
    url(r'^my_message/', MyMessageView.as_view(), name='my_message'),
]
