from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    STATUS_CHOICES = [
        ('off', 'Xin nghỉ'),
        ('working', 'Đang làm'),
        ('on_leave', 'Đang nghỉ phép'),
    ]

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    position = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    reward = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='working')

    def __str__(self):
        return self.name
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}: {self.content[:20]}..."