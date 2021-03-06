from django.db import models
from datetime import datetime
from origanization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField

# Create your models here.
'''
课程中需要四张表
Course  课程表
Lesson  章节信息
Video    视频资源
CourseResource  课程资源
'''


class Course(models.Model):
    degree_choices = (('cj', '初级'), ('zj', '中级'), ('gj', '高级'))

    name = models.CharField('课程名', max_length=50)
    desc = models.CharField('课程描述', max_length=300)
    detail = UEditorField(verbose_name=u'课程详情', width=600, height=300, imagePath="courses/ueditor/",
                          filePath="courses/ueditor/", default='')
    degree = models.CharField('难度', max_length=2, choices=degree_choices)
    learn_times = models.IntegerField('学习时长（分钟）', default=0)
    students = models.IntegerField('学习人数', default=0)
    fav_nums = models.IntegerField('收藏人数', default=0)
    image = models.ImageField('封面图', upload_to='course/%Y/%m', max_length=100)
    click_nums = models.IntegerField('点击数', default=0)
    add_time = models.DateTimeField("添加时间", default=datetime.now, )
    is_banner = models.BooleanField('轮播课程', default=False)
    tag = models.CharField('课程标签', default='', max_length=10)
    category = models.CharField('课程类别', default='', max_length=20)
    you_need_know = models.CharField('课程须知', max_length=300, default='')
    teacher_tell = models.CharField('老师告诉你', max_length=300, default='')

    # 课程属于哪个机构
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, verbose_name='讲师', null=True, blank=True)

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取这门课程的所有学习者，反向查询
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    # 获取章节数
    def get_zj_nums(self):
        return self.lesson_set.all().count()

    # 获取所有课程
    def get_course_lesson(self):
        return self.lesson_set.all()

    get_zj_nums.short_description = "章节数"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.projectsedu.com'>跳转</>")

    go_to.short_description = "跳转"


class Lesson(models.Model):
    '''课程章节'''
    course = models.ForeignKey(Course, verbose_name='课程', on_delete=models.CASCADE)
    name = models.CharField("章节名", max_length=100)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取章节视频
    def get_lesson_vedio(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField("视频名", max_length=100)
    url = models.CharField('访问地址', max_length=200, default='')
    learn_times = models.IntegerField('学习时长（分钟）', default=0)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BannerCourse(Course):
    '''显示轮播课程'''

    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        # 这里必须设置proxy=True，这样就不会在生成一张表，而且具有Model的功能
        proxy = True


class CourseResource(models.Model):
    # 课程资源
    course = models.ForeignKey(Course, verbose_name="课程", on_delete=models.CASCADE)
    name = models.CharField("名称", max_length=100)
    download = models.FileField("资源文件", upload_to="course/resource/%Y/%m", max_length=100)
    add_time = models.DateTimeField("添加时间", default=datetime.now)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
