# middleware.py
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse


def admin_access_middleware(get_response):
    def middleware(request):
        # Kiểm tra xem người dùng đã đăng nhập chưa và cố gắng vào trang admin
        if request.path.startswith('/admin/') and not request.user.is_authenticated:
            # Nếu chưa đăng nhập và đang cố gắng vào trang admin, chuyển hướng về trang đăng nhập
            if not request.path.startswith(reverse("admin:login")):
                return redirect(f'{reverse("admin:login")}?next={request.path}')

        # Nếu người dùng đã đăng nhập nhưng không phải là admin, từ chối quyền truy cập
        if request.path.startswith('/admin/') and request.user.is_authenticated and not request.user.is_superuser:
            return HttpResponseForbidden("Bạn không có quyền truy cập trang quản trị.")

        response = get_response(request)
        return response

    return middleware
