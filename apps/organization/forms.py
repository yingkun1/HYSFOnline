#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/3/5 15:17
@Author  : yingkun
@File    : forms.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""
import re
from django import forms
from operation.models import UserAsk

class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile','course_name']

    def clean_mobile(self):
        """
        验证手机号码是否合法
        """
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code='mobile_invalid')
