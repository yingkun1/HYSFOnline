#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/29 14:10
@Author  : yingkun
@File    : email_send.py
@Software: PyCharm
@contact: 925712087@qq.com
@desc:
"""
from random import Random
from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from HYSFOnline.settings import EMAIL_FROM


def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    email_record.send_type = send_type
    if send_type == 'update_email':
        random_str = generate_random_str(4)
    else:
        random_str = generate_random_str(16)
    email_record.code = random_str
    email_record.email= email

    if send_type == 'register':
        email_title = u'衡师在线网注册激活链接'
        email_body = u'请点击下面的的链接激活你的账号:http://101.132.138.215/active/{0}'.format(email_record.code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        print send_status
        print u'发送邮件成功'
        if send_status:
            email_record.save()

    if send_type == 'forget':
        email_title = u'衡师在线网密码重置链接'
        email_body = u'请点击下面的的链接重置你的密码:http://101.132.138.215/reset/{0}'.format(email_record.code)
        print u'尝试发送邮件'
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        print send_status
        if send_status:
            email_record.save()

    if send_type == 'update_email':
        email_title = u'衡师在线网邮箱修改验证码'
        email_body = u'你的邮箱验证码为:{0}'.format(email_record.code)
        print u'尝试发送邮件'
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        print send_status
        if send_status:
            email_record.save()



def generate_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str

