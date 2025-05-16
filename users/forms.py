from django import forms

from .models import User, Address


class RegistrationForm(forms.Form):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'floatingInputEmail'
            }
        )
    )

    first_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'floatingInputEmail'
            }
        )
    )

    last_name = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'floatingInputEmail'
            }
        )
    )

    email = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'id': 'floatingInputEmail'
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'id': 'floatingInputPasswd'
            }
        )
    )

    re_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'id': 'floatingInputPasswd'
            }
        )
    )


class LoginForm(forms.Form):
    email = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'id': 'floatingInputEmail'
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'id': 'floatingInputPasswd'
            }
        )
    )


class ForgetPasswordForm(forms.Form):
    email = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'type': 'email',
                'class': 'form-control',
                'id': 'floatingInputEmail'
            }
        ),

    )


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'id': 'floatingInputPasswd'
            }
        )
    )

    re_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'id': 'floatingInputPasswd'
            }
        )
    )


class ChangeUserInfoForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'id': 'floatingInputEmail',
                    'value': f'{model.username}'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'id': 'floatingInputEmail',
                    'value': f'{model.first_name}'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'id': 'floatingInputEmail',
                    'value': f'{model.last_name}'
                }
            )
        }
        error_messages = {
            'username': {
                'unique': 'این نام کاربری از قبل وجود دارد.',
                'validation': 'لطفا از فاصله در نام کاربری استفاده نکنید.'
            }
        }


class ChangePasswordPanelForm(forms.ModelForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'floatingInputoldPasswd',
                'placeholder': 'رمز عبور قبلی خود را وارد کنید ...'
            }
        )
    )

    re_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'type': 'text',
                'class': 'form-control',
                'id': 'floatingInputoldPasswd',
                'placeholder': 'رمز عبور جدید خود را وارد کنید ...'
            }
        )
    )

    class Meta:
        model = User
        fields = ('old_password', 'password', 're_password')
        widgets = {
            'password': forms.PasswordInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'id': 'floatingInputoldPasswd',
                    'placeholder': 'رمز عبور جدید خود را دوباره بنویسید ...'
                }
            )
        }


class AddressCreateForm(forms.ModelForm):
    city_choices = [
        ('کرج', 'کرج'),
        ('خرم آباد', 'خرم آباد'),
        ('نور آباد', 'نور آباد'),
        ('الشتر', 'الشتر'),
    ]

    state_choices = [
        ('تهران', 'تهران'),
        ('اصفهان', 'اصفهان'),
        ('مشهد', 'مشهد'),
        ('شیراز', 'شیراز'),
    ]

    city_select = forms.ChoiceField(
        choices=city_choices,
        widget=forms.Select(attrs={'id': 'floatingInputOstan1', 'class': 'form-select'}),
    )

    state_select = forms.ChoiceField(
        choices=state_choices,
        widget=forms.Select(attrs={'id': 'floatingInputCity1', 'class': 'form-select'}),
    )

    class Meta:
        model = Address
        fields = ('street', 'city_select', 'state_select', 'phone_number')
        widgets = {
            'street': forms.TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'id': 'floatingInputStreet1',
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control py-3',
                    'id': 'floatingInputDesc',
                    'placeholder': '09123457899'
                }
            )
        }