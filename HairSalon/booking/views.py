# from django.shortcuts import render, redirect
# from django.contrib import messages
# from .forms import BookingForm
# from .models import Booking, Guest_Booking

# def booking_view(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
        
#         if form.is_valid():
#             # Lấy dữ liệu từ form
#             name = form.cleaned_data.get('name')
#             phone = form.cleaned_data.get('phone')
#             gender = form.cleaned_data.get('gender')
#             branch = form.cleaned_data.get('branch')
#             service = form.cleaned_data.get('service')
#             message = form.cleaned_data.get('message')
#             booking_date = form.cleaned_data.get('booking_date')
#             booking_time = form.cleaned_data.get('booking_time')
            
#             if request.user.is_authenticated:  # Nếu người dùng đã đăng nhập
#                 # Lưu vào bảng Booking (dành cho người dùng đã đăng nhập)
#                 booking = Booking.objects.create(
#                     user=request.user,
#                     phone=phone,
#                     branch=branch,
#                     service=service,
#                     message=message,
#                     booking_date=booking_date,
#                     booking_time=booking_time,
#                 )
#                 messages.success(request, 'Đặt lịch thành công!')  # Thông báo thành công
#                 return redirect('booking')  # Redirect đến trang quản lý lịch hẹn của người dùng

#             else:  # Nếu người dùng chưa đăng nhập (khách)
#                 # Lưu vào bảng GuestBooking (dành cho khách)
#                 guest_booking = Guest_Booking.objects.create(
#                     guest_phone=phone,
#                     name=name,
#                     gender=gender,
#                     branch=branch,
#                     service=service,
#                     message=message,
#                     booking_date=booking_date,
#                     booking_time=booking_time,
#                 )
#                 messages.success(request, 'Đặt lịch thành công!')  # Thông báo thành công
#                 return redirect('booking')  # Redirect đến trang dành cho khách chưa đăng nhập

#     else:
#         form = BookingForm()

#     return render(request, 'booking.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm

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

