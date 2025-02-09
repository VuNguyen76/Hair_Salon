from django.contrib import messages
from django.shortcuts import redirect

class RestrictStaffManageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if request.user.is_authenticated:
            # Nếu user là staff nhưng không phải superuser, chặn truy cập `/manage/`
            if request.path == '/manage/' and request.user.is_staff and not request.user.is_superuser:
                messages.error(request, "Nhân viên không có quyền truy cập vào trang quản lý")
                return redirect('/')  # Chuyển hướng về trang chủ

            # Nếu user không phải là staff hoặc admin, chặn truy cập `/staff/`, `/manage/`, `/admin/`
            if request.path in ['/staff/', '/manage/', '/admin/'] and not (request.user.is_staff or request.user.is_superuser):
                messages.error(request, "Bạn không có quyền truy cập vào trang này")
                return redirect('/')  # Chuyển hướng về trang chủ

        return self.get_response(request)
