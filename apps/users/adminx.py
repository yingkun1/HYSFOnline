#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/24 21:59
@Author  : yingkun
@File    : adminx.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""

import xadmin

from xadmin import views
from .models import EmailVerifyRecord, Banner

# 启动主题，网速太卡，建议使用默认
# class BaseSetting(object):
#     enable_themes = True
#     use_bootswatch = True


class GlobalSettings(object):
    site_title = '衡师在线后台管理'
    site_footer = '衡师在线网'
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']


class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
# 启动主题，网速太卡，建议默认
# xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
