#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/6 18:33
@Author  : yingkun
@File    : urls.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""
from django.conf.urls import url,include
from  .views import CourseListView

urlpatterns = [
    # 课程相关列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
]