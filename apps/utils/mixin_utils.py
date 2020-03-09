#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/9 15:17
@Author  : yingkun
@File    : mixin_utils.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)