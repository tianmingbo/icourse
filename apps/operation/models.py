from django.db import models

from datetime import datetime

from users.models import UserProfile
from courses.models import Course

# Create your models here.
'''
UserAsk         --用户咨询
CourseComments  --用户评论
UserFavorite    ==用户收藏
UserMessage      --用户消息
UserCourse      --用户学习的课程
'''


class UserAsk(models.Model):
    name = models.CharField('姓名', max_length=20)
    mobile = models.CharField('手机', max_length=11)
    course_name = models.CharField('课程名', max_length=50)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户咨询'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户')
    course = models.ForeignKey(Course, verbose_name='课程')
    comments = models.CharField('评论', max_length=200)
    add_time = models.DateTimeField('时间', default=datetime.now)

    class Meta:
        verbose_name = '课程评论'
        verbose_name_plural = verbose_name


class UserFavorite(models.Model):
    fav_type = (
        (1, '课程'),
        (2, '课程机构'),
        (3, '讲师')
    )

    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    fav_id = models.IntegerField('数据id', default=0)
    fav_type = models.IntegerField(verbose_name='收藏类型', choices=fav_type, default=1)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField('接收用户', default=0)  # 默认发所有用户，>0表示用户id
    message = models.CharField('消息内容', max_length=500)
    has_read = models.BooleanField('是否已读', default=False)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    add_time = models.DateTimeField('添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户课程'
        verbose_name_plural = verbose_name
