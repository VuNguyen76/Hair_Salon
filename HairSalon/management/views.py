from django.shortcuts import render, redirect, get_object_or_404
from booking.models import Booking,Service
from .forms import ServiceForm, EmployeeForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Employee, Message
from user.models import Feedback
from django.contrib.auth.models import User

@login_required(login_url='/login/')
def manage_dashboard(request):
    # Tính tổng doanh thu từ các booking đã hoàn thành
    completed_bookings = Booking.objects.filter(status='completed').order_by('-id')
    total_revenue = sum(booking.revenue for booking in completed_bookings)
    
    # Tính số nhân viên
    total_employees = Employee.objects.count()

    # Lấy danh sách nhân viên
    employees_list = Employee.objects.all()

    # Phân trang
    paginator = Paginator(employees_list, 5)  # Hiển thị 10 nhân viên mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Tính số khách hàng phục vụ
    total_customers_served = Booking.objects.filter(status='completed').count()
    
    return render(request, 'manage_dashboard.html', {
        'page_obj': page_obj,
        'total_revenue': total_revenue,
        'total_employees': total_employees,
        'total_customers_served': total_customers_served
    })
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

def manage_employee(request):
    # Xử lý form thêm nhân viên
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_employee')  # Tải lại trang sau khi thêm nhân viên
    else:
        form = EmployeeForm()

    # Lấy danh sách nhân viên
    employees_list = Employee.objects.all()

    # Phân trang
    paginator = Paginator(employees_list, 5)  # Hiển thị 10 nhân viên mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Thống kê số lượng nhân viên theo từng trạng thái
    total_employees = employees_list.count()
    on_leave = employees_list.filter(status='leave').count()
    working = employees_list.filter(status='working').count()
    off = employees_list.filter(status='off').count()
    return render(request, 'manage_employee.html', {
        'form': form,
        'page_obj': page_obj,
        'total_employees': total_employees,
        'on_leave': on_leave,
        'working': working,
        'off':off
    })
# Hàm sửa thông tin nhân viên
def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('manage_employee')  # Chuyển về danh sách nhân viên
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form})

# Hàm xóa nhân viên
def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()
    return redirect('manage_employee')  # Chuyển về danh sách nhân viên

def manage_report(request):
    # Xác định người dùng hiện tại (quản lý hoặc nhân viên)
    user = request.user

    # Lấy tất cả tin nhắn giữa nhân viên và quản lý
    messages = Message.objects.filter(
        receiver=user
    ) | Message.objects.filter(
        sender=user
    ).order_by('timestamp')

    # Gửi tin nhắn khi có yêu cầu POST
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            receiver = User.objects.exclude(id=user.id).filter(is_staff=not user.is_staff).first()
            if receiver:
                Message.objects.create(sender=user, receiver=receiver, content=content)
            return redirect('manage_report')

    return render(request, 'manage_report.html', {'messages': messages})

def manage_feedback(request):
    # Chuyển hướng về trang chủ hoặc trang khác    
    feedback_list = Feedback.objects.all().order_by('-created_at')
    paginator = Paginator(feedback_list, 10)  # Hiển thị 10 nhân viên mỗi trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'manage_feedback.html', {'page_obj': page_obj})
