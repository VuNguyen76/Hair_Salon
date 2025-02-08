from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .models import Infor

class RegisterForm(forms.ModelForm):    
    phone = forms.CharField(required=True, max_length=15, label="Số điện thoại")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Tên người dùng này đã được đăng ký. Hãy thử một tên khác.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password != password_confirm:
            raise forms.ValidationError("Mật khẩu và mật khẩu xác nhận không khớp!")
        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserInfoChangeForm(forms.Form):
    username = forms.CharField(max_length=150, required=False, label="Tên người dùng")
    phone = forms.CharField(max_length=15, required=False, label="Số điện thoại")
    old_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Mật khẩu cũ")
    new_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Mật khẩu mới")
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False, label="Xác nhận mật khẩu mới")

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            # Kiểm tra nếu tên người dùng đã tồn tại và không phải là tên người dùng hiện tại
            if User.objects.filter(username=username).exclude(username=self.initial['username']).exists():
                raise ValidationError("Tên người dùng đã tồn tại. Vui lòng chọn tên khác.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password != confirm_password:
                raise ValidationError("Mật khẩu mới và xác nhận mật khẩu không khớp.")
        
        return cleaned_data