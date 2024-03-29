from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-account/<token>/', VerifyAccountView.as_view(), name='verify-account'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget-password'),
    path('forget-password/<token>/', VerifyAccountForgetPasswordView.as_view(), name='verify-account-forget-password'),
    path('change-password/<token>/', ForgetPasswordChangePasswordView.as_view(), name='change-password-forget-password'),
    path('user-panel/', UserPanelView.as_view(), name='user-panel'),
    path('resend-code/<token>', ResendEmailView.as_view(), name='resend-code'),
    path('change-password/', UserPanelChangePasswordView.as_view(), name='change-pass'),
    path('change-info/', UserPanelChangeInfoView.as_view(), name='change-info')
]
