from django.shortcuts import render
from booking.models import Booking

def manage_dashboard(request):
    completed_bookings = Booking.objects.filter(status='completed')
    total_revenue = sum(booking.revenue for booking in completed_bookings)
    
    return render(request, 'manage_dashboard.html', {'completed_bookings': completed_bookings, 'total_revenue': total_revenue})
def manage_service(request):
    egcye
def manage_service(request):
    egcye