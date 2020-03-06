# *_* coding:utf-8 *_*
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .forms import UserAskForm
from operation.models import UserFavorite
from courses.models import Course
import json
# Create your views here.

class OrgView(View):
    def get(self,request):
        all_orgs = CourseOrg.objects.all()
        all_citys = CityDict.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:6]
        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id = int(city_id))
        #类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category = category)

        sort = request.GET.get('sort')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')[:5]
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')[:5]
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort
        })


class AddUserAskView(View):
    """
    用户添加咨询
    """
    def post(self,request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            data = {'status':'success'}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data = {'status':'fail', 'msg':'添加出错'}
            return HttpResponse(json.dumps(data),content_type="application/json")


class OrgHomeView(View):
    def get(self,request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id =int(org_id))
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:2]
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })

class OrgCourseView(View):
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id =int(org_id))
        all_courses = course_org.course_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })


class OrgDescView(View):
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id =int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })


class OrgTeacherView(View):
    def get(self,request,org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id =int(org_id))
        all_teachers = course_org.teacher_set.all()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-teachers.html',{
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav
        })

class AddFavView(View):
    """
    用户收藏，用户取消收藏功能
    """
    def post(self,request):
        fav_id = request.POST.get('fav_id', '')
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            data = {'status':'fail', 'msg':'用户未登录'}
            return HttpResponse(json.dumps(data),content_type="application/json")
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #如果存在这条数据，标识用户希望取消收藏
            exist_records.delete()
            data = {'status':'success', 'msg':'收藏'}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            user_fav = UserFavorite()
            if int(fav_id) >0 and int(fav_type) >0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                data = {'status':'success', 'msg':'已收藏'}
                return HttpResponse(json.dumps(data),content_type="application/json")
            else:
                data = {'status':'fail', 'msg':'收藏出错'}
                return HttpResponse(json.dumps(data),content_type="application/json")


