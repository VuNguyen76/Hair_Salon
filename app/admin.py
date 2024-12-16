from cProfile import Profile

from django.contrib import admin
from .models import *

#Đăng ký register từ models
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Post)
