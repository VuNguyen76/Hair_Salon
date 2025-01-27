from django.urls import path
from .views import booking_view

urlpatterns = [
    path('booking/', booking_view, name='booking'),
]
