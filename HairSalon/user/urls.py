from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('', views.main, name='main'),
   path('about/', views.about, name='about'),
   path('register/', views.register, name='register'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('manage/', views.manage, name='manage'),
   path('staff/', views.staff, name='staff'),
   path('quan-ly-thong-tin-dat-hang/', views.quan_ly_dat_lich, name='quan_ly_dat_lich'),
]
