from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib.auth import login
from django.http import HttpResponse
from django.conf import settings
from django.views import View

from .forms import RegistrationForm, LoginForm, ForgetPasswordForm, ChangePasswordForm
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

        user = User.objects.filter(email=form.cleaned_data.get('email').lower(), is_active=True).first()

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
        user = User.objects.filter(email=form.cleaned_data.get('email').lower()).first()

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
            email=form.cleaned_data.get('email').lower(),
            token=get_random_string(100),
            is_active=True
        )

        # User Set Password
        user.set_password(form.cleaned_data.get('password'))
        user.save()

        # Login user
        login(request, user)

        return redirect(reverse('index'))


class ForgetPasswordView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        form = ForgetPasswordForm()

        return render(
            request, 'forget.html', {
                'form': form,
                'sent': False
            }
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = ForgetPasswordForm(request.POST)

        # Validate Form
        if not form.is_valid():
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        user = User.objects.filter(email=form.cleaned_data.get('email').lower()).first()

        # Validate User email
        if user is None:
            form.add_error('email', 'کاربری با این ایمیل وجود ندارد')
            return render(
                request, 'forget.html', {
                    'form': form,
                    'sent': False
                }
            )

        link = f'http://localhost:8000/users/change-password/{user.token}'
        html = render_to_string('email.html', {'link': link})

        try:
            send_mail(
                subject='تغغیر رمز عبور',
                message=' ',
                html_message=html,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except BadHeaderError as e:
            form.add_error('email', 'در ارسال ایمیل مشکلی به وجود آمده لطفا دوباره امتحان کنید.')
            return render(
                request, 'forget.html', {
                    'form': form,
                    'sent': False
                }
            )

        return render(
            request, 'forget.html', {
                'form': form,
                'sent': True
            }
        )


class ChangePasswordView(View):
    def get(self, request, token, *args, **kwargs) -> HttpResponse:
        user = User.objects.filter(token=token).first()

        if user is None:
            return redirect(reverse('index'))

        form = ChangePasswordForm()

        return render(
            request, 'change_pass.html', {
                'form': form
            }
        )

    def post(self, request, token, *args, **kwargs) -> HttpResponse:
        user = User.objects.filter(token=token).first()

        if user is None:
            return redirect(reverse('index'))

        form = ChangePasswordForm(request.POST)

        # Validate Form
        if not form.is_valid():
            return render(
                request, 'change_pass.html', {
                    'form': form
                }
            )

        if not form.cleaned_data.get('password') == form.cleaned_data.get('re_password'):
            form.add_error('password', 'رمز عبور و تکرار آن مطابقت ندارد.')
            return render(
                request, 'change_pass.html', {
                    'form': form
                }
            )

        user.set_password(form.cleaned_data.get('password'))
        user.token = get_random_string(100)
        user.save()

        login(request, user)

        return redirect(reverse('index'))
