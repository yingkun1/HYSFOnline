#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/11 14:33
@Author  : yingkun
@File    : urls.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""
from django.conf.urls import url,include
from .views import UserInfoView,UploadImageView
urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'^image/upload/$',UploadImageView.as_view(),name='image_upload')
]