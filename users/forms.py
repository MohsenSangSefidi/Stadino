from django import forms


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
