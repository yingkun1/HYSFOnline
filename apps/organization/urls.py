#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/5 15:32
@Author  : yingkun
@File    : urls.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""
from django.conf.urls import url,include
from .views import OrgView, AddUserAskView,OrgHomeView

urlpatterns = [
    # 课程机构列表页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$',AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$',OrgHomeView.as_view(),name='org_home')
]