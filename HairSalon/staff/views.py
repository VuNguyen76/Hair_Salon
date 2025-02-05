from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from booking.models import Booking
from django.core.paginator import Paginator
from decimal import Decimal


def staff(request):
    bookings_list = Booking.objects.all()  # Lấy tất cả các đơn đặt lịch
    paginator = Paginator(bookings_list, 5 )  # Phân trang 10 đơn/ trang
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'staff_dashboard.html', {'page_obj': page_obj})
def staff_booking_single(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # Lấy đơn đặt lịch theo ID

    if request.method == 'POST':
        # Cập nhật trạng thái khi nhân viên gửi form
        new_status = request.POST.get('status')
        booking.status = new_status
        if new_status == 'completed':
            booking.revenue = booking.total_price()  # Cập nhật doanh thu nếu trạng thái là "Hoàn thành"
            reward_points = booking.revenue * Decimal('0.1')
            
            # Cập nhật số điểm thưởng cho khách hàng
            if booking.user:
                user_profile = booking.user.infor  # Lấy thông tin người dùng
                user_profile.reward_points += reward_points  # Thêm điểm thưởng
                user_profile.save()
        booking.save()

        return redirect('staff')  # Quay lại trang danh sách sau khi cập nhật

    return render(request, 'staff_booking_single.html', {'booking': booking})

def staff_booking_multiple(request):
    if request.method == 'POST':
        # Cập nhật trạng thái cho tất cả các đơn đặt lịch đã chọn
        bookings = Booking.objects.all()
        for booking in bookings:
            new_status = request.POST.get(f'status_{booking.id}')
            if new_status:
                booking.status = new_status
                if new_status == 'completed':
                    booking.revenue = booking.total_price()  # Cập nhật doanh thu
                    # Tính điểm thưởng (10% số tiền chi tiêu)
                    reward_points = booking.revenue * Decimal('0.1')
                    
                    # Cập nhật số điểm t    hưởng cho khách hàng
                    if booking.user:
                        user_profile = booking.user.infor
                        user_profile.reward_points += reward_points
                        user_profile.save()
 
                booking.save()

        return redirect('staff')  # Quay lại trang danh sách sau khi cập nhật

    bookings = Booking.objects.all()  # Lấy tất cả các đơn đặt lịch
    return render(request, 'staff_booking_multiple.html', {'bookings': bookings})
