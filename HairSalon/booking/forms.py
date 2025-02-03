from django import forms
from .models import Booking
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'phone_number', 'full_name', 'gender', 
            'branch', 'services', 'message', 
            'booking_date', 'booking_time'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'formInput', 'placeholder': 'Số điện thoại'}),
            'full_name': forms.TextInput(attrs={'class': 'formInput', 'placeholder': 'Họ Tên'}),
            'gender': forms.Select(attrs={'class': 'formInput'}, choices=[('Anh/Chị', 'Anh/Chị'), ('nam', 'Anh'), ('nữ', 'Chị')]),
            'branch': forms.Select(attrs={'class': 'formInput'}, choices=[
                ('', 'Chi nhánh'),
                ('Hà nội', 'CN Hair Salon 145 Chùa Láng, Đống Đa, Hà Nội'),
                ('Đà nẵng', 'CN Hair Salon 85 Đ. Trần Cao Vân, Hội An, Quảng Nam'),
                ('HCM', 'CN Hair Salon 189 Trung Mỹ Tây, Tô Ký, Q.12, TP.HCM')
            ]),
            'services': forms.CheckboxSelectMultiple(attrs={'class': 'formInput'}),
            'message': forms.Textarea(attrs={'class': 'formTextarea', 'placeholder': 'Lời nhắn...', 'rows': 5}),
            'booking_date': forms.Select(attrs={'class': 'formInput'}, choices=[
                ('','Chọn ngày đặt lịch'),
                ('Thứ 2', 'Thứ 2'),
                ('Thứ 3', 'Thứ 3'),
                ('Thứ 4', 'Thứ 4'),
                ('Thứ 5', 'Thứ 5'),
                ('Thứ 6', 'Thứ 6'),
                ('Thứ 7', 'Thứ 7'),
                ('Chủ nhật', 'Chủ nhật')
            ]),
            'booking_time': forms.Select(attrs={'class': 'formInput'}, choices=[
                ('','Chọn thời gian đặt lịch'),
                ('8:30', '8:30'),
                ('9:00', '9:00'),
                ('9:30', '9:30'),
                ('10:00', '10:00'),
                ('10:30', '10:30'),
                ('11:00', '11:00'),
                ('11:30', '11:30'),
                ('12:00', '12:00'),
                ('12:30', '12:30'),
                ('13:00', '13:00'),
                ('13:30', '13:30'),
                ('14:00', '14:00'),
                ('14:30', '14:30'),
                ('15:00', '15:00'),
                ('15:30', '15:30'),
                ('16:00', '16:00'),
                ('16:30', '16:30'),
                ('17:00', '17:00'),
                ('17:30', '17:30'),
                ('18:00', '18:00'),
                ('18:30', '18:30'),
                ('19:00', '19:00'),
                ('19:30', '19:30')
            ]),
        }
        error_messages = {
            'service': {
                'required': 'Vui lòng chọn ít nhất một dịch vụ.'
            }
        }
class LookupForm(forms.Form):
    phone_number = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'formInput', 'placeholder': 'Nhập số điện thoại'})
    )
