__author__ = '田明博'
__date__ = '2019/8/9 11:02'
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))  # 判断用户是否登录
    def dispath(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispath(request, *args, **kwargs)
