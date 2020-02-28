#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/28 12:09
@Author  : yingkun
@File    : forms.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""

from django import forms
from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)

class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captcha = CaptchaField()

