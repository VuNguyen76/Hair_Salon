import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegistrationForm, CustomerForm
from .models import *


# Create your views here.
def home(request):
    context = {}
    return render(request, 'app/index.html', context)


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
    return render(request, 'app/checkout.html', context)


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
    context = {}
    return render(request, 'app/admin.html', context)


def staff_view(request):
    context = {}
    return render(request, 'app/staff_dashboard.html', context)


# @receiver(post_save, sender=User)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         Customer.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_customer(sender, instance, **kwargs):
#     instance.customer.save()
# Kiểm tra xem người dùng có phải admin không
def is_admin(user):
    return user.is_superuser


# Admin có quyền xem và quản lý tất cả bài viết
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    posts = Post.objects.all()
    return render(request, 'app/admin.html', {'posts': posts})


# Staff chỉ có thể xem và quản lý bài viết của chính mình
@login_required
def staff_dashboard(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'app/staff_dashboard.html', {'posts': posts})


# View tạo bài viết
@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')  # Get the uploaded image

        # Create the new post
        post = Post.objects.create(
            title=title,
            content=content,
            author=request.user,
            image=image  # Save the image if it was uploaded
        )

        messages.success(request, 'Bài viết đã được tạo thành công.')
        return redirect('staff_dashboard')

    return render(request, 'app/create_post.html')  # Return the form for GET requests


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user and not request.user.is_superuser:
        return redirect('staff_dashboard')  # Unauthorized edit attempt

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.image = request.FILES.get('image', post.image)  # Update the image if a new one is uploaded
        post.save()
        return redirect('staff_dashboard')

    return render(request, 'app/edit_post.html', {'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.author or request.user.is_superuser:
        post.delete()
        messages.success(request, 'Bài viết đã được xóa thành công.')
    else:
        messages.error(request, 'Bạn không có quyền xóa bài viết này.')

    return redirect('staff_dashboard')
