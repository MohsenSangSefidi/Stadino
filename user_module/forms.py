from django import forms
from .models import *


class RegisterForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(
        attrs={'id': 'floatingInputEmail', 'class': 'form-control', 'type': 'email'}))
    password = forms.CharField(label='',widget=forms.TextInput(
        attrs={'id': 'floatingInputEmail', 'class': 'form-control', 'type': 'text'}))
    passwordCheck = forms.CharField(label='',widget=forms.TextInput(
        attrs={'id': 'floatingInputEmail', 'class': 'form-control', 'type': 'text'}))

class VerifyAcounntForm(forms.Form):
    num1 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "_", 'type': "number", 'step': "1", 'min': "0", 'max': "9", 'autocomplete': "no",
               "pattern": "\d*"}))
    num2 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "_", 'type': "number", 'step': "1", 'min': "0", 'max': "9", 'autocomplete': "no",
               "pattern": "\d*"}))
    num3 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "_", 'type': "number", 'step': "1", 'min': "0", 'max': "9", 'autocomplete': "no",
               "pattern": "\d*"}))
    num4 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "_", 'type': "number", 'step': "1", 'min': "0", 'max': "9", 'autocomplete': "no",
               "pattern": "\d*"}))
    num5 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "_", 'type': "number", 'step': "1", 'min': "0", 'max': "9", 'autocomplete': "no",
               "pattern": "\d*"}))
    num6 = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': "_", 'type': "number", 'step': "1", 'min': "0", 'max': "9", 'autocomplete': "no",
               "pattern": "\d*"}))
    fullNumber = forms.CharField(label='', widget=forms.TextInput(
        attrs={'id': "otp-value", 'placeholder': "_", 'type': "hidden", 'name': "otp"}))

class LoginForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(
        attrs={'type': "email", 'class': "form-control", 'id': "floatingInputEmail"}))
    password = forms.CharField(label='', widget=forms.TextInput(
        attrs={'type': "password", 'class': "form-control", 'id': "floatingInputPasswd"}))

class ForgetPasswordForm(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(
        attrs={'type': "email", 'class': "form-control", 'id': "floatingInputEmail"}))

class ForgetPasswordChangePassForm(forms.Form):
    newPass = forms.CharField(label='', widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control", 'id': "floatingInputoldPasswd",
               'placeholder': "رمز عبور قبلی خود را وارد کنید ..."}))
    rePass = forms.CharField(label='', widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control", 'id': "floatingInputConfirmPasswd",
               'placeholder': "رمز عبور قبلی خود را وارد کنید ..."}))

class ChangePassForm(forms.Form):
    oldPass = forms.CharField(label='', widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control", 'id': "floatingInputoldPasswd",
               'placeholder': "رمز عبور قبلی خود را وارد کنید ..."}))
    newPass = forms.CharField(label='', widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control", 'id': "floatingInputoldPasswd",
               'placeholder': "رمز عبور قبلی خود را وارد کنید ..."}))
    rePass = forms.CharField(label='', widget=forms.TextInput(
        attrs={'type': "text", 'class': "form-control", 'id': "floatingInputConfirmPasswd",
               'placeholder': "رمز عبور قبلی خود را وارد کنید ..."}))

class ChangeInfoForm(forms.ModelForm):
    class Meta:
        model = UserModels
        fields = ['username', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'type':"text",
                'class':"form-control",
                'id':"floatingInputEmail",
                'placeholder':"نام کاربری"
            }),
            'first_name': forms.TextInput(attrs={
                'type':"text",
                'class':"form-control",
                'id':"floatingInputEmail",
                'placeholder':"نام"
            }),
            'last_name': forms.TextInput(attrs={
                'type':"text",
                'class':"form-control",
                'id':"floatingInputEmail",
                'placeholder':"نام خانوادگی"
            }),}
        error_messages = {
            'username': {
                'unique': 'این نام کاربری از قبل موجود است.'
            },}
