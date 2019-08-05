import xadmin
from xadmin import views
from .models import *


class BaseSetting(object):
    enable_themes = True  # 开启主题功能
    use_bootswatch = True


# 全局修改，固定写法
class GlobalSettings(object):
    # 修改title
    site_title = '明博定制版后台管理系统'
    # 修改footer
    site_footer = '明博的公司'
    # 设置可以收起菜单
    menu_style = 'accordion'


class EmailVerifyRecordConfig(object):  # 定制显示列
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']  # 搜索
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerConfig(object):  # 定制显示列
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']  # 搜索
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# xadmin.site.register(UserProfile)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordConfig)
xadmin.site.register(Banner, BannerConfig)

# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView, BaseSetting)

# 将title和footer信息进行注册
xadmin.site.register(views.CommAdminView, GlobalSettings)
