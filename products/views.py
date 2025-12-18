from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from .forms import ProductForm 

def product_detail(request, pk):
    return render(request, 'product_detail.html')

def cart_view(request):
    return render(request, 'checkout.html')

def product_list(request):
    # Get all products
    products = Product.objects.filter(is_active=True).select_related('seller', 'category')
    
    # Get all categories for filter
    categories = Category.objects.all()
    
    # Filter by category (if selected)
    category_filter = request.GET.get('category')
    if category_filter:
        products = products.filter(category__slug=category_filter)
    
    # Filter by price range
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    # Filter by verified sellers only
    verified_only = request.GET.get('verified')
    if verified_only:
        products = products.filter(seller__is_verified=True)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    
    context = {
        'products': products,
        'categories': categories,
        'total_products': products.count(),
    }
    
    return render(request, 'product_list.html', context)


def product_detail(request, pk, slug):
    product = get_object_or_404(Product, pk=pk, slug=slug, is_active=True)
    
    # Get related products (same category)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(pk=product.pk)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    
    return render(request, 'products/product_detail.html', context)

