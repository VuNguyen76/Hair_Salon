from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('', views.main, name='main'),
   path('about/', views.about, name='about'),
   path('register/', views.register, name='register'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('quan-ly-thong-tin-dat-hang/', views.quan_ly_dat_lich, name='quan_ly_dat_lich'),
   path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),  # Dashboard cho staff
    path('staff/manage/dashboard/', views.manage_dashboard, name='manage_dashboard'),  # Dashboard cho admin
   path('cancel_booking/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
]
