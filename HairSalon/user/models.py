from django.db import models
from django.contrib.auth.models import User
from booking.models import Booking
class Infor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Số điện thoại
    reward_points = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return self.user.username
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username if self.user else 'Guest'} on {self.created_at}"