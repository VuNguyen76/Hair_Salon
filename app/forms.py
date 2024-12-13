# forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Customer


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Mật khẩu")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Nhập lại mật khẩu")

    class Meta:
        model = User
        fields = ['username', 'email']  # Chỉ giữ lại email trong User form

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Mật khẩu không khớp.")
        return cleaned_data


class CustomerForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, label="Họ")
    last_name = forms.CharField(max_length=100, label="Tên")
    phone = forms.CharField(max_length=15, label="Số điện thoại")
    address = forms.CharField(max_length=255, required=False, label="Địa chỉ")

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone', 'address']  # Không bao gồm email
