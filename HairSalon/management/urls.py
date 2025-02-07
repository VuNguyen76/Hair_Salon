from django.urls import path
from . import views

urlpatterns = [
   path('manage/', views.manage_dashboard, name='manage'),
   path('manage_service/', views.manage_service, name='manage_service'),
   path('manage_service/edit/<int:service_id>/', views.edit_service, name='edit_service'),
   path('manage_service/delete/<int:service_id>/', views.delete_service, name='delete_service'),
   path('manage_employee/', views.manage_employee, name='manage_employee'),
   path('employee/edit/<int:pk>/', views.edit_employee, name='edit_employee'),
   path('employee/delete/<int:pk>/', views.delete_employee, name='delete_employee'),
   path('manage_report/', views.manage_report, name='manage_report'),
]
