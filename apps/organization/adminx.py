#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/25 12:50
@Author  : yingkun
@File    : adminx.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""
import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'fav_nums']
    search_fields = ['name', 'desc', 'click_nums', 'fav_nums']
    list_filter = ['name', 'desc', 'click_nums', 'fav_nums']


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_year', 'work_company']
    search_fields = ['org', 'name', 'work_year', 'work_company']
    list_filter = ['org', 'name', 'work_year', 'work_company']


xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
