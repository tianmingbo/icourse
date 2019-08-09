__author__ = '田明博'
__date__ = '2019/8/8 8:27'
from django.conf.urls import url
from origanization.views import *

app_name = 'origanization'  # 写上app的名字

urlpatterns = [
    url(r'^list/', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/', AskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),

    # 收藏
    url(r'^add_fav/', AddFavView.as_view(), name='add_fav'),
    # 教师列表
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    # 教师详情页
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail'),

]
