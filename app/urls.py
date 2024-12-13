from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('admin_salon/', views.admin_view, name='admin_salon' ,),
    path('staff_salon/', views.staff_view, name='staff_salon' ,),
    path('login/', views.login_view, name='login'),  # Đường dẫn đăng nhập
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
