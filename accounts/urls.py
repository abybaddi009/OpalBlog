from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views
from . import views_api

app_name = "accounts"

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path("register/", views.UserRegisterView.as_view(), name="register"),

    path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
    path('api/register/', views_api.UserRegisterApi.as_view(), name='api-register'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('api/users/', views_api.UserListAPIView.as_view(), name='api-users-list'),
]