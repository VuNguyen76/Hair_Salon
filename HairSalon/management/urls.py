from django.urls import path
from . import views

urlpatterns = [
   path('manage/', views.manage_dashboard, name='manage'),
   path('manage_service/', views.manage_service, name='manage_service'),
   path('manage_service/edit/<int:service_id>/', views.edit_service, name='edit_service'),
   path('manage_service/delete/<int:service_id>/', views.delete_service, name='delete_service'),
   path('manage_staff/', views.manage_staff, name='manage_staff'),
]
