from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
   path('manage/', views.manage_dashboard, name='manage'),
]
