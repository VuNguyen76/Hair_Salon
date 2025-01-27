from django.db import models

class Booking(models.Model):
    phone_number = models.CharField(max_length=15)  # Bắt buộc
    full_name = models.CharField(max_length=100)  # Bắt buộc
    gender = models.CharField(max_length=10, blank=True, null=True)  # Không bắt buộc
    branch = models.CharField(max_length=255)  # Bắt buộc
    service = models.CharField(max_length=255)  # Bắt buộc
    message = models.TextField(blank=True, null=True)  # Không bắt buộc
    booking_date = models.CharField(max_length=15)  # Bắt buộc
    booking_time = models.CharField(max_length=15)  # Bắt buộc

    def __str__(self):
        return f"{self.full_name} - {self.phone_number}"
