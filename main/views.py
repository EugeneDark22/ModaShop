from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ContactForm, UserProfileForm, EditProfileForm
from .models import Product, Order, UserProfile


def index(request):
    return render(request, 'main/index.html')

def shop(request, category=None):
    products = Product.objects.filter(gender=category) if category else Product.objects.all()
    return render(request, 'main/shop.html', {'products': products, 'category': category})


def search(request):
    gender = request.GET.get('gender', 'all')
    category = request.GET.get('category')
    price_min = request.GET.get('price_min', 0)
    price_max = request.GET.get('price_max', 1000000)
    products = Product.objects.filter(gender=gender, price__gte=price_min, price__lte=price_max)
    if category:
        products = products.filter(category=category)
    return render(request, 'main/shop.html', {'products': products})

def about(request):
    return render(request, 'main/about.html')

@login_required
def profile(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'main/profile.html', {
        'user_orders': user_orders,
        'user_profile': user_profile
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Дякуємо за ваше повідомлення!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'main/contact.html', {'form': form})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'main/tovar.html', {'product': product})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    messages.success(request, 'Товар додано до кошика')
    return redirect('cart')

def cart(request):
    cart = request.session.get('cart', {})
    total_cost = 0
    products_info = []

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total_cost += subtotal
        products_info.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'main/kosh.html', {
        'products_info': products_info,
        'total_cost': total_cost
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')


@login_required
def process_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Ваш кошик порожній.")
            return redirect('cart')

        card_number = request.POST.get('card-number')
        card_expiration = request.POST.get('card-expiration')
        card_cvc = request.POST.get('card-cvc')
        address = request.POST.get('address')

        if not all([card_number, card_expiration, card_cvc, address]):
            messages.error(request, "Будь ласка, заповніть усі поля.")
            return redirect('cart')

        total_cost = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total_cost += product.price * quantity

        order = Order.objects.create(
            user=request.user,
            total_cost=total_cost,
            address=address
        )

        del request.session['cart']

        messages.success(request, "Ваше замовлення успішно оформлено!")
        return redirect('order_success')
    else:
        return redirect('cart')

@login_required
def order_success(request):
    return render(request, 'main/order_success.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    auth_logout(request)
    return redirect('index')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Ваш профіль успішно оновлено!')
            return redirect('edit_profile')
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.userprofile)

    return render(request, 'main/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })