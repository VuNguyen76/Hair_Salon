from django.urls import path
from .views import booking_view,lookup_view

urlpatterns = [
    path('booking/', booking_view, name='booking'),
    path('lookup/', lookup_view, name='lookup'),
]
