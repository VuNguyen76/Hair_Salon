from django.shortcuts import render, redirect
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
                return redirect('/')  # Chuyển hướng đến trang chủ
            else:
                messages.error(request, "Vui lòng kiểm tra lại tên đăng nhập hoặc mật khẩu.")
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

