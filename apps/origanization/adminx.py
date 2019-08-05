import xadmin
from .models import *

'''
外键在过滤器中不会出现，需要加 __实现，如course__name
'''


class CourseOrgConfig(object):  # 定制显示列
    list_display = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums', 'address', 'city', 'add_time']


class TeacherConfig(object):  # 定制显示列
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                    'teacher_age', 'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                     'teacher_age']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',
                   'teacher_age', 'add_time']


class CityDictConfig(object):  # 定制显示列
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


# xadmin.site.register(UserProfile)
xadmin.site.register(CourseOrg, CourseOrgConfig)
xadmin.site.register(Teacher, TeacherConfig)
xadmin.site.register(CityDict, CityDictConfig)
