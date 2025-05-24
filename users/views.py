from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail, BadHeaderError
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from django.http import HttpResponse
from urllib.parse import urlencode
from django.conf import settings
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

        # Validate form
        if not form.is_valid():
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        # Trying to get user object ( If didn't exist, sets user to none )
        try:
            user = User.objects.get(email=form.cleaned_data.get('email').lower(), is_active=True)
        except User.DoesNotExist:
            user = None

        # Validate user information
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

        # Validate form
        if not form.is_valid():
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        # Validate password
        if form.cleaned_data.get('password') != form.cleaned_data.get('re_password'):
            form.add_error('re_password', 'رمز عبور و تکرار آن متفاوت است.')
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        # Trying to get user object ( If didn't exist, sets user to none )
        try:
            user = User.objects.get(username=form.cleaned_data.get('username'))
        except User.DoesNotExist:
            user = None

        if user is not None:
            form.add_error('username', 'این نام کاربری از قبل وجود دارد')
            return render(
                request, 'register.html', {
                    'form': form
                }
            )

        # Check Email
        try:
            user = User.objects.get(email=form.cleaned_data.get('email').lower())
        except User.DoesNotExist:
            user = None

        # Validate user information
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

        # Trying to get user object ( If didn't exist, sets user to none )
        try:
            user = User.objects.get(email=form.cleaned_data.get('email').lower())

        except User.DoesNotExist:
            user = None

        # Validate User email
        if user is None:
            form.add_error('email', 'کاربری با این ایمیل وجود ندارد')
            return render(
                request, 'forget.html', {
                    'form': form,
                    'sent': False
                }
            )

        # Set information to send it via email
        link = reverse('change_password', kwargs={'token': user.token})
        html = render_to_string('email.html', {'link': link})

        # Trying to send email
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
        try:
            user = User.objects.filter(token=token).first()
        except User.DoesNotExist:
            return redirect('index')

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

        # Save user data
        user.set_password(form.cleaned_data.get('password'))
        user.token = get_random_string(100)
        user.save()

        # Login user
        login(request, user)

        return redirect(reverse('index'))


@method_decorator(login_required, name='dispatch')
class UserPanelView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        user_carts = request.user.carts.filter(is_paid=True).only('cart_status', 'pay_date', 'id')[:5]

        return render(
            request, 'user_panel.html', {
                'user_carts': user_carts,
            }
        )


@method_decorator(login_required, name='dispatch')
class ChangeUserInfoView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        change_info_form = ChangeUserInfoForm(instance=request.user)
        change_pass_form = ChangePasswordPanelForm(instance=request.user)

        # Get variables from Query-Params ( Showing message on template )
        error = request.GET.get('error')
        success = request.GET.get('success')

        return render(request, 'chang_info.html', {
            'change_info_form': change_info_form,
            'change_pass_form': change_pass_form,
            'error': error,
            'success': success
        })

    def post(self, request, *args, **kwargs) -> HttpResponse:
        change_info_form = ChangeUserInfoForm(request.POST, instance=request.user)
        change_pass_form = ChangePasswordPanelForm(request.POST, instance=request.user)

        # Get variables from Query-Params ( Showing message on template )
        error = request.GET.get('error')
        success = request.GET.get('success')

        # Validate form ( change_info_form )
        if not change_info_form.is_valid():
            return render(request, 'chang_info.html', {
                'change_info_form': change_info_form,
                'change_pass_form': change_pass_form,
                'error': error,
                'success': success
            })

        # Save data
        change_info_form.save()

        return render(request, 'chang_info.html', {
            'change_info_form': change_info_form,
            'change_pass_form': change_pass_form,
            'error': error,
            'success': success
        })


@method_decorator(login_required, name='dispatch')
class UserOrderView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        # Get user cart ( shopping history )
        user_carts = request.user.carts.filter(is_paid=True).only('cart_status', 'pay_date', 'id')

        # Paginate item
        paginator = Paginator(user_carts, 5)

        # Get variables from Query-Params ( showing which page of paginated item must be sent )
        page_number = request.GET.get('page')

        # Set paginate items
        page_obj = paginator.page(page_number if page_number else 1)

        return render(
            request, 'last_order.html', {
                'page_obj': page_obj,
            }
        )


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        address = Address.objects.filter(user=request.user, is_active=True)

        return render(
            request, 'address.html', {
                'address': address
            }
        )


@method_decorator(login_required, name='dispatch')
class CreateAddressView(View):
    def get(self, request, *args, **kwargs) -> HttpResponse:
        form = AddressCreateForm()

        return render(
            request, 'address_create.html', {
                'form': form
            }
        )

    def post(self, request, *args, **kwargs) -> HttpResponse:
        form = AddressCreateForm(request.POST)

        # Validate form
        if not form.is_valid():
            return render(
                request, 'address_create.html', {
                    'form': form
                }
            )

        # Create instance of information user sent
        data = form.save(commit=False)

        # Set information
        data.user = request.user
        data.street = form.cleaned_data.get('street')
        data.city = form.cleaned_data.get('city_select')
        data.state = form.cleaned_data.get('state_select')
        data.phone_number = form.cleaned_data.get('phone_number')

        # Save data
        data.save()

        # Return previous-page
        previous_page = request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(previous_page)


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
        # Get user favorite products
        favorites = FavoriteProducts.objects.filter(user=request.user)

        # Paginate item
        paginator = Paginator(favorites, 10)

        # Get variables from Query-Params ( showing which page of paginated item must be sent )
        page = request.GET.get('page')

        # Set paginate items
        paginated_products = paginator.page(page if page else 1)

        return render(
            request, 'favorites.html', {
                'paginated_products': paginated_products
            }
        )


@login_required()
def delete_address(request, object_id, *args, **kwargs) -> HttpResponse:
    # Try to get user address
    try:
        address = Address.objects.get(id=object_id)
    except Address.DoesNotExist:
        previous_page = request.META.get('HTTP_REFERER', reverse('index'))
        return redirect(previous_page)

    # Delete ( set is_active to False )
    address.is_active = False
    address.save()

    # Return previous-page
    previous_page = request.META.get('HTTP_REFERER', reverse('index'))
    return redirect(previous_page)


@login_required()
def change_password_panel(request, *args, **kwargs) -> HttpResponse:
    if request.method == 'POST':
        change_pass_form = ChangePasswordPanelForm(request.POST, instance=request.user)

        # Validate form
        if not change_pass_form.is_valid():
            return redirect(reverse('change_info'))

        # Set data from form
        old_password = change_pass_form.cleaned_data.get('old_password')
        password = change_pass_form.cleaned_data.get('password')
        re_password = change_pass_form.cleaned_data.get('re_password')

        # Try to get user object ( if didn't exist, returns previous-page )
        try:
            user = User.objects.get(email=request.user.email)

        except User.DoesNotExist:
            # Return previous-page
            previous_page = request.META.get('HTTP_REFERER', reverse('index'))
            return redirect(previous_page)

        # Set Url
        url = reverse('change_info')
        params = {}

        # Validate information ( user password )
        if not user.check_password(old_password):
            params['error'] = 'رمز عبور قدیمی درست وارد نشده است'

            return redirect(f'{url}?{urlencode(params)}')

        # Validate information ( check re-password )
        if password != re_password:
            params['error'] = 'رمز عبور و تکرار آن مطابقت ندارد'
            return redirect(f'{url}?{urlencode(params)}')

        # Save data and login user
        user.set_password(password)
        user.save()
        login(request, user)

        # Return page
        params['success'] = 'رمز عبور تغییر یافت'
        return redirect(f'{url}?{urlencode(params)}')

# Log out functions
@login_required()
def logout_view(request):
    logout(request)

    return redirect(reverse('login'))
