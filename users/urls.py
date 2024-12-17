from django.urls import path
from .views import LoginView, RegisterView, ForgetPasswordView, ChangePasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('change-password/<str:token>', ChangePasswordView.as_view(), name='change_password'),
]
