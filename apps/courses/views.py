from django.shortcuts import render
from django.views.generic.base import View
from django.urls import reverse
from .models import *
from pure_pagination import PageNotAnInteger, Paginator
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
from django.http import HttpResponse


# Create your views here.
class CourseListView(View):
    def get(self, request):
        # 获取所有课程,默认以时间排序
        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课程推荐
        hot_courses = all_courses.order_by('-click_nums')[:3]
        # 按最热门与参与人数排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_courses = all_courses.order_by('-click_nums')
            elif sort == 'students':
                all_courses = all_courses.order_by('-students')

        # 分页处理,每页两个
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 2, request=request)
        courses = p.page(page)

        return render(request, 'course-list.html', {'all_courses': courses,
                                                    'sort': sort, 'hot_courses': hot_courses})


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 根据标签推荐课程
        tag = course.tag
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            elif UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {'course': course,
                                                      'relate_courses': relate_courses,
                                                      'has_fav_course': has_fav_course,
                                                      'has_fav_org': has_fav_org})


class CourseInfoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查询用户是否已经学过这个课程，如果没有，就关联起来
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            UserCourse.objects.create(user=request.user, course=course)  # 关联

        # 推荐其他人学习的课程
        # 找到学习这门课的所有人
        user_courses = UserCourse.objects.filter(course=course)
        # 获取这些人的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 获取他们所学的所有课程
        all_courses_ids = UserCourse.objects.filter(user_id__in=user_ids)
        # 按课程id获取课程，并按点击量取前五个
        relate_courses = Course.objects.filter(id__in=all_courses_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {'relate_courses': relate_courses,
                                                     'course': course,
                                                     'all_resources': all_resources})


# 视频播放
class VideoPlayView(LoginRequiredMixin, View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否已经学过这个课程，如果没有，就关联起来
        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            UserCourse.objects.create(user=request.user, course=course)  # 关联

        # 推荐其他人学习的课程
        # 找到学习这门课的所有人
        user_courses = UserCourse.objects.filter(course=course)
        # 获取这些人的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 获取他们所学的所有课程
        all_courses_ids = UserCourse.objects.filter(user_id__in=user_ids)
        # 按课程id获取课程，并按点击量取前五个
        relate_courses = Course.objects.filter(id__in=all_courses_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {'relate_courses': relate_courses,
                                                    'course': course,
                                                    'all_resources': all_resources,
                                                    'video': video})


class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        # 由课程获取评论
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()

        # 推荐其他人学习的课程
        # 找到学习这门课的所有人
        user_courses = UserCourse.objects.filter(course=course)
        # 获取这些人的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 获取他们所学的所有课程
        all_courses_ids = UserCourse.objects.filter(user_id__in=user_ids)
        # 按课程id获取课程，并按点击量取前五个
        relate_courses = Course.objects.filter(id__in=all_courses_ids).order_by('-click_nums')[:5]
        return render(request, 'course-comment.html',
                      {'relate_courses': relate_courses, 'course': course, 'all_resources': all_resources,
                       'all_comments': all_comments})


class AddCommentsView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponse({"status": "fail", "msg": "用户未登录"}, content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments')
        if int(course_id) and comments:
            # 获取评论的哪门课程
            course = Course.objects.get(id=int(course_id))
            CourseComments.objects.create(user=request.user, course=course, comments=comments)
            return HttpResponse({"status": "success", "msg": "评论成功"}, content_type='application/json')
        else:
            return HttpResponse({"status": "fail", "msg": "评论失败"}, content_type='application/json')
