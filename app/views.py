from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.
def home(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'app/home.html',context)
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Lưu người dùng vào cơ sở dữ liệu
            username = form.cleaned_data.get('username')
            messages.success(request, f'Tài khoản của bạn đã được tạo thành công!')
            return redirect('login')  # Sau khi đăng ký xong, chuyển đến trang đăng nhập
    else:
        form = UserCreationForm()
    return render(request, 'app/register.html', {'form': form})

# View đăng nhập
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Sau khi đăng nhập, chuyển đến trang chủ
        else:
            messages.error(request, 'Tên người dùng hoặc mật khẩu không chính xác.')
    return render(request, 'app/login.html')

# View đăng xuất
def logout_view(request):
    logout(request)
    return redirect('home')  # Sau khi đăng xuất, chuyển đến trang chủ