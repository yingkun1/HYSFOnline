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
from .views import UserInfoView,UploadImageView,UpdatePwdView,SendEmialCodeView,UpdateEmailView,MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MyMessageView
urlpatterns = [
    # 用户信息
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    # 用户头像上传
    url(r'^image/upload/$',UploadImageView.as_view(),name='image_upload'),
    # 用户个人中心修改密码
    url(r'^update/pwd/$',UpdatePwdView.as_view(),name='update_pwd'),
    # 获取邮箱验证码
    url(r'^sendemail_code/$',SendEmialCodeView.as_view(),name='sendemail_code'),
    # 修改邮箱
    url(r'^update_email/$',UpdateEmailView.as_view(),name='update_email'),
    # 我的课程
    url(r'^mycourse/$',MyCourseView.as_view(),name='mycourse'),
    # 我收藏的课程机构
    url(r'^myfav/org$',MyFavOrgView.as_view(),name='myfav_org'),
    # 我收藏的教师
    url(r'^myfav/teacher$',MyFavTeacherView.as_view(),name='myfav_teacher'),
    # 我收藏的课程
    url(r'^myfav/course$',MyFavCourseView.as_view(),name='myfav_course'),
    # 我的消息
    url(r'^mymessage/$',MyMessageView.as_view(),name='mymessage')
]