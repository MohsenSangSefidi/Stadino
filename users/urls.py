from django.urls import path
from .views import (
    LoginView, RegisterView, ForgetPasswordView, ChangePasswordView, UserPanelView, ChangeUserInfoView,
    change_password_panel, UserOrderView, AddressView, CreateAddressView, delete_address, UserCommentView,
    FavoriteProductView, logout_view
)

urlpatterns = [
    # Login And Sing Up Urls
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('change-password/<str:token>', ChangePasswordView.as_view(), name='change_password'),
    path('logout/', logout_view, name='logout'),
    # User Panel Urls
    path('user-panel/', UserPanelView.as_view(), name='user_panel'),
    path('change-info/<error>', ChangeUserInfoView.as_view(), name='change_info'),
    path('change-pass/', change_password_panel, name='change_pass'),
    path('orders/', UserOrderView.as_view(), name='user_orders'),
    path('address/', AddressView.as_view(), name='address'),
    path('create-address/<object_id>', CreateAddressView.as_view(), name='create_address'),
    path('delete-address/<object_id>', delete_address, name='delete_address'),
    path('comment/', UserCommentView.as_view(), name='user_comment'),
    path('favorite/', FavoriteProductView.as_view(), name='favorite'),
]
