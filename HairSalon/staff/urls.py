from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('staff/', views.staff, name='staff'),  # Trang danh sách lịch hẹn
    path('booking/<int:booking_id>/', views.staff_booking_single, name='staff_booking_single'),  # Trang chi tiết đơn đặt lịch
    path('staff_booking/', views.staff_booking_multiple, name='staff_booking_multiple'),  # Trang xử lý nhiều đơn đặt lịch
    path('staff_account/', views.staff_account, name='staff_account'), 
    path('staff_booking_details/<int:user_id>/', views.staff_booking_details, name='staff_booking_details'),
    path('staff_report/', views.staff_report, name='staff_report'), 
]
