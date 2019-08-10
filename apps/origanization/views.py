from django.shortcuts import render
from django.views.generic.base import View
from .models import *
from pure_pagination import PageNotAnInteger, Paginator
from .forms import *
from django.http import HttpResponse
from operation.models import UserFavorite
from courses.models import Course
from django.db.models import Q


# Create your views here.
class OrgView(View):
    '''
    课程机构
    '''

    def get(self, request):
        # 所有机构
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        # 所有城市
        all_citys = CityDict.objects.all()

        # 搜索
        keyword = request.GET.get('keywords', '')
        if keyword:
            # i表示忽略大小写
            all_orgs = all_orgs.filter(
                Q(name__icontains=keyword) | Q(desc__icontains=keyword))

        # 类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 热门机构排名，按照点击次数降序
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 按照机构的学习人数或者课程数排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_orgs = all_orgs.order_by('-students')
        elif sort == 'courses':
            all_orgs = all_orgs.order_by('-course_nums')

        # 分页处理,每页两个
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 2, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html',
                      {
                          'all_orgs': orgs,
                          'all_citys': all_citys,
                          'org_nums': org_nums,
                          'hot_orgs': hot_orgs,
                          'category': category,
                          # 传回sort和city_id，目的是为了判断选中状态，增加active属性
                          'sort': sort,
                          'city_id': city_id,
                      })


class AskView(View):
    '''
    用户添加咨询，只有post请求
    '''

    def post(self, request):
        use_post = UserAskForm(request.POST)  # 实例化
        if use_post.is_valid():
            use_post.save(commit=True)  # 当commit为True，可以直接把提交的数据保存在数据库
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    def get(self, request, org_id):
        current_page = 'home'
        # 找到这个机构有哪些课程、教师、讲师有什么课
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 反向查找课程和讲师
        all_courses = course_org.course_set.all()[:4]
        all_teacher = course_org.teacher_set.all()[:2]
        return render(request, 'org-detail-home.html', {'course_org': course_org,
                                                        'all_courses': all_courses,
                                                        'all_teacher': all_teacher,
                                                        'current_page': current_page,
                                                        'has_fav': has_fav})


class OrgCourseView(View):
    def get(self, request, org_id):

        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 反向查找课程
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:4]
        return render(request, 'org-detail-course.html', {'course_org': course_org,
                                                          'all_courses': all_courses,
                                                          'current_page': current_page,
                                                          'has_fav': has_fav})


class OrgDescView(View):
    def get(self, request, org_id):

        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {'course_org': course_org,

                                                        'current_page': current_page,
                                                        'has_fav': has_fav})


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 反向查找课程
        all_teacher = course_org.teacher_set.all()[:2]
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {'course_org': course_org,
                                                            'all_teacher': all_teacher,
                                                            'current_page': current_page,
                                                            'has_fav': has_fav})


class AddFavView(View):
    def post(self, request):
        id = request.POST.get('fav_id', 0)
        type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated:
            # 未登录
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(id), fav_type=int(type))
        if exist_record:
            # 用户已经收藏过，再点击表示取消收藏
            exist_record.delete()
            return HttpResponse({"status": "success", "msg": "收藏"}, content_type='application/json')
        else:
            UserFavorite.objects.create(user=request.user, fav_id=int(id), fav_type=int(type))  # 不存在则创建
            return HttpResponse({"status": "success", "msg": "已收藏"}, content_type='application/json')


class TeacherListView(View):
    def get(self, request):
        all_teachers = Teacher.objects.all()
        sort = request.GET.get('sort', '')
        teacher_nums = all_teachers.count()

        # 搜索
        keyword = request.GET.get('keywords', '')
        if keyword:
            # i表示忽略大小写
            all_teachers = all_teachers.filter(
                Q(name__icontains=keyword) | Q(work_position__icontains=keyword))
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')[:3]
        # 讲师排行榜
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # 分页处理
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 2, request=request)
        teachers = p.page(page)

        return render(request, 'teachers-list.html',
                      {'all_teachers': teachers,
                       'teacher_nums': teacher_nums,
                       'sorted_teacher': sorted_teacher})


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        all_course = Course.objects.filter(teacher=teacher)
        sorted_teacher = Teacher.objects.all().order_by('-click_nums')[:3]
        # 教师和机构是否收藏
        has_teacher_faved = False
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True
        elif UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True
        return render(request, 'teacher-detail.html',
                      {'teacher': teacher,
                       'all_course': all_course,
                       'sorted_teacher': sorted_teacher,
                       'has_teacher_faved': has_teacher_faved,
                       'has_org_faved': has_org_faved})
