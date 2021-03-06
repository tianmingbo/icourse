"""icourse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""

from users.views import IndexView, LoginView, LogoutView, RegisterView, ActiveUserView, ForgetView, ResetView, \
    ModifyPwdView
import xadmin
from icourse.settings import MEDIA_ROOT, STATIC_ROOT
from django.views.static import serve  # 处理图片
from django.conf.urls import include, url

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),  # 验证码
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),  # 用户激活,active_code是传递的参数
    url(r'^forget/$', ForgetView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),  # 重置密码链接
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),  # 修改密码链接
    # 处理图片显示的url,使用Django自带serve,传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    url(r'^media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),
    # 静态文件配置，当debug为False时
    # url(r'^static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
    # 课程机构
    url(r'^org/', include('origanization.urls', namespace='org')),
    # 课程功能
    url(r'^courses/', include('courses.urls', namespace='courses')),
    # 个人中心
    url(r'^uses/', include('users.urls', namespace='users')),
    # 富文本相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]

# if settings.DEBUG:
#     import debug_toolbar
#
#     urlpatterns = [
#                       url(r'^__debug__/', include(debug_toolbar.urls)),
#                   ] + urlpatterns

# 全局404页面配置
handler404 = 'users.views.page_not_found'
# 全局500页面配置
handler500 = 'users.views.page_error'
