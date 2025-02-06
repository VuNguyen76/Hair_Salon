from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm,LoginForm
from .models import Infor
from booking.models import Booking
from booking.forms import LookupForm
import ast

def main(request):
    return render(request, 'main.html')

def about(request):
    return render(request, 'about.html')

def manage(request):
    return render(request, 'manage.html')
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Lưu số điện thoại vào UserProfile
            phone = form.cleaned_data['phone']
            Infor.objects.create(user=user, phone=phone)

            return redirect('/login')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Kiểm tra quyền của người dùng và chuyển hướng đến trang phù hợp
                if user.is_staff:
                    if user.is_superuser:
                        # Nếu là admin, chuyển hướng đến trang quản lý
                        return redirect('manage')
                    else:
                        # Nếu là staff, chuyển hướng đến trang staff dashboard
                        return redirect('staff')
                else:
                    # Nếu là user (không phải staff hoặc admin), chuyển hướng đến trang chủ
                    return redirect('/')
            else:
                messages.error(request, "Vui lòng kiểm tra lại tên đăng nhập hoặc mật khẩu.")
        else:
            messages.error(request, "Thông tin đăng nhập không hợp lệ.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
def logout_view(request):
    logout(request)
    return redirect('/')
def staff(request):
    return render(request, 'staff.html')


def quan_ly_dat_lich(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'quan-ly-dat-lich.html', {'bookings': bookings})
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')
def manage_dashboard(request):
    return render(request, 'manage_dashboard.html')

def cancel_booking_view(request, booking_id):
    # Lấy booking theo ID
    booking = get_object_or_404(Booking, id=booking_id)

    # Kiểm tra nếu người dùng có quyền hủy booking
    if request.user.is_authenticated and (booking.user == request.user or request.user.is_staff):
        booking.status = 'canceled'  # Cập nhật trạng thái thành 'canceled'
        booking.save()

        messages.success(request, f"Lịch hẹn của {booking.full_name} đã được hủy thành công.")
    else:
        messages.error(request, "Bạn không có quyền hủy lịch hẹn này.")

    # Sau khi hủy, chuyển hướng về trang chi tiết lịch hẹn
    return redirect('quan_ly_dat_lich')


