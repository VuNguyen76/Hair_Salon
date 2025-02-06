from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404, redirect
from booking.models import Booking
from django.core.paginator import Paginator
from decimal import Decimal


def staff(request):
    bookings_list = Booking.objects.all().order_by('-booking_date')
    paginator = Paginator(bookings_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate statistics
    completed_count = Booking.objects.filter(status='completed').count()
    pending_count = Booking.objects.filter(status='pending').count()
    canceled_count = Booking.objects.filter(status='canceled').count()

    context = {
        'page_obj': page_obj,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'canceled_count': canceled_count,
    }
    return render(request, 'staff_dashboard.html', context)
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from booking.models import Booking

def staff_booking_single(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)  # Lấy đơn đặt lịch theo ID

    if request.method == 'POST':
        new_status = request.POST.get('status')
        reward_points_used = request.POST.get('reward_points_used')  # Lấy số điểm muốn sử dụng từ form

        booking.status = new_status

        if new_status == 'completed':
            booking.revenue = booking.total_price()  # Cập nhật doanh thu nếu trạng thái là "Hoàn thành"
            earned_points = booking.revenue * Decimal('0.1')  # Tính điểm thưởng kiếm được

            # Cập nhật số điểm thưởng cho khách hàng
            if booking.user:
                user_profile = booking.user.infor  # Lấy thông tin người dùng
                reward_points_used = Decimal(reward_points_used) if reward_points_used else Decimal('0')

                if reward_points_used > user_profile.reward_points:
                    reward_points_used = user_profile.reward_points  # Không cho sử dụng nhiều hơn số điểm đang có
                
                booking.revenue -= reward_points_used  # Giảm doanh thu bằng số điểm sử dụng
                user_profile.reward_points -= reward_points_used  # Trừ điểm của khách
                user_profile.reward_points += earned_points  # Cộng điểm thưởng mới
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
