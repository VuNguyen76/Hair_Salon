# middleware.py
from django.contrib import messages
from django.shortcuts import redirect

class RestrictStaffManageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):        # Kiểm tra xem người dùng đã đăng nhập chưa
        if request.user.is_authenticated:
            # Nếu người dùng là user thông thường (không phải staff hoặc admin), chặn không cho truy cập
            if request.path in ['/staff/', '/manage/'] and not (request.user.is_staff or request.user.is_superuser):
                messages.error(request, "Bạn không có quyền truy cập vào admin")
                return redirect('/')  # Chuyển hướng về trang chủ
        return self.get_response(request)
