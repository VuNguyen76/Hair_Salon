from django.db import models
from django.contrib.auth.models import User
class Service(models.Model):    
    name = models.CharField(max_length=255)  # Tên dịch vụ
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá dịch vụ

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('in_progress', 'Đang thực hiện'),
        ('completed', 'Hoàn thành'),
        ('canceled', 'Đã hủy'),  # Thêm trạng thái hủy
    ]
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.0) #Doanh thu
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')#Trạng thái
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=15)  # Số điện thoại khách hàng
    full_name = models.CharField(max_length=100)  # Họ và tên khách hàng
    gender = models.CharField(max_length=10, blank=True, null=True)  # Giới tính (nếu có)
    branch = models.CharField(max_length=255)  # Chi nhánh salon
    services = models.ManyToManyField(Service)  # Liên kết nhiều dịch vụ cho một lịch hẹn
    message = models.TextField(blank=True, null=True)  # Lời nhắn của khách hàng
    booking_date = models.CharField(max_length=15)  # Ngày đặt lịch
    booking_time = models.CharField(max_length=15)  # Giờ đặt lịch

    def total_price(self):
        return sum(service.price for service in self.services.all())  # Tính tổng giá các dịch vụ đã chọn

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"