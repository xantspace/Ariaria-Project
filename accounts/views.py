from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order
from products.models import Product, Category
from products.forms import ProductForm

User = get_user_model()


def auth_page(request):
    """Single page for both login and signup"""
    return render(request, 'accounts/auth.html')


def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')  # Add this
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role', 'buyer')  # Get role from form

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('accounts:auth')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('accounts:auth')

        # Create user with role
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=name,
            role=role,
            phone_number=phone
        )

        # Auto login after signup
        login(request, user)

        # Redirect based on role
        if role == 'seller':
            return redirect('accounts:seller_dashboard')
        else:
            return redirect('accounts:dashboard')

    return redirect('accounts:auth')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Redirect based on user type
            if user.role == 'seller':
                request.session["account_info"] = user.id    #
                return redirect('accounts:seller_dashboard')
            else:
                request.session["account_info"] = user.id    #
                return redirect('accounts:dashboard')
        else:
            messages.error(request, "Invalid login details")
            return redirect('accounts:auth')

    return redirect('accounts:auth')


@login_required(login_url='accounts:auth')
def dashboard(request):
    # get user id from session and allows for only logged in users
    user = request.session.get("account_info")
    if user == None:
        return redirect("accounts:auth")
    # Block sellers
    if request.user.role == 'seller':
        return redirect('accounts:seller_dashboard')

    # Base queryset (NOT sliced)
    base_orders = Order.objects.filter(user=request.user)

    # Aggregates (work on full queryset)
    total_orders = base_orders.count()
    pending_orders = base_orders.filter(status='pending').count()
    completed_orders = base_orders.filter(status='completed').count()

    # Recent orders (slice LAST)
    recent_orders = base_orders.order_by('-created_at')[:5]

    context = {
        "orders": recent_orders,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_spent": 4.2,  # compute later
    }

    return render(request, "accounts/dashboard.html", context)


@login_required(login_url='accounts:auth')
def seller_dashboard(request):
    # Check if user is seller
    if request.user.role != 'seller':
        return redirect('accounts:dashboard')

    seller = request.user

    # Handle product form submission
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()
            messages.success(request, "Product added successfully!")
            return redirect('accounts:seller_dashboard')
    else:
        form = ProductForm()

    # Seller products and categories
    products = Product.objects.filter(seller=seller)
    categories = Category.objects.all()

    # Context with stats (keep your mock data or calculate dynamically)
    context = {
        'form': form,
        'products': products,
        'categories': categories,
        'total_revenue': 12500,
        'new_orders': 12,
        'active_products': 45,
        'store_rating': 4.8,
        'recent_orders': [
            {
                'id': '8829',
                'product': 'Senator Wear',
                'quantity': 20,
                'buyer': 'Chinedu Retail',
                'status': 'paid',
            },
            {
                'id': '8831',
                'product': 'Johnkoso',
                'quantity': 50,
                'buyer': 'Kingsley Retail',
                'status': 'pending',
            },
        ],
    }

    return render(request, "accounts/sellers_dashboard.html", context)


@login_required(login_url='accounts:auth')
def seller_add_product(request):
    if request.user.role != 'seller':
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request, "Product added successfully!")
        else:
            messages.error(request, "Failed to add product. Check the form.")

    return redirect('accounts:seller_dashboard')


@login_required(login_url='accounts:auth')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('core:home')  # Redirect to homepage, not auth


@login_required(login_url='accounts:auth')
def inventory(request):
    return render(request, 'accounts/inventory.html', {})
