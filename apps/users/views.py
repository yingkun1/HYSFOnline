# *_* coding:utf-8 *_*
from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm,UploadImageForm,UserInfoForm
from django.db.models import Q
from django.views.generic.base import View
from django.core.urlresolvers import reverse
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from users.models import Banner
from courses.models import Course
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
import json


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
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, 'login.html', {'msg': '未激活，请在邮箱中点击链接激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或者密码错误，请重新登录'})
        else:
            return render(request, 'login.html', {"login_form":login_form})


class LogoutView(View):
    """
    用户登出
    """
    def get(self,request):
        logout(request)

        return HttpResponseRedirect(reverse("index"))


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
            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = u'欢迎注册衡师在线网'
            user_message.save()
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
    """
    重置用户密码(用户未登录)
    """
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
                data = {'email':'未知错误'}
                return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            return render(request, 'forgetpwd.html',{'forgetpwd_form':forgetpwd_form})


class UserInfoView(LoginRequiredMixin,View):
    """
    用户个人信息
    """
    def get(self,request):
        current_nav = 'info'
        return render(request,'usercenter-info.html',{
            'current_nav':current_nav
        })

    def post(self,request):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            data = {'status':'success'}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            return HttpResponse(json.dumps(userinfo_form.errors),content_type="application/json")


class UploadImageView(LoginRequiredMixin,View):
    """
    用户上传头像
    """
    def post(self,request):
        uploadimage_form = UploadImageForm(request.POST,request.FILES)
        if uploadimage_form.is_valid():
            image = uploadimage_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            data = {'status':'success'}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data = {'status':'fail'}
            return HttpResponse(json.dumps(data),content_type="application/json")


class UpdatePwdView(LoginRequiredMixin,View):
    """
    重置用户密码(用户已登录)
    """
    def post(self,request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2','')
            if password != password2:
                data = {'status':'fail','msg':'密码不一致'}
                return HttpResponse(json.dumps(data),content_type="application/json")
            user = request.user
            user.password = make_password(password)
            user.save()
            data = {'status':'success'}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            return HttpResponse(json.dumps(modifypwd_form.errors),content_type="application/json")


class SendEmialCodeView(LoginRequiredMixin,View):
    """
    发送邮箱验证码
    """
    def get(self,request):
        email = request.GET.get('email','')
        if UserProfile.objects.filter(email=email):
            data = {'email':'邮箱已经存在'}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            send_register_email(email, 'update_email')
            data = {'status':'success'}
            return HttpResponse(json.dumps(data),content_type="application/json")


class UpdateEmailView(LoginRequiredMixin,View):
    """
    修改个人邮箱
    """
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')
        existed_records =  EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            data = {'status':'success'}
            return HttpResponse(json.dumps(data),content_type="application/json")
        else:
            data = {'email':'验证码出错'}
            return HttpResponse(json.dumps(data),content_type="application/json")


class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        current_nav = 'course'
        user_courses =  UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'all_courses':user_courses,
            'current_nav':current_nav
        })


class MyFavOrgView(LoginRequiredMixin,View):
    def get(self,request):
        current_nav = 'org'
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id = org_id)
            org_list.append(org)
        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list,
            'current_nav':current_nav
        })


class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self,request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id = teacher_id)
            teacher_list.append(teacher)
        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list
        })


class MyFavCourseView(LoginRequiredMixin,View):
    def get(self,request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id = course_id)
            course_list.append(course)
        return render(request,'usercenter-fav-course.html',{
            'course_list':course_list
        })


class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        current_nav = 'message'
        all_messages = UserMessage.objects.filter(user=request.user.id)
        # 用户清空未读消息
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()
        # 对我的消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 5, request=request)

        messages = p.page(page)
        return render(request,'usercenter-message.html',{
            'messages':messages,
            'current_nav':current_nav
        })


class IndexView(View):
    """
    衡师在线网首页
    """
    def get(self,request):
        # 取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html',{
            'all_banners':all_banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })


def page_not_found(request):
    # 全局404
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
