from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm

def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.error(request, 'Đặt lịch thành công!')  # Thông báo thành công
            return redirect('booking')  # Redirect để làm mới form
    else:
        form = BookingForm()
    
    return render(request, 'booking.html', {'form': form})
