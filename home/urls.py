from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.loginuser, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logoutuser, name="logout"),
    path("company_register/", views.register_company, name="register_company"),
    path("user_detail/", views.user_detail, name="user_detail"),
    path("company_detail/", views.company_detail, name="company_detail"),
    path("company_delete/", views.delete_company, name="company_detail"),
    path("user_delete/", views.delete_user, name="company_detail"),
]
