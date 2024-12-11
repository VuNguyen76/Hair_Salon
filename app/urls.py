from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart,name='cart'),
    path('checkout/', views.checkout,name='checkout'),
    path('update_item/', views.updateItem, name='update_item'),

    path('login/', views.login_view, name='login'),  # Đường dẫn đăng nhập
    path('logout/', views.logout_view, name='logout'),  # Đường dẫn đăng xuất
    path('register/', views.register_view, name='register'),  # Đường dẫn đăng ký
]
