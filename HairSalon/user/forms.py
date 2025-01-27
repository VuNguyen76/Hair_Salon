from django import forms
from django.contrib.auth.models import User

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