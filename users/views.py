from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from django.http import HttpResponse
from django.views import View

from .forms import RegistrationForm, LoginForm
from .models import User


class LoginView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        form = LoginForm()

        return render(
            request, 'login.html', {
                'form': form,
            }
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = LoginForm(request.POST)

        # Validate Form
        if not form.is_valid():
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        user = User.objects.filter(email=form.cleaned_data.get('email'), is_active=True).first()

        # Validate User Information
        if user is None:
            form.add_error('email', 'کاربری با این ایمیل وجور ندارد.')
            return render(request, 'login.html', {
                'form': form
            })

        if not user.check_password(form.cleaned_data.get('password')):
            form.add_error('password', 'رمز عبور یا ایمیل وارد شده نادرست است.')
            return render(request, 'login.html', {
                'form': form
            })

        # Login user
        login(request, user)

        return redirect(reverse('index'))


class RegisterView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        form = RegistrationForm()

        return render(
            request, 'register.html', {
                'form': form
            }
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = RegistrationForm(request.POST)

        # Validate Form
        if not form.is_valid():
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        # Validate Password
        if form.cleaned_data.get('password') != form.cleaned_data.get('re_password'):
            form.add_error('re_password', 'رمز عبور و تکرار آن متفاوت است.')
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        # Check Username
        user = User.objects.filter(username=form.cleaned_data.get('username')).first()

        if user is not None:
            form.add_error('username', 'این نام کاربری از قبل وجود دارد')
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        # Check Email
        user = User.objects.filter(email=form.cleaned_data.get('email')).first()

        if user is not None:
            form.add_error('email', 'این ایمیل از قبل وجود دارد')
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        # Create User
        user = User.objects.create(
            username=form.cleaned_data.get('username'),
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
            email=form.cleaned_data.get('email'),
            is_active=True
        )

        # User Set Password
        user.set_password(form.cleaned_data.get('password'))
        user.save()

        # Login user
        login(request, user)

        return redirect(reverse('index'))
