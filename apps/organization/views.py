# *_* coding:utf-8 *_*
from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class OrgView(View):
    def get(self,request):
        all_orgs = CourseOrg.objects.all()
        org_nums = all_orgs.count()
        all_citys = CityDict.objects.all()
        # 城市筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id = int(city_id))
        #类别筛选
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category = category)

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
            'category':category
        })
