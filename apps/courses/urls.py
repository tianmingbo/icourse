__author__ = '田明博'
__date__ = '2019/8/9 8:05'

from django.conf.urls import url
from courses.views import *

app_name = 'courses'  # 写上app的名字

urlpatterns = [
    # 课程列表
    url(r'^list/', CourseListView.as_view(), name='course_list'),
    # 课程详情
    url(r'^detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
    # 课程章节信息页
    url(r'^info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name='course_info'),
    # 课程视频播放
    url(r'^video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name='video_play'),
    # 评论
    url(r'^comments/(?P<course_id>\d+)/', CommentsView.as_view(), name='course_comments'),
    #添加评论
    url(r'^add_comment/', AddCommentsView.as_view(), name='add_comment'),
]
