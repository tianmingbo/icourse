import xadmin
from .models import *


class CourseConfig(object):  # 定制显示列
    list_display = ['name', 'desc', 'degree', 'students']
    search_fields = ['name', 'desc', 'degree', 'students']
    list_filter = ['name', 'desc', 'degree', 'students']


class LessonConfig(object):  # 定制显示列
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']


class VideoConfig(object):  # 定制显示列
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceConfig(object):  # 定制显示列
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


# xadmin.site.register(UserProfile)
xadmin.site.register(Course, CourseConfig)
xadmin.site.register(Lesson, LessonConfig)
xadmin.site.register(Video, VideoConfig)
xadmin.site.register(CourseResource, CourseResourceConfig)
