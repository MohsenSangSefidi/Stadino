from django.utils.crypto import get_random_string
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import login, logout

from django.core.mail import send_mail
from django.conf import settings

from utils import utils
from .models import *
from .forms import *
import re


class LoginView(View):
    def get(self, request:HttpRequest):
        form = LoginForm()
        return render(request, 'login.html', {
            'form' : form
        })

    def post(self, request:HttpRequest):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = UserModels.objects.filter(email=email, is_active=True).first()
            if user:
                password = form.cleaned_data.get('password')
                if user.check_password(password):
                    user.token = get_random_string(40)
                    user.save()
                    login(request, user)
                    return redirect(reverse('home'))
                else:
                    form.add_error('password', 'رمز عبور اشتباه است.')
            else:
                form.add_error('email', 'حسابی با این ایمیل وجود ندارد.')

        return render(request, 'login.html', {
            'form' : form
        })

class RegisterView(View):
    def get(self, request:HttpRequest):

        form = RegisterForm()
        return render(request, 'singup.html', {
            'form' : form
        })

    def post(self, request:HttpRequest):
        register = RegisterForm(request.POST)
        if register.is_valid():
            email = register.cleaned_data.get('email')
            user = UserModels.objects.filter(email=email).first()

            if not user:
                password = register.cleaned_data.get('password')
                passwordCheck = register.cleaned_data.get('passwordCheck')
                if password == passwordCheck:
                    code = utils.activeCode()
                    newUser = UserModels(email=email, activeCode=code,token=get_random_string(40), is_active=False)
                    newUser.set_password(password)
                    # send_mail(
                    #     'Verify Code',
                    #     f'<h1>{code}</h1>',
                    #     'settings.EMAIL_HOST_USER',
                    #     [email],
                    #     fail_silently=False)
                    newUser.save()
                    return redirect(reverse('verify-account', args=[newUser.token]))
                else:
                     register.add_error('password', 'پسورد و تکرار ان مطابقت ندارد.')
            else:
                register.add_error('email', 'ایمیل از قبل موجود است.')

        return render(request, 'singup.html', {
            'form': register
        })

class VerifyAccountView(View):
    def get(self, request:HttpRequest, token):
        user = UserModels.objects.filter(token=token, is_active=False).first()
        if user:
            form = VerifyAcounntForm()
            return render(request, 'verify-account.html', {
                'form' : form
            })
        else:
            return redirect(reverse('home'))

    def post(self, request:HttpRequest, token):
        form = VerifyAcounntForm(request.POST)

        if form.is_valid():
            user = UserModels.objects.filter(token=token, is_active=False).first()
            code = form.cleaned_data.get('fullNumber')
            if code == user.activeCode:
                user.is_active = True
                user.save()
                return redirect(reverse('home'))
            else:
                form.add_error('num1', 'کد اشتباه است.')

        return render(request, 'verify-account.html', {
            'form': form
        })

class ResendEmailView(View):
    def get(self, request:HttpRequest, token):
        user = UserModels.objects.filter(token=token).first()
        user.activeCode = utils.activeCode()
        user.token = get_random_string(40)
        user.save()
        # send_mail(
        #     'Verify Code',
        #     f'<h1>{user.activeCode}</h1>',
        #     'settings.EMAIL_HOST_USER',
        #     [user.email],
        #     fail_silently=False)
        return redirect(reverse('verify-account', args=[user.token]))

class ForgetPasswordView(View):
    def get(self, request:HttpRequest):
        form = ForgetPasswordForm()
        return render(request, 'forget-password.html', {
            'form' : form
        })

    def post(self, request:HttpRequest):
        form = ForgetPasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = UserModels.objects.filter(email=email).first()
            if user:
                user.activeCode = utils.activeCode()
                user.is_active = False
                user.save()
                # send_mail(
                #     'Verify Code',
                #     f'<h1>{user.activeCode}</h1>',
                #     'settings.EMAIL_HOST_USER',
                #     [user.email],
                #     fail_silently=False)
                return redirect(reverse('verify-account-forget-password', args=[user.token]))
            else:
                form.add_error('email', 'کاربری با این ایمیل یافت نشد.')

        return render(request, 'forget-password.html', {
            'form': form
        })

class VerifyAccountForgetPasswordView(View):
    def get(self, request:HttpRequest, token):
        user = UserModels.objects.filter(token=token, is_active=False).first()
        if user:
            form = VerifyAcounntForm()
            return render(request, 'verify-account-forget-password.html', {
                'form' : form
            })
        else:
            return redirect(reverse('home'))

    def post(self, request:HttpRequest, token):
        form = VerifyAcounntForm(request.POST)

        if form.is_valid():
            user = UserModels.objects.filter(token=token, is_active=False).first()
            code = form.cleaned_data.get('fullNumber')
            if code == user.activeCode:
                user.is_active = True
                user.save()
                return redirect(reverse('change-password-forget-password', args=[user.token]))
            else:
                form.add_error('num1', 'کد اشتباه است.')

        return render(request, 'verify-account-forget-password.html', {
            'form': form
        })

class ForgetPasswordChangePasswordView(View):
    def get(self, request:HttpRequest, token):
        user = UserModels.objects.filter(is_active=True, token=token).first()
        form = ForgetPasswordChangePassForm()

        if user:
            return render(request, 'changepass-forget-password.html', {
                'user' : user,
                'form' : form
            })

        return redirect(reverse('home'))

    def post(self, request:HttpRequest, token):
        user = UserModels.objects.filter(is_active=True, token=token).first()
        form = ForgetPasswordChangePassForm(request.POST)

        if form.is_valid():
            newPass = form.cleaned_data.get('newPass')
            rePass = form.cleaned_data.get('rePass')
            if newPass == rePass:
                user.set_password(newPass)
                user.token = get_random_string(40)
                user.save()
                return redirect(reverse('login'))
            else:
                form.add_error('oldPass', 'رمز عبور و تکرار آن مطابقت ندارد.')

        return render(request, 'changepass-forget-password.html', {
            'user': user,
            'form': form
        })

class UserPanelView(View):
    def get(self, request:HttpRequest):
        return render(request, 'user-panel.html')

class UserPanelMenu(View):
    def get(self, request:HttpRequest):
        user = request.user
        return render(request, 'user-panel-menu.html', {
            'user' : user
        })

    def post(self, request:HttpRequest):
        user = request.user
        return render(request, 'user-panel-menu.html', {
            'user' : user
        })

class UserPanelMenuRes(View):
    def get(self, request:HttpRequest):
        user = request.user
        return render(request, 'user-panel-menu-res.html', {
            'user' : user
        })

    def post(self, request: HttpRequest):
        user = request.user
        return render(request, 'user-panel-menu-res.html', {
            'user': user
        })

class UserPanelChangePasswordView(View):
    def get(self, request:HttpRequest):
        user = request.user
        form = ChangePassForm()
        return render(request, 'user-panel-changpass.html', {
            'user' : user,
            'form' : form
        })

    def post(self, request:HttpRequest):
        user = request.user
        form = ChangePassForm(request.POST)

        if form.is_valid():
            oldPass = form.cleaned_data.get('oldPass')
            if user.check_password(oldPass):
                newPass = form.cleaned_data.get('newPass')
                rePass = form.cleaned_data.get('rePass')
                if newPass == rePass:
                    user.set_password(newPass)
                    user.save()
                    return redirect(reverse('login'))
                else:
                    form.add_error('oldPass', 'رمز عبور و تکرار آن مطابقت ندارد.')
            else:
                form.add_error('oldPass', 'رمز قبلی مطابقت ندارد.')

        return render(request, 'user-panel-changpass.html', {
            'user': user,
            'form': form
        })

class UserPanelChangeInfoView(View):
    def get(self, request:HttpRequest):
        form = ChangeInfoForm(instance=request.user)
        return render(request, 'user-panel-changeinfo.html', {
            'form' : form
        })

    def post(self, request:HttpRequest):
        form = ChangeInfoForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save(commit=True)
            return redirect('user-panel')

        return render(request, 'user-panel-changeinfo.html', {
            'user' : request.user,
            'form': form
        })

class Logout(View):
    def get(self, request:HttpRequest):
        logout(request)
        return redirect(reverse('home'))