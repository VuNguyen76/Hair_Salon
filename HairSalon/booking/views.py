
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm, LookupForm
from .models import Booking 
import ast

def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking_instance = form.save(commit=False)
            if request.user.is_authenticated:
                booking_instance.user = request.user  # Gán user nếu đã đăng nhập
            else:
                booking_instance.user = None  # Để user là None nếu chưa đăng nhập
            booking_instance.save()
            messages.success(request, 'Đặt lịch thành công!')
            return redirect('booking')  # Redirect để làm mới form
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {'form': form})

def convert_to_list(string):
    try:
        return ast.literal_eval(string)
    except (ValueError, SyntaxError):
        return [string]

def lookup_view(request):
    form_lookup = LookupForm()
    bookings = None
    lookup=False
    if request.method == "POST":
        form_lookup = LookupForm(request.POST)
        if form_lookup.is_valid():
            phone_number = form_lookup.cleaned_data["phone_number"]
            bookings = Booking.objects.filter(phone_number=phone_number)
            for booking in bookings:
                booking.service = convert_to_list(booking.service)
            lookup=True
    return render(request, "lookup.html", {"form": form_lookup, "bookings": bookings, "lookup": lookup})

