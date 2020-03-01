# *_* coding:utf-8 *_*
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from django.db.models import Q
from django.views.generic.base import View
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# Create your views here.
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'msg': '未激活，请在邮箱中点击链接激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误，请重新登录'})
        else:
            return render(request, 'login.html', {"login_form":login_form})

class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm(request.POST)
        return render(request, 'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email','')
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'msg':u'用户已经被注册了','register_form':register_form})
            pass_word = request.POST.get('password','')
            user_profile = UserProfile()
            user_profile.username = user_name   #这是邮箱
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.is_active = False
            user_profile.save()
            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form':register_form})

class ActiveUserView(View):
    print u'进入到当前页面了'
    def get(self,request,active_code):
          all_records =  EmailVerifyRecord.objects.filter(code=active_code)
          if all_records:
              for record in all_records:
                  email = record.email
                  all_users = UserProfile.objects.filter(email=email)
                  for user in all_users:
                      user.is_active = True
                      user.save()
          else:
              return render(request, 'active_fail.html')
          return render(request, 'login.html')




class ResetUserView(View):
    print u'进入到密码重置页面了'
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html', {'email':email})
class ModifyPwdView(View):
    print u'进入该界面'
    def post(self,request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            email = request.POST.get('email','')
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2','')
            if password != password2:
                return render(request, 'password_reset.html', {'email':email, 'msg':'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'modifypwd_form':modifypwd_form})





class ForgetPwdView(View):
    def get(self,request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        return render(request, 'forgetpwd.html',{'forgetpwd_form':forgetpwd_form})

    def post(self,request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            if UserProfile.objects.filter(email=email):
                print u"准备发送邮件"
                send_register_email(email,'forget')
                return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html',{'forgetpwd_form':forgetpwd_form})




