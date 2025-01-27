from django.db import models
from django.contrib.auth.models import User

class Infor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Số điện thoại

    def __str__(self):
        return self.user.username
