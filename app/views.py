from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .forms import UserRegistrationForm, CustomerForm
from .models import *
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your views here.
def home(request):
    context = {}
    return render(request, 'app/index.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
    context = {'items': items, 'order': order}
    return render(request, 'app/cart.html', context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
    context = {'items': items, 'order': order}
    return render(request,'app/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)

    # Lấy hoặc tạo đơn hàng
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    # Lấy hoặc tạo OrderItem
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Thêm hoặc giảm số lượng sản phẩm
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove' and orderItem.quantity > 0:  # Không cho phép giảm xuống dưới 0
        orderItem.quantity -= 1

    # Lưu lại thay đổi
    orderItem.save()

    # Xóa OrderItem nếu số lượng sản phẩm là 0 hoặc âm
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse({'success': True, 'message': 'Updated cart successfully'})
# View đăng ký
def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        customer_form = CustomerForm(request.POST)

        if user_form.is_valid() and customer_form.is_valid():
            # Lưu user (User model)
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])  # Mã hóa mật khẩu
            user.save()

            # Lưu customer (Customer model)
            customer = customer_form.save(commit=False)
            customer.user = user  # Gắn người dùng vào khách hàng
            customer.save()

            # Đăng nhập người dùng
            login(request, user)

            return redirect('home')  # Điều hướng sau khi đăng ký thành công

    else:
        user_form = UserRegistrationForm()
        customer_form = CustomerForm()

    return render(request, 'app/register.html', {
        'user_form': user_form,
        'customer_form': customer_form,
    })
# View đăng nhập
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Kiểm tra xem người dùng có phải là admin không
            if user.is_superuser:
                # Nếu là admin, thông báo lỗi và chuyển hướng về trang login
                messages.error(request, "Bạn không thể đăng nhập bằng tài khoản admin.")
                return redirect('login')

            # Nếu không phải admin, tiến hành đăng nhập
            login(request, user)
            return redirect('home')  # Điều hướng đến trang chủ (index) sau khi đăng nhập thành công

        else:
            # Nếu đăng nhập không thành công
            messages.error(request, 'Thông tin đăng nhập không hợp lệ.')
            return render(request, 'app/login.html')
    else:
        return render(request, 'app/login.html')

# View đăng xuất
def logout_view(request):
    logout(request)
    return redirect('home')  # Sau khi đăng xuất, chuyển đến trang chủ
def admin_view(request):
    context ={}
    return render(request, 'app/admin.html', context)
def staff_view(request):
    context ={}
    return render(request,'app/staff.html', context)
# @receiver(post_save, sender=User)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_customer(sender, instance, **kwargs):
#     instance.customer.save()
