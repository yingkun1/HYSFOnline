#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/25 12:08
@Author  : yingkun
@File    : adminx.py.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""
import xadmin

from .models import Course, Lesson, CourseResource, Video,BannerCourse
from organization.models import CourseOrg


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0



class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'get_zj_nums' ]
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students']
    list_editable = ['degree','desc']
    refresh_times = [3, 5]
    style_fields = {'detail': 'ueditor',}
    import_excel = True
    def queryset(self):
        qs = super(CourseAdmin,self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def post(self,request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin,self).post(request,args,kwargs)
    # 排序
    # ordering = ['-click_nums']
    # 隐藏
    # exclude = ['click_nums']
    #课程中嵌套章节和资源(无法实现)
    # inlines = [LessonInline,CourseResourceInline]

class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', ]
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students']

    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
