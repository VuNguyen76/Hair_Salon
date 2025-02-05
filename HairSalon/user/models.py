from django.db import models
from django.contrib.auth.models import User
from booking.models import Booking
class Infor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Số điện thoại
    reward_points = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    def __str__(self):
        return self.user.username
