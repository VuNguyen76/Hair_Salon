from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Booking,Service
from .forms import ServiceForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def manage_dashboard(request):
    completed_bookings = Booking.objects.filter(status='completed').order_by('-id')  # Sắp xếp theo ID mới nhất
    total_revenue = sum(booking.revenue for booking in completed_bookings)
    
    return render(request, 'manage_dashboard.html', {'completed_bookings': completed_bookings, 'total_revenue': total_revenue})
def manage_staff(request): 
    return render(request, 'manage_staff.html')

def manage_service(request):
    services = Service.objects.all().order_by('-id')  # Lấy danh sách dịch vụ và sắp xếp theo ID mới nhất
    
    paginator = Paginator(services, 5)  # Mỗi trang có 5 dịch vụ
    page_number = request.GET.get('page')  # Lấy số trang từ URL
    page_obj = paginator.get_page(page_number)  # Lấy danh sách dịch vụ cho trang hiện tại

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)  # Lấy cả dữ liệu hình ảnh
        if form.is_valid():
            form.save()  # Lưu dịch vụ mới vào DB
            return redirect('manage_service')  # Reload trang sau khi thêm
    else:
        form = ServiceForm()

    return render(request, 'manage_service.html', {'page_obj': page_obj, 'form': form})
def edit_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)  # Lấy dịch vụ theo ID

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)  # Sử dụng instance để cập nhật
        if form.is_valid():
            form.save()
            return redirect('manage_service')  # Quay lại trang danh sách dịch vụ
    else:
        form = ServiceForm(instance=service)  # Hiển thị thông tin hiện tại của dịch vụ

    return render(request, 'edit_service.html', {'form': form, 'service': service})

def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    service.delete()  # Xóa dịch vụ
    return redirect('manage_service') 
