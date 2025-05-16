from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views import View

from .forms import (
    RegistrationForm, LoginForm, ForgetPasswordForm, ChangePasswordForm, ChangeUserInfoForm, ChangePasswordPanelForm,
    AddressCreateForm
)
from products.models import ProductComments, FavoriteProducts
from .models import User, Address


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


@method_decorator(login_required, name='dispatch')
class UserPanelView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, 'user_panel.html', {})


@method_decorator(login_required, name='dispatch')
class ChangeUserInfoView(View):
    def get(self, request, error=None, *args, **kwargs) -> HttpResponse:
        change_info_form = ChangeUserInfoForm(instance=request.user)
        change_pass_form = ChangePasswordPanelForm(instance=request.user)

        return render(request, 'chang_info.html', {
            'change_info_form': change_info_form,
            'change_pass_form': change_pass_form,
            'error': error
        })

    def post(self, request, error=None, *args, **kwargs) -> HttpResponse:
        change_info_form = ChangeUserInfoForm(request.POST, instance=request.user)
        change_pass_form = ChangePasswordPanelForm(request.POST, instance=request.user)

        if not change_info_form.is_valid():
            return render(request, 'chang_info.html', {
                'change_info_form': change_info_form,
                'change_pass_form': change_pass_form,
                'error': error
            })

        change_info_form.save()

        return render(request, 'chang_info.html', {
            'change_info_form': change_info_form,
            'change_pass_form': change_pass_form,
            'error': error
        })


@method_decorator(login_required, name='dispatch')
class UserOrderView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, 'last_order.html', {})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:

        address = Address.objects.filter(user=request.user)

        return render(
            request, 'address.html', {
                'address': address
            }
        )


@method_decorator(login_required, name='dispatch')
class CreateAddressView(View):
    def get(self, request, object_id=None, *args, **kwargs) -> HttpResponse:

        form = AddressCreateForm()

        return render(
            request, 'address_create.html', {
                'form': form
            }
        )

    def post(self, request, object_id=None, *args, **kwargs) -> HttpResponse:

        form = AddressCreateForm(request.POST)

        if not form.is_valid():
            return render(
                request, 'address_create.html', {
                    'form': form
                }
            )

        data = form.save(commit=False)

        data.user = request.user
        data.street = form.cleaned_data.get('street')
        data.city = form.cleaned_data.get('city_select')
        data.state = form.cleaned_data.get('state_select')
        data.phone_number = form.cleaned_data.get('phone_number')

        data.save()

        return redirect(reverse('address'))


@method_decorator(login_required, name='dispatch')
class UserCommentView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        comments = ProductComments.objects.filter(user=request.user).only('comment', 'product')

        return render(
            request, 'comment.html', {
                'comments': comments
            }
        )


@method_decorator(login_required, name='dispatch')
class FavoriteProductView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        favorites = FavoriteProducts.objects.filter(user=request.user)

        return render(
            request, 'favorites.html', {
                'favorites': favorites
            }
        )


@login_required()
def delete_address(request, object_id, *args, **kwargs) -> HttpResponse:
    address = Address.objects.filter(id=object_id).first()

    address.delete()

    return redirect(reverse('address'))


@login_required()
def change_password_panel(request, *args, **kwargs) -> HttpResponse:
    if request.method == 'POST':
        change_pass_form = ChangePasswordPanelForm(request.POST, instance=request.user)

        if not change_pass_form.is_valid():
            return redirect(reverse('change_info'))

        old_password = change_pass_form.cleaned_data.get('old_password')
        password = change_pass_form.cleaned_data.get('password')
        re_password = change_pass_form.cleaned_data.get('re_password')

        user = User.objects.get(email=request.user.email).only('password')

        if not user.check_password(old_password):
            return redirect(reverse('change_info', kwargs={'error': 'رمز عبور قدیمی درست وارد نشده است.'}))

        if password != re_password:
            return redirect(reverse('change_info', kwargs={'error': 'رمز عبور و تکرار آن مطابقت ندارد.'}))

        user.set_password(password)
        user.save()
        login(request, user)

        return redirect(reverse('change_info', kwargs={'error': 'رمز عبور تغییر یافت.'}))


@login_required()
def logout_view(request):

    logout(request)

    return redirect(reverse('login'))
