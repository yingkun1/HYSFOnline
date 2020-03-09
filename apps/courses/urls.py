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
from  .views import CourseListView, CourseDetailView,CourseInfoView,CourseCommentView,AddCommentsView

urlpatterns = [
    # 课程相关列表页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详情页面
    # url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(),name='course_detail'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(),name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(),name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(),name='course_comments'),
    # 添加课程评论
    url(r'^add_comment/$', AddCommentsView.as_view() ,name='add_comment'),

]