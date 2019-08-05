import xadmin
from .models import *


class UserAskConfig(object):  # 定制显示列
    list_display = ['name', 'mobile', 'course_name', 'add_time']
    search_fields = ['name', 'mobile', 'course_name']
    list_filter = ['name', 'mobile', 'course_name', 'add_time']


class CourseCommentsConfig(object):  # 定制显示列
    list_display = ['user', 'course', 'comments', 'add_time']
    search_fields = ['user', 'course', 'comments']
    list_filter = ['user', 'course', 'comments', 'add_time']


class UserFavoriteConfig(object):  # 定制显示列
    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']


class UsrMessageConfig(object):  # 定制显示列
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']


class UserCourseConfig(object):  # 定制显示列
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']


# xadmin.site.register(UserProfile)
xadmin.site.register(UserAsk, UserAskConfig)
xadmin.site.register(CourseComments, CourseCommentsConfig)
xadmin.site.register(UserFavorite, UserFavoriteConfig)
xadmin.site.register(UserMessage, UsrMessageConfig)
xadmin.site.register(UserCourse, UserCourseConfig)
