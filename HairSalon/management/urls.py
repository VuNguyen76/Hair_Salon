from django.urls import path
from . import views
urlpatterns = [
   path('manage/', views.manage_dashboard, name='manage'),
   path('manage_service/', views.manage_service, name='manage_service'),
]
