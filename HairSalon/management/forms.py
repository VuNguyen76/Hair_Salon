from django import forms
from booking.models import Service
from .models import Employee

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'price', 'image', 'description']

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'phone_number', 'position', 'salary', 'reward', 'status']
        labels = {
            'name': 'Tên nhân viên',
            'phone_number': 'Số điện thoại',
            'position': 'Chức vụ',
            'salary': 'Lương',
            'reward': 'Thưởng',
            'status': 'Tình trạng',
        }
