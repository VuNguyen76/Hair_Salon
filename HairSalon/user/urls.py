from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('', views.main, name='main'),
   path('about/', views.about, name='about'),
   path('service/', views.service, name='service'),
   path('register/', views.register, name='register'),
   path('login/', views.login_view, name='login'),
   path('logout/', views.logout_view, name='logout'),
   path('quan-ly-thong-tin-dat-hang/', views.quan_ly_dat_lich, name='quan_ly_dat_lich'),
   path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
   path('staff/manage/dashboard/', views.manage_dashboard, name='manage_dashboard'),  
   path('cancel_booking/<int:booking_id>/', views.cancel_booking_view, name='cancel_booking'),
   path('review_infor/', views.review_infor, name='review_infor'),
   path('update_infor/', views.update_infor, name='update_infor'),
]
